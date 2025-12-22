# 🌐 How to View Database Tables in Chrome

## Quick Start

### 1. Start the Database
```bash
./start.sh
```

### 2. Open pgAdmin in Chrome
```bash
./open_chrome.sh
```

Or manually open: **http://localhost:5050**

---

## 📋 Step-by-Step Guide

### Step 1: Start Database
```bash
cd postgres_db
./start.sh
```

### Step 2: Open pgAdmin
**Option A: Use script (automatic)**
```bash
./open_chrome.sh
```

**Option B: Manual**
1. Open Chrome browser
2. Go to: http://localhost:5050

### Step 3: Login to pgAdmin
- **Email:** `admin@admin.com`
- **Password:** `admin`
- Click "Login"

### Step 4: Add Database Server
1. In the left panel, right-click **"Servers"**
2. Select **"Register"** → **"Server"**

3. **General Tab:**
   - Name: `FastAPI Local DB`
   - Click "Save"

4. **Connection Tab:**
   - Host name/address: `postgres` (or `host.docker.internal` on Mac/Windows)
   - Port: `5432`
   - Maintenance database: `fastapi_db`
   - Username: `postgres`
   - Password: `postgres123`
   - Check "Save password" (optional)
   - Click "Save"

### Step 5: Browse Tables
1. Expand **"FastAPI Local DB"** in left panel
2. Expand **"Databases"**
3. Expand **"fastapi_db"**
4. Expand **"Schemas"**
5. Expand **"public"**
6. Expand **"Tables"**
7. You'll see **"users"** table

### Step 6: View Table Data
1. Right-click on **"users"** table
2. Select **"View/Edit Data"** → **"All Rows"**
3. Table data will appear in the main panel

---

## 🔍 Query Data

### Using Query Tool
1. Right-click on **"fastapi_db"** database
2. Select **"Query Tool"**
3. Type SQL query:
   ```sql
   SELECT * FROM users;
   ```
4. Click **"Execute"** (or press F5)
5. Results appear below

### Example Queries
```sql
-- Get all users
SELECT * FROM users;

-- Count users
SELECT COUNT(*) FROM users;

-- Get specific user
SELECT * FROM users WHERE email = 'test@example.com';

-- Get active users only
SELECT * FROM users WHERE is_active = true;
```

---

## 📊 View Table Structure

1. Right-click on **"users"** table
2. Select **"Properties"**
3. Go to **"Columns"** tab
4. See all columns, data types, and constraints

---

## 🎯 Quick Access URLs

- **pgAdmin:** http://localhost:5050
- **PostgreSQL:** localhost:5432

---

## 💡 Tips

### Auto-refresh Data
- In Query Tool, click the refresh icon to reload data
- Or press F5

### Export Data
1. Right-click table → **"Backup"**
2. Choose format (CSV, SQL, etc.)
3. Download file

### Import Data
1. Right-click database → **"Restore"**
2. Select backup file
3. Restore data

### Create New Tables
1. Right-click **"Tables"** → **"Create"** → **"Table"**
2. Define columns
3. Set constraints
4. Save

---

## 🐛 Troubleshooting

### Can't Access http://localhost:5050
- Check if containers are running: `./status.sh`
- Wait 10 seconds after starting
- Try: http://127.0.0.1:5050

### Can't Connect to Database Server
- Make sure PostgreSQL container is running
- Use `postgres` as hostname (not `localhost`)
- On Mac/Windows, try `host.docker.internal`

### Chrome Won't Open
- Manually open: http://localhost:5050
- Check if port 5050 is available: `lsof -i :5050`

---

## ✨ All Set!

You can now:
- ✅ View tables in Chrome
- ✅ Query data
- ✅ Edit data
- ✅ Manage database visually

Happy browsing! 🚀

