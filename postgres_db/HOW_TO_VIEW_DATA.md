# 📊 How to View Data in pgAdmin (Chrome)

## ✅ Table Created & Data Added!

Your `users` table now has **3 test users**. Here's how to view them:

---

## 🌐 Method 1: View in pgAdmin (Visual - Recommended)

### Step 1: Open pgAdmin
```bash
cd postgres_db
./open_chrome.sh
```

Or manually: **http://localhost:5050**

### Step 2: Login
- Email: `admin@admin.com`
- Password: `admin`

### Step 3: Connect to Database (if not already connected)
1. In left panel, expand **"Servers"**
2. If you see **"FastAPI Local DB"**, expand it
3. If not, add it:
   - Right-click **"Servers"** → **"Register"** → **"Server"**
   - **Name:** `FastAPI Local DB`
   - **Connection Tab:**
     - Host: `postgres`
     - Port: `5432`
     - Database: `fastapi_db`
     - Username: `postgres`
     - Password: `postgres123`
   - Click **"Save"**

### Step 4: Navigate to Table
1. Expand **"FastAPI Local DB"**
2. Expand **"Databases"**
3. Expand **"fastapi_db"**
4. Expand **"Schemas"**
5. Expand **"public"**
6. Expand **"Tables"**
7. You'll see **"users"** table

### Step 5: View Data
**Option A: View All Rows**
1. Right-click on **"users"** table
2. Select **"View/Edit Data"** → **"All Rows"**
3. Data appears in the main panel!

**Option B: Query Tool**
1. Right-click on **"fastapi_db"** database
2. Select **"Query Tool"**
3. Type: `SELECT * FROM users;`
4. Click **"Execute"** (or press F5)
5. Results appear below

---

## 💻 Method 2: View via Command Line

### Quick View
```bash
cd postgres_db
./view_data.sh
```

### Direct SQL
```bash
docker exec fastapi_postgres psql -U postgres -d fastapi_db -c "SELECT * FROM users;"
```

---

## 🧪 Method 3: View via FastAPI

### Start FastAPI
```bash
cd /Users/socaresabol/POC/vue_project/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Get Users via API
```bash
# In browser or curl
curl http://localhost:8000/api/v1/users

# Or open in browser
http://localhost:8000/api/v1/users
```

---

## 📋 Current Test Data

Your table has 3 users:

| ID | Email | Username | Active |
|----|-------|----------|--------|
| 1 | john@example.com | john_doe | ✅ |
| 2 | jane@example.com | jane_smith | ✅ |
| 3 | admin@example.com | admin | ✅ |

---

## 🔍 Common Issues & Solutions

### Issue: "Table not found" in pgAdmin
**Solution:**
1. Refresh pgAdmin (F5)
2. Reconnect to server
3. Make sure you're in the correct database: `fastapi_db`

### Issue: "No data" shown
**Solution:**
1. Check if table exists: `./view_data.sh`
2. If empty, add test data: `./add_test_data.sh`
3. Refresh pgAdmin view

### Issue: Can't connect to server
**Solution:**
1. Check containers are running: `./status.sh`
2. Use `postgres` as hostname (not `localhost`)
3. On Mac/Windows, try `host.docker.internal`

### Issue: Table structure looks wrong
**Solution:**
1. Right-click table → **"Properties"**
2. Check **"Columns"** tab
3. Verify all columns are there

---

## 🎯 Quick Commands Reference

```bash
# View data in terminal
./view_data.sh

# Add more test data
./add_test_data.sh

# Open pgAdmin in Chrome
./open_chrome.sh

# Check database status
./status.sh
```

---

## ✨ Tips for Viewing Data

### Auto-refresh
- In Query Tool, click refresh icon
- Or press F5 to re-execute query

### Filter Data
In Query Tool, use WHERE clause:
```sql
-- Active users only
SELECT * FROM users WHERE is_active = true;

-- Specific user
SELECT * FROM users WHERE email = 'john@example.com';

-- Search username
SELECT * FROM users WHERE username LIKE '%admin%';
```

### Export Data
1. Right-click table → **"Backup"**
2. Choose format (CSV, SQL, etc.)
3. Download file

### Edit Data
1. Right-click table → **"View/Edit Data"** → **"All Rows"**
2. Click on any cell to edit
3. Click **"Save"** button

---

## 🎉 You're All Set!

You should now be able to see your data in pgAdmin. If you still can't see it:

1. **Refresh pgAdmin** (F5)
2. **Reconnect** to the server
3. **Run:** `./view_data.sh` to verify data exists
4. **Check:** Make sure you're viewing the correct table

Happy viewing! 🚀

