"""
Comprehensive Diagnostic Tool

This script helps diagnose why the Supabase connection is failing.
"""

import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_internet():
    """Test if internet connection works."""
    print("🌐 Testing Internet Connection...")
    try:
        # Try to resolve google.com
        socket.gethostbyname("google.com")
        print("   ✓ Internet connection working (google.com resolved)")
        return True
    except:
        print("   ✗ Cannot connect to internet")
        return False


def test_supabase_dns():
    """Test if Supabase DNS works in general."""
    print("\n🔍 Testing Supabase DNS (general)...")
    try:
        # Try to resolve supabase.com
        ip = socket.gethostbyname("supabase.com")
        print(f"   ✓ Supabase.com resolved to {ip}")
        return True
    except:
        print("   ✗ Cannot resolve supabase.com")
        return False


def test_your_db_host():
    """Test if your specific database host resolves."""
    print("\n🗄️ Testing Your Database Host...")
    hostname = "db.imeqqvcsikolhdsseabg.supabase.co"
    print(f"   Hostname: {hostname}")
    try:
        ip = socket.gethostbyname(hostname)
        print(f"   ✓ Hostname resolved to {ip}")
        return True
    except Exception as e:
        print(f"   ✗ Cannot resolve hostname: {e}")
        return False


def main():
    print("=" * 70)
    print("DIAGNOSTIC REPORT")
    print("=" * 70)
    print()
    
    internet_ok = test_internet()
    supabase_ok = test_supabase_dns()
    db_ok = test_your_db_host()
    
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print()
    
    if internet_ok and supabase_ok and db_ok:
        print("✅ All tests passed! Connection should work.")
        print("\nNext: Run python test/test_db_connection.py")
    elif not internet_ok:
        print("❌ ISSUE: No internet connection")
        print("\n💡 SOLUTION:")
        print("   - Check your network connection")
        print("   - Check if you're connected to WiFi/Ethernet")
        print("   - Try accessing a website in your browser")
    elif not supabase_ok:
        print("❌ ISSUE: Cannot reach Supabase services")
        print("\n💡 SOLUTION:")
        print("   - Check Supabase status: https://status.supabase.com/")
        print("   - Check if Supabase is blocked by firewall/VPN")
        print("   - Try disabling VPN if you're using one")
    elif not db_ok:
        print("❌ ISSUE: Cannot resolve your database hostname")
        print("\n💡 MOST LIKELY CAUSES:")
        print("   1. Supabase project is PAUSED")
        print("   2. Project reference ID is incorrect")
        print("   3. Project was deleted")
        print()
        print("📋 YOUR PROJECT DETAILS:")
        print("   Project Reference: imeqqvcsikolhdsseabg")
        print("   Expected Hostname: db.imeqqvcsikolhdsseabg.supabase.co")
        print()
        print("✅ WHAT TO DO:")
        print("   1. Go to: https://supabase.com/dashboard")
        print("   2. Find your project")
        print("   3. Check if it says 'PAUSED' or 'INACTIVE'")
        print("   4. If paused, click 'Resume' or 'Restore'")
        print("   5. Wait 2-3 minutes for DNS to propagate")
        print("   6. Run this diagnostic again")
        print()
        print("   If project doesn't exist:")
        print("   - Create a new Supabase project")
        print("   - Get the new connection string")
        print("   - Update your .env file")
    
    print()


if __name__ == "__main__":
    main()

