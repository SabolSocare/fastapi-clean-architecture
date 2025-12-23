# FastAPI Clean Architecture Template

[![FastAPI](https://img.shields.io/badge/FastAPI-0.125.0-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.45-EE0000?style=flat&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-1.13.2-FF6B6B?style=flat&logo=alembic&logoColor=white)](https://alembic.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

A production-ready FastAPI backend template with clean layered architecture, following best practices for separation of concerns, dependency injection, and maintainability.

**🔗 Repository**: [github.com/SabolSocare/fastapi-clean-architecture](https://github.com/SabolSocare/fastapi-clean-architecture)

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Setup Instructions](#-setup-instructions)
- [Database Migrations](#️-database-migrations)
- [Development Flow](#-development-flow)
- [API Flow Example](#-api-flow-example)
- [Adding New Features](#-adding-new-features)
- [Common Commands](#️-common-commands)
- [Additional Resources](#-additional-resources)
- [License](#-license)

---

## ✨ Features

- 🏗️ **Clean Layered Architecture** - Separation of concerns with API, Schemas, Services, Models, and Database layers
- 🔌 **Dependency Injection** - FastAPI dependency injection for services and database sessions
- 🗄️ **Async Database** - SQLAlchemy async with PostgreSQL support
- 🔄 **Database Migrations** - Alembic for version-controlled database schema management
- ✅ **Type Safety** - Pydantic v2 schemas for request/response validation
- 🔐 **Password Hashing** - Bcrypt for secure password storage
- 🐳 **Docker Support** - Containerized PostgreSQL database setup
- 📝 **Auto Documentation** - Interactive API docs with Swagger UI and ReDoc
- 🔄 **Scalable Structure** - Easy to extend with new features
- 🧪 **Test Ready** - Architecture designed for easy testing

---

## 🎯 Project Overview

This is a FastAPI-based backend application with:
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Async ORM for database operations
- **Alembic** - Database migration tool
- **PostgreSQL** - Relational database
- **Pydantic v2** - Data validation using Python type annotations
- **Bcrypt** - Password hashing
- **Docker** - Containerized PostgreSQL database

---

## 🏗️ Architecture

The project follows a **layered architecture** pattern with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer (Routes)                    │
│  Handles HTTP requests/responses, validation, errors    │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│                 Schemas Layer                            │
│  Pydantic models for request/response validation        │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│                Service Layer                             │
│  Business logic, data processing, validation            │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│                 Model Layer                              │
│  SQLAlchemy ORM models (database tables)                │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│              Database Layer                              │
│  Database connection, session management                │
└─────────────────────────────────────────────────────────┘
```

### Architecture Principles

1. **Separation of Concerns**: Each layer has a single, well-defined responsibility
2. **Dependency Injection**: Services and dependencies are injected, not instantiated directly
3. **Layered Architecture**: Clear boundaries between API, business logic, and data access
4. **Scalability**: Easy to add new features without modifying existing code

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   │
│   ├── api/                    # API Routes Layer
│   │   └── v1/                 # API version 1
│   │       ├── __init__.py     # Router aggregation
│   │       ├── dependencies.py # Dependency injection functions
│   │       └── user.py         # User endpoints
│   │
│   ├── schemas/                # Pydantic Schemas Layer
│   │   ├── __init__.py
│   │   └── user.py             # User request/response schemas
│   │
│   ├── services/               # Business Logic Layer
│   │   └── user_service.py     # User business logic
│   │
│   ├── models/                 # Database Models Layer
│   │   ├── __init__.py
│   │   └── user.py             # User SQLAlchemy model
│   │
│   ├── db/                     # Database Layer
│   │   ├── __init__.py
│   │   ├── session.py          # Database session & engine
│   │   └── base.py             # Database connection verification
│   │
│   └── core/                   # Core Configuration
│       ├── __init__.py
│       ├── config.py           # Application settings (Pydantic v2)
│       └── security.py         # Security utilities (password hashing)
│
├── alembic/                    # Database Migrations
│   ├── versions/               # Migration files
│   ├── env.py                  # Alembic environment configuration
│   └── script.py.mako          # Migration template
│
├── postgres_db/                # Docker PostgreSQL setup
│   ├── docker-compose.yml
│   └── *.sh                    # Database management scripts
│
├── alembic.ini                  # Alembic configuration
├── migrate.sh                   # Migration helper script
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
└── README.md                    # This file
```

### Layer Responsibilities

| Layer | Responsibility | Files |
|-------|---------------|-------|
| **API** | Handle HTTP requests, routing, status codes | `api/v1/*.py` |
| **Schemas** | Validate request/response data | `schemas/*.py` |
| **Services** | Business logic, data processing | `services/*.py` |
| **Models** | Database table definitions | `models/*.py` |
| **Database** | Connection, session management | `db/*.py` |
| **Core** | Configuration, settings | `core/*.py` |

---

## 🚀 Quick Start

### Clone the Repository

```bash
git clone git@github.com:SabolSocare/fastapi-clean-architecture.git
cd fastapi-clean-architecture
```

Then follow the [Setup Instructions](#-setup-instructions) below.

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.13+ (or 3.9+)
- Docker and Docker Compose
- pip (Python package manager)

### Step 1: Clone and Navigate to Project

```bash
cd /Users/socaresabol/POC/vue_project/backend
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup Database with Docker

```bash
# Navigate to postgres_db directory
cd postgres_db

# Start PostgreSQL container
docker-compose up -d

# Check if containers are running
docker-compose ps
```

The database will be available at:
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `fastapi_db`
- **User**: `fastapi_user`
- **Password**: `fastapi_password`

### Step 5: Create Environment File

Create a `.env` file in the root directory:

```bash
cd ..  # Back to backend root
touch .env
```

Add the following to `.env`:

```env
# Database Configuration
DATABASE_URL=postgresql+psycopg://fastapi_user:fastapi_password@localhost:5432/fastapi_db

# Application Configuration
APP_NAME=FastAPI Backend
APP_VERSION=1.0.0
API_V1_STR=/api/v1

# Optional: Skip DB init on startup (set to True for production)
SKIP_DB_INIT=False
```

### Step 6: Run Database Migrations

```bash
# From the backend root directory
# Apply all pending migrations
./migrate.sh upgrade
# or
alembic upgrade head
```

**Important**: Always run migrations before starting the application, especially in production.

### Step 7: Run the Application

```bash
# From the backend root directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 8: Verify Setup

1. **Health Check**: http://localhost:8000/health
2. **API Docs**: http://localhost:8000/docs (Swagger UI)
3. **Alternative Docs**: http://localhost:8000/redoc

---

## 🔄 Development Flow

### How Data Flows Through the Application

```
1. HTTP Request
   ↓
2. API Route (api/v1/user.py)
   - Receives request
   - Validates using Pydantic schema
   - Calls service via dependency injection
   ↓
3. Schema Validation (schemas/user.py)
   - Validates request data structure
   - Converts to Python objects
   ↓
4. Service Layer (services/user_service.py)
   - Contains business logic
   - Performs data operations
   - Uses database session
   ↓
5. Model Layer (models/user.py)
   - SQLAlchemy ORM operations
   - Maps to database tables
   ↓
6. Database Layer (db/session.py)
   - Manages database connection
   - Executes SQL queries
   ↓
7. Response Flow (reverse)
   - Service returns model
   - Schema validates response
   - API returns JSON response
```

---

## 🗄️ Database Migrations

This project uses **Alembic** for database migrations. Migrations allow you to:
- Version control your database schema
- Safely update production databases
- Roll back changes if needed
- Track schema history

### Quick Migration Commands

```bash
# Apply all pending migrations
./migrate.sh upgrade
# or
alembic upgrade head

# Create a new migration (after modifying models)
./migrate.sh revision "Description of changes"
# or
alembic revision --autogenerate -m "Description of changes"

# View migration history
./migrate.sh history
# or
alembic history

# Check current database revision
./migrate.sh current
# or
alembic current

# Rollback one revision
alembic downgrade -1
```

### Migration Workflow

1. **Modify your SQLAlchemy model** in `app/models/`
2. **Create a migration**: `alembic revision --autogenerate -m "Description"`
3. **Review the generated migration** in `alembic/versions/`
4. **Apply the migration**: `alembic upgrade head`

### Important Notes

- **Always review** auto-generated migrations before applying
- **Never edit** migrations that have been applied to production
- **Run migrations separately** from application startup in production
- **Backup your database** before running migrations in production

For more details, see the migration files in `alembic/versions/` or run `./migrate.sh` for help.

---

## 📝 API Flow Example: Creating a User

Let's trace through the complete flow when creating a user:

### 1. **HTTP Request**
```http
POST /api/v1/users
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "secret123"
}
```

### 2. **API Route Handler** (`app/api/v1/user.py`)
```python
@router.post("/users", response_model=UserRead)
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    # user is automatically validated by UserCreate schema
    existing_user = await service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = await service.create_user(...)
    return db_user  # Automatically serialized to UserRead schema
```

**What happens:**
- FastAPI receives POST request at `/api/v1/users`
- Request body is validated against `UserCreate` schema
- `get_user_service` dependency injects `UserService` instance
- Calls service methods to check and create user

### 3. **Schema Validation** (`app/schemas/user.py`)
```python
class UserCreate(BaseModel):
    email: str      # Validates email format
    username: str   # Validates string type
    password: str   # Validates string type

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Pydantic v2 syntax
    
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime
```

**What happens:**
- Pydantic validates request data structure
- Ensures all required fields are present
- Type validation (strings, integers, etc.)

### 4. **Dependency Injection** (`app/api/v1/dependencies.py`)
```python
async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)
```

**What happens:**
- Creates `UserService` instance with database session
- `get_db` provides the database session
- Injected into route handler automatically

### 5. **Service Layer** (`app/services/user_service.py`)
```python
async def get_user_by_email(self, email: str) -> Optional[User]:
    result = await self.db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(self, email: str, username: str, hashed_password: str) -> User:
    db_user = User(email=email, username=username, hashed_password=hashed_password)
    self.db.add(db_user)
    await self.db.commit()
    await self.db.refresh(db_user)
    return db_user
```

**What happens:**
- Business logic executed here
- Database queries performed
- Transaction committed
- Returns SQLAlchemy model

### 6. **Model Layer** (`app/models/user.py`)
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    # ...
```

**What happens:**
- SQLAlchemy model represents database table
- ORM converts Python objects to SQL

### 7. **Response Serialization**
- Service returns `User` model
- FastAPI serializes using `UserRead` schema
- Returns JSON response:

```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "is_active": true
}
```

---

## ➕ Adding New Features

To add a new feature (e.g., "Product"), follow this order:

### Step 1: Create Database Model
**File**: `app/models/product.py`
```python
from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
```

### Step 2: Register Model
**File**: `app/db/base.py`
```python
from app.models.product import Product  # Add import
```

### Step 3: Create Migration
```bash
# Create a migration for the new model
alembic revision --autogenerate -m "Add product model"
alembic upgrade head
```

### Step 4: Create Schemas
**File**: `app/schemas/product.py`
```python
from pydantic import BaseModel, ConfigDict

class ProductCreate(BaseModel):
    name: str
    price: int

class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Pydantic v2 syntax
    
    id: int
    name: str
    price: int
```

### Step 5: Create Service
**File**: `app/services/product_service.py`
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.product import Product

class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def list_products(self):
        result = await self.db.execute(select(Product))
        return result.scalars().all()
    
    async def create_product(self, name: str, price: int):
        product = Product(name=name, price=price)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product
```

### Step 6: Add Dependency (if needed)
**File**: `app/api/v1/dependencies.py`
```python
from app.services.product_service import ProductService

async def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(db)
```

### Step 7: Create API Routes
**File**: `app/api/v1/product.py`
```python
from fastapi import APIRouter, Depends
from app.schemas.product import ProductCreate, ProductRead
from app.services.product_service import ProductService
from app.api.v1.dependencies import get_product_service

router = APIRouter()

@router.get("/products", response_model=list[ProductRead])
async def get_products(service: ProductService = Depends(get_product_service)):
    return await service.list_products()

@router.post("/products", response_model=ProductRead)
async def create_product(product: ProductCreate, service: ProductService = Depends(get_product_service)):
    return await service.create_product(product.name, product.price)
```

### Step 8: Register Router
**File**: `app/api/v1/__init__.py`
```python
from app.api.v1.product import router as product_router

router.include_router(product_router, tags=["products"])
```

---

## 🗂️ File Creation Order Summary

When building a new feature from scratch:

1. **`core/config.py`** - Configuration settings
2. **`db/session.py`** - Database engine & session
3. **`db/base.py`** - Database connection verification
4. **`models/your_model.py`** - Database model
5. **Create migration** - `alembic revision --autogenerate -m "Add your_model"`
6. **Apply migration** - `alembic upgrade head`
7. **`schemas/your_schema.py`** - Request/response schemas (Pydantic v2)
8. **`services/your_service.py`** - Business logic
9. **`api/v1/dependencies.py`** - Dependency functions (if needed)
10. **`api/v1/your_route.py`** - API endpoints
11. **`api/v1/__init__.py`** - Register router
12. **`main.py`** - Application entry point

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

## 🛠️ Common Commands

### Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations

```bash
# Apply all pending migrations
./migrate.sh upgrade
# or
alembic upgrade head

# Create a new migration
./migrate.sh revision "Description"
# or
alembic revision --autogenerate -m "Description"

# View migration history
./migrate.sh history
# or
alembic history

# Check current revision
./migrate.sh current
# or
alembic current

# Rollback one revision
alembic downgrade -1
```

### Docker Database

```bash
# View Docker containers
cd postgres_db && docker-compose ps

# Start database
cd postgres_db && docker-compose up -d

# Stop database
cd postgres_db && docker-compose stop

# Restart database
cd postgres_db && docker-compose restart
```

---

## ✅ Architecture Benefits

1. **Maintainability**: Clear separation makes code easy to understand and modify
2. **Testability**: Each layer can be tested independently
3. **Scalability**: Easy to add new features without affecting existing code
4. **Reusability**: Services and schemas can be reused across different endpoints
5. **Type Safety**: Pydantic schemas provide runtime validation and type hints

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [SQLAlchemy](https://www.sqlalchemy.org/) - The ORM used
- [Pydantic](https://docs.pydantic.dev/) - Data validation library

---

**Happy Coding! 🚀**

**⭐ Star this repo if you find it useful!**

