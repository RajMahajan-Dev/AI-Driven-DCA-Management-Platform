from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.config import settings
from app.api import auth_routes, case_routes, dca_routes, dashboard_routes, testing_routes, customer_routes, settings_routes, report_routes
from app.services import CaseService
from app.database import SessionLocal


# Initialize database tables
def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


# Initialize sample data
def init_sample_data():
    """Initialize sample data for demonstration."""
    from app.models import User, DCA, RoleEnum
    from app.auth import get_password_hash
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            return
        
        # Create admin user
        admin = User(
            email="admin@fedex.com",
            username="admin",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role=RoleEnum.ADMIN,
            is_active=True
        )
        db.add(admin)
        
        # Create internal user
        user = User(
            email="user@fedex.com",
            username="user",
            full_name="Internal User",
            hashed_password=get_password_hash("user123"),
            role=RoleEnum.INTERNAL_USER,
            is_active=True
        )
        db.add(user)
        
        # Create sample DCAs
        dca1 = DCA(
            name="Premium Recovery Services",
            contact_person="John Smith",
            email="john@premiumrecovery.com",
            phone="+1-555-0101",
            performance_score=85.5,
            max_capacity=100,
            is_active=True
        )
        db.add(dca1)
        
        dca2 = DCA(
            name="Global Collections Inc",
            contact_person="Sarah Johnson",
            email="sarah@globalcollections.com",
            phone="+1-555-0102",
            performance_score=78.2,
            max_capacity=150,
            is_active=True
        )
        db.add(dca2)
        
        dca3 = DCA(
            name="Swift Debt Solutions",
            contact_person="Michael Brown",
            email="michael@swiftdebt.com",
            phone="+1-555-0103",
            performance_score=92.1,
            max_capacity=80,
            is_active=True
        )
        db.add(dca3)
        
        db.commit()
        print("✓ Sample data initialized successfully")
        
    except Exception as e:
        print(f"Error initializing sample data: {e}")
        db.rollback()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print("Starting FedEx DCA Management Platform...")
    init_db()
    init_sample_data()
    
    # Initialize comprehensive dummy data
    try:
        from app.init_dummy_data import init_comprehensive_dummy_data
        init_comprehensive_dummy_data()
    except Exception as e:
        print(f"Note: Could not initialize dummy data: {e}")
    
    print("✓ Database initialized")
    
    yield
    
    # Shutdown
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI-Driven Debt Collection Agency Management Platform",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router)
app.include_router(case_routes.router)
app.include_router(dca_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(testing_routes.router)
app.include_router(customer_routes.router)
app.include_router(settings_routes.router)
app.include_router(report_routes.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs",
        "message": "Welcome to FedEx DCA Management Platform API"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
