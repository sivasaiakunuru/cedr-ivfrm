#!/usr/bin/env python3
"""
Unit tests for encryption functionality
"""

import unittest
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os


class MockEncryption:
    """Mock encryption class for testing"""
    
    def __init__(self, password=None):
        self.password = password or os.urandom(32)
        self.key = self._derive_key(self.password)
        self.cipher = Fernet(self.key)
    
    def _derive_key(self, password):
        """Derive encryption key from password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'cedr_salt_2026',  # Fixed salt for testing
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def encrypt(self, data):
        """Encrypt data"""
        if isinstance(data, dict):
            data = str(data).encode()
        elif isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data)
    
    def decrypt(self, encrypted_data):
        """Decrypt data"""
        return self.cipher.decrypt(encrypted_data)


class TestEncryption(unittest.TestCase):
    """Test cases for encryption functionality"""
    
    def setUp(self):
        self.enc = MockEncryption(b"test_password_123")
        self.sample_data = {
            "vehicle_id": "VEH001",
            "event": "SECURITY_ALERT",
            "severity": "HIGH"
        }
    
    def test_encryption_roundtrip(self):
        """Test encrypt then decrypt returns original data"""
        original = b"Test message for encryption"
        encrypted = self.enc.encrypt(original)
        decrypted = self.enc.decrypt(encrypted)
        
        self.assertEqual(original, decrypted)
    
    def test_encryption_changes_data(self):
        """Test that encryption actually changes the data"""
        original = b"Test message"
        encrypted = self.enc.encrypt(original)
        
        self.assertNotEqual(original, encrypted)
        self.assertIsInstance(encrypted, bytes)
    
    def test_deterministic_encryption(self):
        """Test that same data encrypts differently each time"""
        original = b"Test message"
        encrypted1 = self.enc.encrypt(original)
        encrypted2 = self.enc.encrypt(original)
        
        # Fernet includes a timestamp, so results should differ
        self.assertNotEqual(encrypted1, encrypted2)
        
        # But both should decrypt to same value
        self.assertEqual(self.enc.decrypt(encrypted1), original)
        self.assertEqual(self.enc.decrypt(encrypted2), original)
    
    def test_different_keys_produce_different_results(self):
        """Test that different keys produce different ciphertexts"""
        enc1 = MockEncryption(b"password1")
        enc2 = MockEncryption(b"password2")
        
        data = b"Secret message"
        cipher1 = enc1.encrypt(data)
        cipher2 = enc2.encrypt(data)
        
        self.assertNotEqual(cipher1, cipher2)
    
    def test_decryption_with_wrong_key_fails(self):
        """Test that decryption fails with wrong key"""
        enc1 = MockEncryption(b"correct_password")
        enc2 = MockEncryption(b"wrong_password")
        
        data = b"Secret message"
        encrypted = enc1.encrypt(data)
        
        # Should raise exception
        with self.assertRaises(Exception):
            enc2.decrypt(encrypted)
    
    def test_encrypt_dict(self):
        """Test encrypting dictionary data"""
        encrypted = self.enc.encrypt(self.sample_data)
        decrypted = self.enc.decrypt(encrypted)
        
        # Decrypted should be string representation of dict
        self.assertIn(b"VEH001", decrypted)
        self.assertIn(b"SECURITY_ALERT", decrypted)


if __name__ == "__main__":
    unittest.main(verbosity=2)
