"""
Script to initialize comprehensive dummy data for testing.
Run this after the database is created.
"""
from datetime import datetime, timedelta
import random

from app.database import SessionLocal
from app.models import User, DCA, Case, RoleEnum, CaseStatus, Priority, SLAStatus
from app.auth import get_password_hash


def init_comprehensive_dummy_data():
    """Initialize comprehensive dummy data for testing."""
    db = SessionLocal()
    
    try:
        # Skip if data exists
        if db.query(Case).count() > 0:
            print("Dummy data already exists, skipping...")
            return
        
        print("Initializing comprehensive dummy data...")
        
        # Get existing users and DCAs
        admin = db.query(User).filter(User.email == "admin@fedex.com").first()
        
        # Get DCAs
        dcas = db.query(DCA).all()
        
        if not dcas:
            print("No DCAs found. Please run init_sample_data first.")
            return
        
        # Update DCAs with new fields
        dca_configs = [
            {
                "name": "Swift Debt Solutions",
                "performance_score": "TBD",
                "min_debt": 50000,
                "max_debt": 500000,
                "website": "https://swiftdebt.com",
                "total_completed": 0,
                "total_rejected": 0,
                "total_delays": 0,
                "avg_time": 0.0
            },
            {
                "name": "Premium Recovery Services",
                "performance_score": "TBD",
                "min_debt": 10000,
                "max_debt": 200000,
                "website": "https://premiumrecovery.com",
                "total_completed": 0,
                "total_rejected": 0,
                "total_delays": 0,
                "avg_time": 0.0
            },
            {
                "name": "Global Collections Inc",
                "performance_score": "TBD",
                "min_debt": 5000,
                "max_debt": 1000000,
                "website": "https://globalcollections.com",
                "total_completed": 0,
                "total_rejected": 0,
                "total_delays": 0,
                "avg_time": 0.0
            }
        ]
        
        for dca in dcas:
            config = next((c for c in dca_configs if c["name"] == dca.name), None)
            if config:
                dca.performance_score = config["performance_score"]
                dca.min_debt_amount = config["min_debt"]
                dca.max_debt_amount = config["max_debt"]
                dca.website_url = config["website"]
                dca.total_cases_completed = config["total_completed"]
                dca.total_cases_rejected = config["total_rejected"]
                dca.total_delays = config["total_delays"]
                dca.avg_completion_time_days = config["avg_time"]
        
        # Add more DCAs
        new_dcas = [
            DCA(
                name="Elite Recovery Partners",
                contact_person="Jennifer Davis",
                email="jennifer@eliterecovery.com",
                phone="+1-555-0104",
                performance_score="TBD",
                max_capacity=120,
                min_debt_amount=20000,
                max_debt_amount=300000,
                website_url="https://eliterecovery.com",
                is_active=True
            ),
            DCA(
                name="National Debt Specialists",
                contact_person="Robert Wilson",
                email="robert@nationaldebt.com",
                phone="+1-555-0105",
                performance_score="TBD",
                max_capacity=200,
                min_debt_amount=1000,
                max_debt_amount=100000,
                website_url="https://nationaldebt.com",
                is_active=True
            ),
            DCA(
                name="Metro Collections Agency",
                contact_person="Lisa Anderson",
                email="lisa@metrocollections.com",
                phone="+1-555-0106",
                performance_score="TBD",
                max_capacity=90,
                min_debt_amount=15000,
                max_debt_amount=250000,
                website_url="https://metrocollections.com",
                is_active=True
            )
        ]
        
        for new_dca in new_dcas:
            db.add(new_dca)
        
        db.commit()
        
        # Refresh DCA list
        dcas = db.query(DCA).all()
        
        # Create comprehensive dummy cases
        customers = [
            {
                "name": "Acme Corporation",
                "email": "accounts@acmecorp.com",
                "phone": "+1-555-1001",
                "address": "123 Business St, New York, NY 10001",
                "website": "https://acmecorp.com",
                "instagram": "https://instagram.com/acmecorp",
                "linkedin": "https://linkedin.com/company/acmecorp",
                "amount": 75000,
                "ageing": 95
            },
            {
                "name": "Tech Innovations Ltd",
                "email": "finance@techinnovations.com",
                "phone": "+1-555-1002",
                "address": "456 Silicon Valley Blvd, San Francisco, CA 94105",
                "website": "https://techinnovations.com",
                "facebook": "https://facebook.com/techinnovations",
                "linkedin": "https://linkedin.com/company/techinnovations",
                "amount": 125000,
                "ageing": 120
            },
            {
                "name": "Global Traders Inc",
                "email": "ar@globaltraders.com",
                "phone": "+1-555-1003",
                "address": "789 Trade Center, Chicago, IL 60601",
                "instagram": "https://instagram.com/globaltraders",
                "amount": 45000,
                "ageing": 60
            },
            {
                "name": "Sunrise Manufacturing",
                "email": "billing@sunrisemfg.com",
                "phone": "+1-555-1004",
                "address": "321 Industrial Park, Detroit, MI 48201",
                "website": "https://sunrisemfg.com",
                "amount": 89000,
                "ageing": 105
            },
            {
                "name": "Metro Services Group",
                "email": "payments@metroservices.com",
                "phone": "+1-555-1005",
                "address": "654 Downtown Plaza, Boston, MA 02101",
                "linkedin": "https://linkedin.com/company/metroservices",
                "amount": 32000,
                "ageing": 45
            },
            {
                "name": "Coastal Enterprises",
                "email": "finance@coastalent.com",
                "phone": "+1-555-1006",
                "address": "987 Harbor View, Miami, FL 33101",
                "website": "https://coastalent.com",
                "facebook": "https://facebook.com/coastalent",
                "amount": 156000,
                "ageing": 150
            },
            {
                "name": "Peak Performance LLC",
                "email": "accounts@peakperformance.com",
                "phone": "+1-555-1007",
                "address": "147 Mountain Road, Denver, CO 80201",
                "instagram": "https://instagram.com/peakperf",
                "amount": 28000,
                "ageing": 38
            },
            {
                "name": "Urban Solutions Co",
                "email": "billing@urbansolutions.com",
                "phone": "+1-555-1008",
                "address": "258 City Center, Seattle, WA 98101",
                "website": "https://urbansolutions.com",
                "amount": 67000,
                "ageing": 78
            },
            {
                "name": "Precision Tools Inc",
                "email": "receivables@precisiontools.com",
                "phone": "+1-555-1009",
                "address": "369 Factory Lane, Pittsburgh, PA 15201",
                "linkedin": "https://linkedin.com/company/precisiontools",
                "amount": 94000,
                "ageing": 112
            },
            {
                "name": "Heritage Wholesale",
                "email": "finance@heritagewholesale.com",
                "phone": "+1-555-1010",
                "address": "741 Commerce Drive, Atlanta, GA 30301",
                "website": "https://heritagewholesale.com",
                "instagram": "https://instagram.com/heritagewholesale",
                "amount": 178000,
                "ageing": 165
            },
            {
                "name": "Valley Distribution",
                "email": "ar@valleydist.com",
                "phone": "+1-555-1011",
                "address": "852 Valley Road, Phoenix, AZ 85001",
                "amount": 21000,
                "ageing": 32
            },
            {
                "name": "Skyline Ventures",
                "email": "accounting@skylineventures.com",
                "phone": "+1-555-1012",
                "address": "963 Highrise Ave, Dallas, TX 75201",
                "facebook": "https://facebook.com/skylineventures",
                "linkedin": "https://linkedin.com/company/skylineventures",
                "amount": 52000,
                "ageing": 68
            }
        ]
        
        cases_created = []
        for idx, customer in enumerate(customers, 1):
            case_id = f"CASE-2026-{1000 + idx}"
            
            # Create case
            case = Case(
                case_id=case_id,
                customer_name=customer["name"],
                customer_email=customer.get("email"),
                customer_phone=customer.get("phone"),
                customer_address=customer.get("address"),
                customer_website_url=customer.get("website"),
                customer_social_media_instagram=customer.get("instagram"),
                customer_social_media_facebook=customer.get("facebook"),
                customer_social_media_linkedin=customer.get("linkedin"),
                overdue_amount=customer["amount"],
                ageing_days=customer["ageing"],
                status=CaseStatus.OPEN,
                created_at=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            
            # Calculate priority based on amount and ageing
            if customer["amount"] > 100000 or customer["ageing"] > 120:
                case.priority = Priority.P1
            elif customer["amount"] > 50000 or customer["ageing"] > 60:
                case.priority = Priority.P2
            else:
                case.priority = Priority.P3
            
            # Set SLA based on priority
            if case.priority == Priority.P1:
                case.sla_due_date = case.created_at + timedelta(days=3)
            elif case.priority == Priority.P2:
                case.sla_due_date = case.created_at + timedelta(days=7)
            else:
                case.sla_due_date = case.created_at + timedelta(days=14)
            
            # AI recovery score (simple calculation)
            normalized_amount = min(customer["amount"] / 200000, 1.0)
            normalized_ageing = min(customer["ageing"] / 180, 1.0)
            case.ai_recovery_score = max(0, 1 - (normalized_amount * 0.5 + normalized_ageing * 0.5))
            
            db.add(case)
            cases_created.append(case)
        
        db.commit()
        
        # Assign ALL cases to DCAs (prefer new DCAs for new cases)
        new_dca_names = ["Elite Recovery Partners", "National Debt Specialists", "Metro Collections Agency"]
        unassigned_cases = []
        
        for case in cases_created:  # Assign ALL cases
            # Find suitable DCA based on debt range and prefer new ones
            suitable_dcas = [
                dca for dca in dcas 
                if dca.min_debt_amount <= case.overdue_amount <= dca.max_debt_amount
                and dca.active_cases_count < dca.max_capacity
            ]
            
            if suitable_dcas:
                # Prefer new DCAs
                new_dcas_list = [dca for dca in suitable_dcas if dca.name in new_dca_names]
                selected_dca = random.choice(new_dcas_list if new_dcas_list else suitable_dcas)
                
                case.dca_id = selected_dca.id
                case.assigned_at = case.created_at + timedelta(hours=2)
                case.allocation_reason = f"Auto-assigned based on debt range ${selected_dca.min_debt_amount:,.0f}-${selected_dca.max_debt_amount:,.0f}"
                selected_dca.active_cases_count += 1
                
                # Simulate some completed cases
                if random.random() > 0.6:
                    case.status = CaseStatus.IN_PROGRESS
            else:
                # If no suitable DCA based on debt range, find any available DCA
                available_dcas = [dca for dca in dcas if dca.active_cases_count < dca.max_capacity]
                if available_dcas:
                    # Sort by available capacity (most available first)
                    available_dcas.sort(key=lambda x: x.max_capacity - x.active_cases_count, reverse=True)
                    selected_dca = available_dcas[0]
                    
                    case.dca_id = selected_dca.id
                    case.assigned_at = case.created_at + timedelta(hours=2)
                    case.allocation_reason = f"Assigned to {selected_dca.name} (best available)"
                    selected_dca.active_cases_count += 1
                    if random.random() > 0.6:
                        case.status = CaseStatus.IN_PROGRESS
                else:
                    # Absolutely no capacity - increase capacity of best DCA
                    best_dca = max(dcas, key=lambda x: x.max_capacity)
                    best_dca.max_capacity += 10
                    case.dca_id = best_dca.id
                    case.assigned_at = case.created_at + timedelta(hours=2)
                    case.allocation_reason = f"Assigned to {best_dca.name} (capacity expanded)"
                    best_dca.active_cases_count += 1
                    if random.random() > 0.6:
                        case.status = CaseStatus.IN_PROGRESS
                    
        db.commit()
        
        assigned_count = len([c for c in cases_created if c.dca_id])
        print(f"✓ Created {len(customers)} dummy cases")
        print(f"✓ Assigned {assigned_count}/{len(cases_created)} cases to DCAs (100% assignment)")
        print(f"✓ Created {len(new_dcas)} additional DCAs")
        print(f"✓ Comprehensive dummy data initialized successfully")
        
    except Exception as e:
        print(f"Error initializing dummy data: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_comprehensive_dummy_data()
