"""
Database Connection Test Script

This script tests the connection to the Supabase PostgreSQL database.
Run this script to diagnose database connection issues.

Usage:
    python test/test_db_connection.py
    or
    python -m test.test_db_connection
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


def mask_password(url: str) -> str:
    """Mask password in connection string for display."""
    if "@" in url:
        parts = url.split("@")
        if ":" in parts[0]:
            user_pass = parts[0].split(":")
            if len(user_pass) >= 2:
                user_pass[1] = "***"
                parts[0] = ":".join(user_pass)
        return "@".join(parts)
    return url


async def test_connection():
    """Test database connection."""
    print("=" * 60)
    print("Database Connection Test")
    print("=" * 60)
    print()
    
    # Display configuration
    print("📋 Configuration:")
    print(f"   DATABASE_URL: {mask_password(settings.DATABASE_URL)}")
    print(f"   SKIP_DB_INIT: {settings.SKIP_DB_INIT}")
    print()
    
    # Process DATABASE_URL
    database_url = settings.DATABASE_URL
    if "postgresql://" in database_url and "+psycopg" not in database_url:
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    elif "postgresql+asyncpg://" in database_url:
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
    
    print(f"   Processed URL: {mask_password(database_url)}")
    print()
    
    # Create engine
    print("🔧 Creating database engine...")
    try:
        engine = create_async_engine(
            database_url,
            echo=False,  # Don't echo SQL in test
            pool_pre_ping=True,
        )
        print("   ✓ Engine created successfully")
    except Exception as e:
        print(f"   ✗ Failed to create engine: {e}")
        return False
    
    print()
    
    # Test connection
    print("🔌 Testing database connection...")
    try:
        async with engine.connect() as conn:
            print("   ✓ Connection established")
            
            # Test simple query
            print("   Testing query execution...")
            result = await conn.execute(text("SELECT version(), current_database(), current_user"))
            row = result.fetchone()
            
            if row:
                print("   ✓ Query executed successfully")
                print()
                print("📊 Database Information:")
                print(f"   PostgreSQL Version: {row[0]}")
                print(f"   Database Name: {row[1]}")
                print(f"   Current User: {row[2]}")
                print()
                
                # Test another query
                print("   Testing table listing...")
                result = await conn.execute(text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                    LIMIT 10
                """))
                tables = result.fetchall()
                
                if tables:
                    print(f"   ✓ Found {len(tables)} table(s) in public schema:")
                    for table in tables:
                        print(f"      - {table[0]}")
                else:
                    print("   ℹ No tables found in public schema")
                
                print()
                print("✅ Database connection test PASSED")
                return True
            else:
                print("   ✗ Query returned no results")
                return False
                
    except Exception as e:
        print(f"   ✗ Connection failed: {e}")
        print()
        print("❌ Database connection test FAILED")
        print()
        print("💡 Troubleshooting tips:")
        print("   1. Check your DATABASE_URL in .env file")
        print("   2. Verify your Supabase project is active")
        print("   3. Check your database password is correct")
        print("   4. Ensure your IP is allowed (if IP restrictions are enabled)")
        print("   5. Verify the hostname is correct")
        print("   6. Check your internet connection")
        return False
    
    finally:
        await engine.dispose()
        print("   ✓ Engine disposed")


async def main():
    """Main function."""
    try:
        success = await test_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

