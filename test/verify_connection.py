"""
Supabase Connection Verification Script

This script helps you verify your Supabase database connection details
and provides step-by-step instructions to fix any issues.

Usage:
    python test/verify_connection.py
"""

import sys
import os
import re
from pathlib import Path
from urllib.parse import urlparse, unquote

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def check_env_file():
    """Check if .env file exists and has DATABASE_URL."""
    env_path = Path(__file__).parent.parent / ".env"
    
    print("=" * 70)
    print("Step 1: Checking .env file")
    print("=" * 70)
    print()
    
    if not env_path.exists():
        print("❌ .env file not found!")
        print(f"   Expected location: {env_path}")
        print()
        print("💡 Solution:")
        print("   1. Create a .env file in the project root")
        print("   2. Add your DATABASE_URL")
        print()
        return False, None
    
    print(f"✓ .env file found at: {env_path}")
    print()
    
    # Read .env file
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Check for DATABASE_URL
        database_url = None
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('DATABASE_URL=') and not line.startswith('#'):
                database_url = line.split('=', 1)[1].strip().strip('"').strip("'")
                break
        
        if not database_url:
            print("❌ DATABASE_URL not found in .env file!")
            print()
            print("💡 Solution:")
            print("   Add this line to your .env file:")
            print("   DATABASE_URL=postgresql+psycopg://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres")
            print()
            return False, None
        
        print(f"✓ DATABASE_URL found in .env file")
        print()
        return True, database_url
        
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False, None


def parse_database_url(url):
    """Parse database URL and extract components."""
    print("=" * 70)
    print("Step 2: Parsing DATABASE_URL")
    print("=" * 70)
    print()
    
    # Mask password for display
    masked_url = re.sub(r':([^:@]+)@', r':***@', url)
    print(f"Database URL: {masked_url}")
    print()
    
    try:
        # Handle postgresql+psycopg:// format
        if url.startswith('postgresql+'):
            url = url.replace('postgresql+psycopg://', 'postgresql://', 1)
            url = url.replace('postgresql+asyncpg://', 'postgresql://', 1)
        
        parsed = urlparse(url)
        
        components = {
            'scheme': parsed.scheme,
            'username': parsed.username,
            'password': parsed.password,
            'hostname': parsed.hostname,
            'port': parsed.port or 5432,
            'database': parsed.path.lstrip('/') if parsed.path else 'postgres'
        }
        
        print("✓ URL parsed successfully")
        print()
        print("📋 Connection Details:")
        print(f"   Username: {components['username']}")
        print(f"   Password: {'***' if components['password'] else 'NOT SET'}")
        print(f"   Hostname: {components['hostname']}")
        print(f"   Port: {components['port']}")
        print(f"   Database: {components['database']}")
        print()
        
        return True, components
        
    except Exception as e:
        print(f"❌ Error parsing URL: {e}")
        print()
        print("💡 Common issues:")
        print("   - Missing password (should be: postgresql://user:password@host...)")
        print("   - Special characters in password not URL-encoded")
        print("   - Incorrect URL format")
        print()
        return False, None


def validate_supabase_format(components):
    """Validate if the URL looks like a Supabase URL."""
    print("=" * 70)
    print("Step 3: Validating Supabase Format")
    print("=" * 70)
    print()
    
    hostname = components['hostname']
    issues = []
    
    # Check hostname format
    if not hostname:
        issues.append("Hostname is missing")
    elif not hostname.endswith('.supabase.co'):
        issues.append(f"Hostname doesn't end with '.supabase.co' (got: {hostname})")
    elif not hostname.startswith('db.'):
        issues.append(f"Hostname should start with 'db.' (got: {hostname})")
    
    # Check username
    if components['username'] != 'postgres':
        issues.append(f"Username should be 'postgres' (got: {components['username']})")
    
    # Check port
    if components['port'] != 5432:
        issues.append(f"Port should be 5432 for direct connection (got: {components['port']})")
    
    # Check database
    if components['database'] != 'postgres':
        issues.append(f"Database should be 'postgres' (got: {components['database']})")
    
    if issues:
        print("⚠ Found potential issues:")
        for issue in issues:
            print(f"   - {issue}")
        print()
    else:
        print("✓ URL format looks correct for Supabase")
        print()
    
    # Extract project reference
    if hostname and hostname.startswith('db.') and hostname.endswith('.supabase.co'):
        project_ref = hostname.replace('db.', '').replace('.supabase.co', '')
        print(f"📌 Detected Project Reference: {project_ref}")
        print()
        print("💡 To verify this is correct:")
        print(f"   1. Go to https://supabase.com/dashboard")
        print(f"   2. Check your project URL - it should contain: {project_ref}")
        print(f"   3. Go to Settings → Database")
        print(f"   4. Compare the connection string")
        print()
    
    return len(issues) == 0


def check_password(components):
    """Check if password is set and provide tips."""
    print("=" * 70)
    print("Step 4: Checking Password")
    print("=" * 70)
    print()
    
    if not components['password']:
        print("❌ Password is missing!")
        print()
        print("💡 How to get your password:")
        print("   1. Go to Supabase Dashboard → Your Project")
        print("   2. Go to Settings → Database")
        print("   3. Find 'Database password' section")
        print("   4. Click 'Reset database password' if you don't know it")
        print("   5. Copy the password and add it to your .env file")
        print()
        print("   Format: DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@...")
        print()
        return False
    
    # Check if password might need URL encoding
    password = components['password']
    if any(char in password for char in ['@', '#', '$', '%', '&', '+', '=', '?', '/']):
        print("⚠ Password contains special characters")
        print("   If connection fails, you may need to URL-encode the password")
        print("   Example: @ becomes %40, # becomes %23")
        print()
    
    print("✓ Password is set")
    print()
    return True


def provide_next_steps():
    """Provide next steps for testing."""
    print("=" * 70)
    print("Next Steps")
    print("=" * 70)
    print()
    print("1. Run DNS test:")
    print("   python test/test_dns.py")
    print()
    print("2. If DNS test passes, run connection test:")
    print("   python test/test_db_connection.py")
    print()
    print("3. If connection fails, check:")
    print("   - Your Supabase project is active (not paused)")
    print("   - Your IP is allowed (if IP restrictions enabled)")
    print("   - Password is correct")
    print("   - Project reference ID is correct")
    print()
    print("4. Get correct connection string from Supabase:")
    print("   Dashboard → Settings → Database → Connection string → URI")
    print()


def main():
    """Main verification function."""
    print()
    print("🔍 Supabase Connection Verification")
    print()
    
    # Step 1: Check .env file
    env_ok, database_url = check_env_file()
    if not env_ok:
        provide_next_steps()
        sys.exit(1)
    
    # Step 2: Parse URL
    parse_ok, components = parse_database_url(database_url)
    if not parse_ok:
        provide_next_steps()
        sys.exit(1)
    
    # Step 3: Validate format
    format_ok = validate_supabase_format(components)
    
    # Step 4: Check password
    password_ok = check_password(components)
    
    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print()
    
    if format_ok and password_ok:
        print("✅ All checks passed! Your connection string looks correct.")
        print()
        print("Next: Run the connection test:")
        print("   python test/test_db_connection.py")
    else:
        print("⚠ Some issues found. Please review the details above.")
        print()
        if not password_ok:
            print("❌ Password is missing - this must be fixed before testing")
        if not format_ok:
            print("⚠ URL format has issues - please verify with Supabase dashboard")
    
    print()
    provide_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Verification interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

