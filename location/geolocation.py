"""
Geolocation and Position Tracking Module for CEDR

Tracks vehicle location during security events for:
- Attack location mapping
- Fleet correlation analysis
- Insurance claim verification
- Forensic timeline reconstruction
"""

import sqlite3
import json
import time
import math
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple


class GeolocationTracker:
    """
    GPS and location tracking for forensic analysis
    
    Features:
    - GPS coordinate logging
    - Speed and heading tracking
    - Geofencing alerts
    - Location-based attack correlation
    - Route reconstruction
    """
    
    def __init__(self, vehicle_id: str, storage_path: str = None):
        self.vehicle_id = vehicle_id
        self.db_path = storage_path or f"/tmp/cedr_location_{vehicle_id}.db"
        self._init_database()
        
        # Current state
        self.current_position = None  # (lat, lon)
        self.current_speed = 0.0
        self.current_heading = 0.0
        self.last_update_time = None
        
        # Geofencing
        self.geofences = []
        
    def _init_database(self):
        """Initialize location database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Location history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS location_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                altitude REAL,
                speed REAL,
                heading REAL,
                accuracy REAL,  -- GPS accuracy in meters
                source TEXT,    -- gps, cellular, wifi
                related_event_id INTEGER
            )
        ''')
        
        # Create index for faster queries
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_location_time 
            ON location_history(timestamp)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_location_event 
            ON location_history(related_event_id)
        ''')
        
        # Geofence definitions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS geofences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                radius_meters REAL NOT NULL,
                geofence_type TEXT,  -- danger_zone, safe_zone, facility
                alert_on_entry INTEGER DEFAULT 1,
                alert_on_exit INTEGER DEFAULT 0,
                created_at REAL NOT NULL
            )
        ''')
        
        # Geofence events
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS geofence_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                geofence_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,  -- ENTER, EXIT
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                related_security_event_id INTEGER
            )
        ''')
        
        # Location-based attack correlation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS location_correlations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                attack_type TEXT NOT NULL,
                location_lat REAL NOT NULL,
                location_lon REAL NOT NULL,
                radius_meters REAL DEFAULT 1000,
                affected_vehicles TEXT,  -- JSON array
                description TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def update_position(self, 
                       latitude: float, 
                       longitude: float,
                       altitude: float = None,
                       speed: float = None,
                       heading: float = None,
                       accuracy: float = None,
                       source: str = "gps",
                       related_event_id: int = None) -> dict:
        """
        Update vehicle position
        
        Args:
            latitude: GPS latitude (-90 to 90)
            longitude: GPS longitude (-180 to 180)
            altitude: Altitude in meters
            speed: Speed in m/s
            heading: Heading in degrees (0-360)
            accuracy: GPS accuracy in meters
            source: Position source (gps, cellular, wifi)
            related_event_id: Link to security event
        """
        timestamp = time.time()
        
        # Validate coordinates
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            raise ValueError("Invalid coordinates")
        
        # Update current state
        self.current_position = (latitude, longitude)
        self.current_speed = speed or 0.0
        self.current_heading = heading or 0.0
        self.last_update_time = timestamp
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert location record
        cursor.execute('''
            INSERT INTO location_history
            (timestamp, latitude, longitude, altitude, speed, heading, accuracy, source, related_event_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, latitude, longitude, altitude, speed, heading, accuracy, source, related_event_id))
        
        location_id = cursor.lastrowid
        
        # Check geofences
        geofence_alerts = self._check_geofences(cursor, latitude, longitude, timestamp, related_event_id)
        
        conn.commit()
        conn.close()
        
        return {
            'location_id': location_id,
            'timestamp': timestamp,
            'position': (latitude, longitude),
            'speed': speed,
            'heading': heading,
            'geofence_alerts': geofence_alerts
        }
    
    def _check_geofences(self, cursor, lat: float, lon: float, 
                        timestamp: float, event_id: int = None) -> List[dict]:
        """Check if position triggers any geofence alerts"""
        alerts = []
        
        cursor.execute('SELECT * FROM geofences')
        geofences = cursor.fetchall()
        
        for geo in geofences:
            geo_id = geo[0]
            geo_name = geo[1]
            geo_lat = geo[2]
            geo_lon = geo[3]
            geo_radius = geo[4]
            alert_entry = geo[6]
            alert_exit = geo[7]
            
            # Calculate distance
            distance = self._haversine_distance(lat, lon, geo_lat, geo_lon)
            
            # Check if currently inside
            is_inside = distance <= geo_radius
            
            # Check previous state
            cursor.execute('''
                SELECT event_type FROM geofence_events
                WHERE geofence_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (geo_id,))
            
            last_event = cursor.fetchone()
            was_inside = last_event and last_event[0] == 'ENTER'
            
            # Detect transitions
            if is_inside and not was_inside and alert_entry:
                cursor.execute('''
                    INSERT INTO geofence_events
                    (timestamp, geofence_id, event_type, latitude, longitude, related_security_event_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (timestamp, geo_id, 'ENTER', lat, lon, event_id))
                
                alerts.append({
                    'type': 'GEOFENCE_ENTER',
                    'geofence': geo_name,
                    'distance_meters': distance
                })
            
            elif not is_inside and was_inside and alert_exit:
                cursor.execute('''
                    INSERT INTO geofence_events
                    (timestamp, geofence_id, event_type, latitude, longitude, related_security_event_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (timestamp, geo_id, 'EXIT', lat, lon, event_id))
                
                alerts.append({
                    'type': 'GEOFENCE_EXIT',
                    'geofence': geo_name,
                    'distance_meters': distance
                })
        
        return alerts
    
    def _haversine_distance(self, lat1: float, lon1: float, 
                           lat2: float, lon2: float) -> float:
        """Calculate distance between two GPS coordinates in meters"""
        R = 6371000  # Earth's radius in meters
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi / 2) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * \
            math.sin(delta_lambda / 2) ** 2
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def add_geofence(self, name: str, latitude: float, longitude: float,
                    radius_meters: float, geofence_type: str = "custom",
                    alert_on_entry: bool = True, alert_on_exit: bool = False) -> dict:
        """Add a new geofence zone"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO geofences
            (name, latitude, longitude, radius_meters, geofence_type, alert_on_entry, alert_on_exit, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, latitude, longitude, radius_meters, geofence_type,
              int(alert_on_entry), int(alert_on_exit), time.time()))
        
        geofence_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'geofence_id': geofence_id,
            'name': name,
            'center': (latitude, longitude),
            'radius': radius_meters
        }
    
    def get_route_during_event(self, event_id: int, 
                              buffer_seconds: float = 60) -> List[dict]:
        """
        Reconstruct vehicle route during a security event
        
        Args:
            event_id: The security event ID
            buffer_seconds: Time before/after event to include
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get event timestamp
        cursor.execute('''
            SELECT timestamp FROM location_history
            WHERE related_event_id = ?
            LIMIT 1
        ''', (event_id,))
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            return []
        
        event_time = result[0]
        start_time = event_time - buffer_seconds
        end_time = event_time + buffer_seconds
        
        # Get route points
        cursor.execute('''
            SELECT timestamp, latitude, longitude, speed, heading, accuracy
            FROM location_history
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp
        ''', (start_time, end_time))
        
        points = cursor.fetchall()
        conn.close()
        
        return [{
            'timestamp': p[0],
            'position': (p[1], p[2]),
            'speed': p[3],
            'heading': p[4],
            'accuracy': p[5]
        } for p in points]
    
    def find_nearby_attacks(self, latitude: float, longitude: float,
                           radius_meters: float = 1000,
                           time_window_hours: float = 24) -> List[dict]:
        """
        Find security events that occurred near a location
        
        Useful for identifying attack hotspots or coordinated attacks
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_time = time.time() - (time_window_hours * 3600)
        
        cursor.execute('''
            SELECT lh.*, ve.event_type, ve.severity
            FROM location_history lh
            JOIN vehicle_events ve ON lh.related_event_id = ve.id
            WHERE lh.timestamp > ?
            AND lh.related_event_id IS NOT NULL
        ''', (cutoff_time,))
        
        events = cursor.fetchall()
        conn.close()
        
        nearby = []
        for event in events:
            event_lat = event[2]
            event_lon = event[3]
            
            distance = self._haversine_distance(latitude, longitude, event_lat, event_lon)
            
            if distance <= radius_meters:
                nearby.append({
                    'event_id': event[9],
                    'event_type': event[10],
                    'severity': event[11],
                    'distance_meters': distance,
                    'position': (event_lat, event_lon),
                    'timestamp': event[1]
                })
        
        # Sort by distance
        nearby.sort(key=lambda x: x['distance_meters'])
        return nearby
    
    def generate_location_report(self, start_time: float = None,
                                end_time: float = None) -> dict:
        """Generate comprehensive location and movement report"""
        if not end_time:
            end_time = time.time()
        if not start_time:
            start_time = end_time - (24 * 3600)  # Last 24 hours
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        report = {
            'report_id': f"LOC-{int(time.time())}",
            'vehicle_id': self.vehicle_id,
            'time_range': {'start': start_time, 'end': end_time},
            'summary': {},
            'route_points': [],
            'geofence_events': [],
            'security_events_at_location': []
        }
        
        # Get all location points
        cursor.execute('''
            SELECT timestamp, latitude, longitude, speed, heading, related_event_id
            FROM location_history
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp
        ''', (start_time, end_time))
        
        points = cursor.fetchall()
        
        if points:
            # Calculate statistics
            speeds = [p[3] for p in points if p[3] is not None]
            report['summary'] = {
                'total_points': len(points),
                'duration_hours': (points[-1][0] - points[0][0]) / 3600,
                'avg_speed': sum(speeds) / len(speeds) if speeds else 0,
                'max_speed': max(speeds) if speeds else 0,
                'security_events': sum(1 for p in points if p[5] is not None)
            }
            
            # Sample route points (every 10th point to reduce size)
            report['route_points'] = [{
                'timestamp': p[0],
                'position': (p[1], p[2]),
                'speed': p[3],
                'heading': p[4],
                'has_event': p[5] is not None
            } for p in points[::10]]
        
        # Get geofence events
        cursor.execute('''
            SELECT ge.timestamp, g.name, ge.event_type, ge.latitude, ge.longitude
            FROM geofence_events ge
            JOIN geofences g ON ge.geofence_id = g.id
            WHERE ge.timestamp BETWEEN ? AND ?
            ORDER BY ge.timestamp
        ''', (start_time, end_time))
        
        ge_events = cursor.fetchall()
        report['geofence_events'] = [{
            'timestamp': g[0],
            'geofence': g[1],
            'event_type': g[2],
            'position': (g[3], g[4])
        } for g in ge_events]
        
        conn.close()
        return report


# Demo
if __name__ == "__main__":
    print("=" * 60)
    print("Geolocation Tracker Demo")
    print("=" * 60)
    
    tracker = GeolocationTracker("VEH-GEO-001")
    
    # Add geofences
    print("\n[1] Adding geofences...")
    
    tracker.add_geofence(
        name="High Crime Area",
        latitude=43.6532,
        longitude=-79.3832,
        radius_meters=500,
        geofence_type="danger_zone"
    )
    print("  Added: High Crime Area")
    
    tracker.add_geofence(
        name="Secure Facility",
        latitude=43.7000,
        longitude=-79.4000,
        radius_meters=200,
        geofence_type="safe_zone"
    )
    print("  Added: Secure Facility")
    
    # Simulate movement
    print("\n[2] Simulating vehicle movement...")
    
    route = [
        (43.6500, -79.3800, 15.0, 90.0),   # Start
        (43.6510, -79.3810, 15.5, 90.0),
        (43.6520, -79.3820, 16.0, 90.0),
        (43.6530, -79.3830, 15.0, 90.0),   # Enter geofence
        (43.6535, -79.3835, 14.0, 90.0),
        (43.6540, -79.3840, 15.0, 90.0),   # Attack happens here
        (43.6550, -79.3850, 16.0, 90.0),
        (43.6560, -79.3860, 15.5, 90.0),   # Exit geofence
    ]
    
    attack_occurred = False
    for i, (lat, lon, speed, heading) in enumerate(route):
        event_id = None
        if i == 5 and not attack_occurred:  # Simulate attack at position 5
            event_id = 999
            attack_occurred = True
            print(f"  ⚠️  Attack recorded at position {i}")
        
        result = tracker.update_position(
            latitude=lat,
            longitude=lon,
            speed=speed,
            heading=heading,
            accuracy=5.0,
            related_event_id=event_id
        )
        
        if result['geofence_alerts']:
            for alert in result['geofence_alerts']:
                print(f"  📍 Geofence alert: {alert['type']} - {alert['geofence']}")
        
        time.sleep(0.1)
    
    # Get route during attack
    print("\n[3] Reconstructing route during attack...")
    
    route_during_attack = tracker.get_route_during_event(999, buffer_seconds=30)
    print(f"  Route points during attack: {len(route_during_attack)}")
    
    # Find nearby attacks
    print("\n[4] Finding attacks near location...")
    
    nearby = tracker.find_nearby_attacks(43.6532, -79.3832, radius_meters=1000)
    print(f"  Attacks within 1km: {len(nearby)}")
    
    # Generate location report
    print("\n[5] Generating location report...")
    
    report = tracker.generate_location_report()
    print(f"  Total points: {report['summary']['total_points']}")
    print(f"  Security events: {report['summary']['security_events']}")
    print(f"  Geofence events: {len(report['geofence_events'])}")
    
    print("\n" + "=" * 60)
    print("Geolocation Demo Complete")
    print("=" * 60)
