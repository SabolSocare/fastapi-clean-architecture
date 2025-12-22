# How to Verify Your Supabase Connection

## Quick Verification Steps

### 1. Run the Verification Script (Recommended)
```bash
source venv/bin/activate
python test/verify_connection.py
```

This will check:
- ✅ If .env file exists
- ✅ If DATABASE_URL is set
- ✅ If URL format is correct
- ✅ If password is set
- ✅ If it matches Supabase format

### 2. Verify in Supabase Dashboard

1. **Go to Supabase Dashboard**
   - Visit: https://supabase.com/dashboard
   - Login to your account

2. **Select Your Project**
   - Find your project in the list
   - Click on it to open

3. **Check Project Reference ID**
   - Look at the project URL in your browser
   - It should contain: `imeqqvcsikolhdsseabg` (or your project ref)
   - This should match the hostname in your DATABASE_URL

4. **Get Connection String**
   - Go to **Settings** → **Database**
   - Scroll to **Connection string** section
   - Select **URI** (not Connection pooling)
   - Copy the connection string
   - It should look like:
     ```
     postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
     ```

5. **Compare with Your .env**
   - Open your `.env` file
   - Compare the DATABASE_URL with what you copied
   - Make sure:
     - Hostname matches (db.[PROJECT-REF].supabase.co)
     - Password matches
     - Port is 5432
     - Database is postgres

### 3. Check Project Status

1. **Verify Project is Active**
   - In Supabase Dashboard, check if project shows as "Active"
   - If it shows "Paused", you need to resume it
   - Paused projects cannot accept connections

2. **Check Project Settings**
   - Go to **Settings** → **General**
   - Verify project is not deleted or archived

### 4. Test DNS Resolution

```bash
python test/test_dns.py
```

This will tell you if the hostname can be resolved.

**If DNS fails:**
- Check your internet connection
- Verify the project reference ID is correct
- Check if project is paused/deleted
- Try: `ping db.imeqqvcsikolhdsseabg.supabase.co`

### 5. Test Database Connection

```bash
python test/test_db_connection.py
```

This will:
- Test the actual database connection
- Execute a test query
- Show database information
- List available tables

## Common Issues and Solutions

### Issue 1: DNS Resolution Fails
**Error:** `nodename nor servname provided, or not known`

**Solutions:**
1. Verify project reference ID in Supabase dashboard
2. Check if project is active (not paused)
3. Check internet connection
4. Verify hostname format: `db.[PROJECT-REF].supabase.co`

### Issue 2: Connection Timeout
**Error:** Connection timeout

**Solutions:**
1. Check if IP restrictions are enabled in Supabase
2. Add your IP to allowed list in Supabase Dashboard
3. Check firewall settings
4. Try from different network

### Issue 3: Authentication Failed
**Error:** Password authentication failed

**Solutions:**
1. Reset database password in Supabase Dashboard
2. Update DATABASE_URL in .env file
3. URL-encode special characters in password
4. Make sure password doesn't have extra spaces

### Issue 4: Wrong URL Format
**Error:** Invalid connection string

**Solutions:**
1. Use the exact format from Supabase Dashboard
2. Make sure it starts with `postgresql://` or `postgresql+psycopg://`
3. Check for typos in hostname
4. Verify port is 5432

## Password URL Encoding

If your password contains special characters, you may need to URL-encode them:

| Character | Encoded |
|-----------|---------|
| `@` | `%40` |
| `#` | `%23` |
| `$` | `%24` |
| `%` | `%25` |
| `&` | `%26` |
| `+` | `%2B` |
| `=` | `%3D` |
| `?` | `%3F` |
| `/` | `%2F` |
| ` ` (space) | `%20` |

**Example:**
- Password: `MyP@ss#123`
- Encoded: `MyP%40ss%23123`
- URL: `postgresql+psycopg://postgres:MyP%40ss%23123@db.xxx.supabase.co:5432/postgres`

## Verification Checklist

- [ ] .env file exists
- [ ] DATABASE_URL is set in .env
- [ ] URL format is correct
- [ ] Project reference ID matches Supabase dashboard
- [ ] Password is correct
- [ ] Project is active (not paused)
- [ ] DNS resolution works (test_dns.py passes)
- [ ] Database connection works (test_db_connection.py passes)

## Getting Help

If all checks pass but connection still fails:

1. **Check Supabase Status Page**
   - https://status.supabase.com/
   - Check for service outages

2. **Check Supabase Logs**
   - Go to Dashboard → Logs
   - Look for connection errors

3. **Contact Supabase Support**
   - If project is active but can't connect
   - Provide project reference ID

4. **Verify Network**
   - Try from different network
   - Check VPN/firewall settings
   - Test with `ping` command

