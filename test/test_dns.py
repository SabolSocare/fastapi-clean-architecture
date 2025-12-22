"""
DNS Resolution Test Script

This script tests if the Supabase database hostname can be resolved.
Run this before testing the database connection.

Usage:
    python test/test_dns.py
"""

import socket
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
import re


def extract_hostname(url: str) -> str:
    """Extract hostname from database URL."""
    # Match patterns like: postgresql://user:pass@host:port/db
    # or postgresql+psycopg://user:pass@host:port/db
    match = re.search(r'@([^:/]+)', url)
    if match:
        return match.group(1)
    return None


def test_dns(hostname: str) -> bool:
    """Test DNS resolution for hostname."""
    try:
        ip_address = socket.gethostbyname(hostname)
        return True, ip_address
    except socket.gaierror as e:
        return False, str(e)


def main():
    """Main function."""
    print("=" * 60)
    print("DNS Resolution Test")
    print("=" * 60)
    print()
    
    database_url = settings.DATABASE_URL
    hostname = extract_hostname(database_url)
    
    if not hostname:
        print("✗ Could not extract hostname from DATABASE_URL")
        print(f"   URL: {database_url[:50]}...")
        sys.exit(1)
    
    print(f"📋 Hostname to test: {hostname}")
    print()
    
    print("🔍 Testing DNS resolution...")
    success, result = test_dns(hostname)
    
    if success:
        print(f"   ✓ DNS resolution successful")
        print(f"   ✓ IP Address: {result}")
        print()
        print("✅ DNS test PASSED - Hostname can be resolved")
        print()
        print("💡 Next step: Run test_db_connection.py to test the database connection")
        sys.exit(0)
    else:
        print(f"   ✗ DNS resolution failed: {result}")
        print()
        print("❌ DNS test FAILED - Cannot resolve hostname")
        print()
        print("💡 Troubleshooting tips:")
        print("   1. Check your internet connection")
        print("   2. Verify the hostname is correct in your .env file")
        print("   3. Check if your Supabase project is active (not paused)")
        print("   4. Try pinging the hostname: ping " + hostname)
        print("   5. Check your DNS settings")
        print("   6. Verify the Supabase project reference ID is correct")
        sys.exit(1)


if __name__ == "__main__":
    main()

