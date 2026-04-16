#!/usr/bin/env python3
"""
Unit tests for hash chain functionality
"""

import unittest
import json
import hashlib
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from examples.basic_logging import HashChain


class TestHashChain(unittest.TestCase):
    """Test cases for HashChain class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.chain = HashChain()
        self.sample_event = {
            "vehicle_id": "TEST001",
            "event_type": "TEST_EVENT",
            "severity": "INFO",
            "details": "Test event for unit testing"
        }
    
    def test_genesis_hash(self):
        """Test that genesis hash is initialized correctly"""
        self.assertEqual(self.chain.previous_hash, "0" * 64)
        self.assertEqual(len(self.chain.events), 0)
    
    def test_add_event(self):
        """Test adding an event to the chain"""
        hash_value = self.chain.add_event(self.sample_event)
        
        # Verify event was added
        self.assertEqual(len(self.chain.events), 1)
        
        # Verify hash format (SHA-256 hex)
        self.assertEqual(len(hash_value), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in hash_value))
    
    def test_event_structure(self):
        """Test that events have correct structure"""
        self.chain.add_event(self.sample_event)
        event = self.chain.events[0]
        
        # Check required fields
        self.assertIn("timestamp", event)
        self.assertIn("data", event)
        self.assertIn("hash", event)
        self.assertIn("previous_hash", event)
        
        # Check data integrity
        self.assertEqual(event["data"], self.sample_event)
        self.assertEqual(event["previous_hash"], "0" * 64)
    
    def test_hash_linkage(self):
        """Test that events are properly linked"""
        # Add multiple events
        for i in range(5):
            event = {**self.sample_event, "sequence": i}
            self.chain.add_event(event)
        
        # Verify linkage
        for i in range(1, len(self.chain.events)):
            current = self.chain.events[i]
            previous = self.chain.events[i-1]
            
            self.assertEqual(current["previous_hash"], previous["hash"])
    
    def test_verify_integrity_valid(self):
        """Test integrity verification with valid chain"""
        # Add events
        for i in range(3):
            event = {**self.sample_event, "sequence": i}
            self.chain.add_event(event)
        
        # Verify integrity
        self.assertTrue(self.chain.verify_integrity())
    
    def test_verify_integrity_tampered(self):
        """Test integrity verification detects tampering"""
        # Add events
        for i in range(3):
            event = {**self.sample_event, "sequence": i}
            self.chain.add_event(event)
        
        # Tamper with event data
        self.chain.events[1]["data"]["severity"] = "CRITICAL"
        
        # Verify integrity fails
        self.assertFalse(self.chain.verify_integrity())
    
    def test_verify_integrity_tampered_hash(self):
        """Test detection of tampered hash"""
        self.chain.add_event(self.sample_event)
        
        # Tamper with hash directly
        original_hash = self.chain.events[0]["hash"]
        self.chain.events[0]["hash"] = "a" * 64
        
        # Verify integrity fails
        self.assertFalse(self.chain.verify_integrity())
        
        # Restore original
        self.chain.events[0]["hash"] = original_hash
        self.assertTrue(self.chain.verify_integrity())
    
    def test_verify_integrity_broken_link(self):
        """Test detection of broken hash linkage"""
        # Add two events
        self.chain.add_event(self.sample_event)
        self.chain.add_event({**self.sample_event, "sequence": 2})
        
        # Break the linkage
        self.chain.events[1]["previous_hash"] = "b" * 64
        
        # Verify integrity fails
        self.assertFalse(self.chain.verify_integrity())
    
    def test_empty_chain(self):
        """Test behavior with empty chain"""
        self.assertTrue(self.chain.verify_integrity())
        self.assertEqual(self.chain.export(), "[]")
    
    def test_export_format(self):
        """Test JSON export format"""
        self.chain.add_event(self.sample_event)
        
        exported = self.chain.export()
        parsed = json.loads(exported)
        
        self.assertIsInstance(parsed, list)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["data"], self.sample_event)


class TestHashChainEdgeCases(unittest.TestCase):
    """Edge case tests for HashChain"""
    
    def setUp(self):
        self.chain = HashChain()
    
    def test_unicode_data(self):
        """Test handling of unicode characters"""
        event = {
            "vehicle_id": "测试车辆",
            "event_type": "测试事件",
            "details": "Unicode test: ñ, é, 中文, العربية"
        }
        
        hash_value = self.chain.add_event(event)
        self.assertEqual(len(hash_value), 64)
        self.assertTrue(self.chain.verify_integrity())
    
    def test_large_data(self):
        """Test handling of large event data"""
        large_event = {
            "vehicle_id": "TEST001",
            "data": "x" * 10000  # 10KB of data
        }
        
        hash_value = self.chain.add_event(large_event)
        self.assertEqual(len(hash_value), 64)
        self.assertTrue(self.chain.verify_integrity())
    
    def test_nested_data(self):
        """Test handling of nested JSON structures"""
        nested_event = {
            "vehicle_id": "TEST001",
            "nested": {
                "level1": {
                    "level2": {
                        "level3": ["item1", "item2"]
                    }
                }
            }
        }
        
        self.chain.add_event(nested_event)
        self.assertTrue(self.chain.verify_integrity())
    
    def test_special_characters(self):
        """Test handling of special characters"""
        event = {
            "data": "<script>alert('xss')</script>",
            "sql": "DROP TABLE events; --",
            "path": "/etc/passwd",
            "null": None
        }
        
        self.chain.add_event(event)
        self.assertTrue(self.chain.verify_integrity())


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
