from backend.core.database import Base, engine, SessionLocal
from backend.core.database import HeadStatusModel, CompetitorModel
import sys

def init_database():
    """Initialize database with default data"""
    
    print("🔄 Starting database initialization...")
    
    try:
        # Test database connection
        print("🔍 Testing database connection...")
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ Database connection successful!")
        
        # Create all tables
        print("🔨 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        # Add default heads
        print("👥 Adding default HYDRA heads...")
        db = SessionLocal()
        
        heads = ["PriceWatch", "JobSpy", "TechRadar", "SocialPulse", "PatentHawk", "AdTracker"]
        
        for head_name in heads:
            existing = db.query(HeadStatusModel).filter(
                HeadStatusModel.head_name == head_name
            ).first()
            
            if not existing:
                head = HeadStatusModel(
                    head_name=head_name,
                    status="inactive",
                    discoveries_count=0,
                    error_count=0,
                    config={}
                )
                db.add(head)
                print(f"  ✅ Added head: {head_name}")
            else:
                print(f"  ⏭️  Head already exists: {head_name}")
        
        # Add sample competitors
        print("🎯 Adding sample competitors...")
        sample_competitors = [
            {"domain": "competitor1.com", "company_name": "Competitor One"},
            {"domain": "competitor2.com", "company_name": "Competitor Two"},
            {"domain": "competitor3.com", "company_name": "Competitor Three"}
        ]
        
        for comp in sample_competitors:
            existing = db.query(CompetitorModel).filter(
                CompetitorModel.domain == comp["domain"]
            ).first()
            
            if not existing:
                competitor = CompetitorModel(
                    domain=comp["domain"],
                    company_name=comp["company_name"],
                    active=1,
                    metadata={}
                )
                db.add(competitor)
                print(f"  ✅ Added competitor: {comp['company_name']}")
            else:
                print(f"  ⏭️  Competitor already exists: {comp['company_name']}")
        
        db.commit()
        db.close()
        
        print("✅ Database initialized successfully!")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Docker Desktop is running")
        print("2. Start PostgreSQL: docker run -d --name hydra-db -e POSTGRES_PASSWORD=hydra123 -e POSTGRES_DB=hydra -p 5432:5432 postgres:15")
        print("3. Check your .env file has correct DATABASE_URL")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
