#!/usr/bin/env python3

print("🔄 Starting debug script...")

try:
    print("📦 Importing database module...")
    from backend.core.database import Base, engine, SessionLocal
    from backend.core.database import HeadStatusModel, CompetitorModel
    print("✅ Database imports successful!")
    
    print("🔍 Testing database connection...")
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✅ Database connection successful!")
    
    print("🔨 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created!")
    
    print("👥 Adding heads...")
    db = SessionLocal()
    heads = ["PriceWatch", "JobSpy", "TechRadar", "SocialPulse", "PatentHawk", "AdTracker"]
    
    for head_name in heads:
        head = HeadStatusModel(
            head_name=head_name,
            status="inactive",
            discoveries_count=0,
            error_count=0,
            config={}
        )
        db.add(head)
        print(f"  ✅ Added head: {head_name}")
    
    print("🎯 Adding competitors...")
    sample_competitors = [
        {"domain": "competitor1.com", "company_name": "Competitor One"},
        {"domain": "competitor2.com", "company_name": "Competitor Two"},
        {"domain": "competitor3.com", "company_name": "Competitor Three"}
    ]
    
    for comp in sample_competitors:
        competitor = CompetitorModel(
            domain=comp["domain"],
            company_name=comp["company_name"],
            active=1,
            metadata={}
        )
        db.add(competitor)
        print(f"  ✅ Added competitor: {comp['company_name']}")
    
    db.commit()
    db.close()
    print("✅ Database initialization complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
