#!/usr/bin/env python3
"""
Data Management Script for FedEx DCA Management Platform
This script can:
1. Delete all data from the database
2. Initialize fresh dummy data with proper relationships
3. Ensure all cases are assigned to DCAs

Usage:
    python reset_and_init_data.py --delete-all
    python reset_and_init_data.py --init
    python reset_and_init_data.py --reset  (delete + init)
"""

import sys
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, engine
from app.models import User, Case, DCA, CaseStatus, SLAStatus, Priority
from app.models.models import AuditLog
from app.auth import get_password_hash
from app.config import settings
from datetime import datetime, timedelta, timezone
import random


def delete_all_data(session):
    """Delete all data from the database."""
    print("🗑️  Deleting all existing data...")
    try:
        # Delete in order to respect foreign keys
        # First delete audit_logs that reference cases
        session.query(AuditLog).delete()
        print("   ✓ Deleted all audit logs")
        
        # Then delete cases
        session.query(Case).delete()
        print("   ✓ Deleted all cases")
        
        # Then delete DCAs
        session.query(DCA).delete()
        print("   ✓ Deleted all DCAs")
        
        # Don't delete users to keep admin login working
        # session.query(User).delete()
        
        session.commit()
        print("✅ All data deleted successfully!")
        return True
    except Exception as e:
        session.rollback()
        print(f"❌ Error deleting data: {e}")
        return False


def init_users(session):
    """Initialize admin and user accounts."""
    print("\n👥 Creating users...")
    
    # Check if admin exists
    existing_admin = session.query(User).filter(User.email == "admin@fedex.com").first()
    if not existing_admin:
        admin = User(
            email="admin@fedex.com",
            hashed_password=get_password_hash("admin123"),
            is_admin=True,
            is_active=True
        )
        session.add(admin)
        print("   ✓ Created admin user")
    else:
        print("   ✓ Admin user already exists")
    
    # Check if regular user exists
    existing_user = session.query(User).filter(User.email == "user@fedex.com").first()
    if not existing_user:
        user = User(
            email="user@fedex.com",
            hashed_password=get_password_hash("user123"),
            is_admin=False,
            is_active=True
        )
        session.add(user)
        print("   ✓ Created regular user")
    else:
        print("   ✓ Regular user already exists")
    
    session.commit()


def init_dcas(session):
    """Initialize DCAs with proper configuration."""
    print("\n🏢 Creating DCAs...")
    
    dcas_config = [
        {
            "name": "Swift Debt Solutions",
            "contact": "John Doe",
            "email": "john@swiftdebt.com",
            "phone": "+1-555-0100",
            "capacity": 150,
            "min_debt": 50000,
            "max_debt": 500000,
            "website": "https://swiftdebt.com"
        },
        {
            "name": "Premium Recovery Services",
            "contact": "John Smith",
            "email": "john@premiumrecovery.com",
            "phone": "+1-555-0101",
            "capacity": 100,
            "min_debt": 10000,
            "max_debt": 200000,
            "website": "https://premiumrecovery.com"
        },
        {
            "name": "Global Collections Inc",
            "contact": "Sarah Johnson",
            "email": "sarah@globalcollections.com",
            "phone": "+1-555-0102",
            "capacity": 150,
            "min_debt": 5000,
            "max_debt": 1000000,
            "website": "https://globalcollections.com"
        },
        {
            "name": "Elite Recovery Partners",
            "contact": "Jennifer Davis",
            "email": "jennifer@eliterecovery.com",
            "phone": "+1-555-0104",
            "capacity": 120,
            "min_debt": 20000,
            "max_debt": 300000,
            "website": "https://eliterecovery.com"
        },
        {
            "name": "National Debt Specialists",
            "contact": "Robert Wilson",
            "email": "robert@nationaldebt.com",
            "phone": "+1-555-0105",
            "capacity": 200,
            "min_debt": 1000,
            "max_debt": 100000,
            "website": "https://nationaldebt.com"
        },
        {
            "name": "Metro Collections Agency",
            "contact": "Lisa Anderson",
            "email": "lisa@metrocollections.com",
            "phone": "+1-555-0106",
            "capacity": 90,
            "min_debt": 15000,
            "max_debt": 250000,
            "website": "https://metrocollections.com"
        }
    ]
    
    created_dcas = []
    for config in dcas_config:
        dca = DCA(
            name=config["name"],
            contact_person=config["contact"],
            email=config["email"],
            phone=config["phone"],
            performance_score="TBD",
            max_capacity=config["capacity"],
            min_debt_amount=config["min_debt"],
            max_debt_amount=config["max_debt"],
            website_url=config["website"],
            is_active=True,
            active_cases_count=0,
            total_cases_completed=0,
            total_cases_rejected=0,
            total_delays=0,
            avg_completion_time_days=0.0
        )
        session.add(dca)
        created_dcas.append(dca)
        print(f"   ✓ Created DCA: {config['name']}")
    
    session.commit()
    return created_dcas


def init_cases(session, dcas):
    """Initialize cases with proper relationships to DCAs."""
    print("\n📋 Creating cases...")
    
    customers_config = [
        {"name": "Acme Corporation", "email": "accounts@acmecorp.com", "phone": "+1-555-1001",
         "address": "123 Business St, New York, NY 10001", "amount": 75000, "ageing": 95,
         "website": "https://acmecorp.com", "instagram": "https://instagram.com/acmecorp",
         "linkedin": "https://linkedin.com/company/acmecorp"},
        
        {"name": "Tech Innovations Ltd", "email": "finance@techinnovations.com", "phone": "+1-555-1002",
         "address": "456 Silicon Valley Blvd, San Francisco, CA 94105", "amount": 125000, "ageing": 120,
         "website": "https://techinnovations.com", "facebook": "https://facebook.com/techinnovations",
         "linkedin": "https://linkedin.com/company/techinnovations"},
        
        {"name": "Global Manufacturing Co", "email": "ar@globalmfg.com", "phone": "+1-555-1003",
         "address": "789 Industrial Parkway, Chicago, IL 60601", "amount": 45000, "ageing": 65,
         "website": "https://globalmfg.com", "instagram": "https://instagram.com/globalmfg"},
        
        {"name": "Retail Solutions Inc", "email": "payments@retailsolutions.com", "phone": "+1-555-1004",
         "address": "321 Commerce Ave, Los Angeles, CA 90001", "amount": 89000, "ageing": 88,
         "website": "https://retailsolutions.com", "linkedin": "https://linkedin.com/company/retail-solutions"},
        
        {"name": "Healthcare Systems LLC", "email": "billing@healthcaresys.com", "phone": "+1-555-1005",
         "address": "654 Medical Plaza, Boston, MA 02101", "amount": 178000, "ageing": 145,
         "website": "https://healthcaresys.com", "facebook": "https://facebook.com/healthcaresystems"},
        
        {"name": "Construction Builders", "email": "finance@constructionbuilders.com", "phone": "+1-555-1006",
         "address": "987 Builder's Road, Houston, TX 77001", "amount": 210000, "ageing": 165,
         "instagram": "https://instagram.com/construction_builders"},
        
        {"name": "Digital Marketing Pro", "email": "admin@digitalmarketingpro.com", "phone": "+1-555-1007",
         "address": "147 Creative Blvd, Austin, TX 78701", "amount": 32000, "ageing": 55,
         "website": "https://digitalmarketingpro.com"},
        
        {"name": "Food Services Group", "email": "accounts@foodservicesgroup.com", "phone": "+1-555-1008",
         "address": "258 Culinary Way, Miami, FL 33101", "amount": 67000, "ageing": 75,
         "linkedin": "https://linkedin.com/company/food-services-group"},
        
        {"name": "Auto Parts Distributors", "email": "payments@autoparts.com", "phone": "+1-555-1009",
         "address": "369 Motor Ave, Detroit, MI 48201", "amount": 95000, "ageing": 102,
         "website": "https://autopartsdist.com", "facebook": "https://facebook.com/autopartsdist"},
        
        {"name": "Legal Services LLP", "email": "billing@legalservices.com", "phone": "+1-555-1010",
         "address": "741 Justice Drive, Washington, DC 20001", "amount": 156000, "ageing": 135,
         "linkedin": "https://linkedin.com/company/legal-services-llp"},
        
        {"name": "Education Tech Corp", "email": "finance@edutech.com", "phone": "+1-555-1011",
         "address": "852 Learning Lane, Seattle, WA 98101", "amount": 52000, "ageing": 68,
         "website": "https://edutech.com", "instagram": "https://instagram.com/edutech"},
        
        {"name": "Logistics Express", "email": "ar@logisticsexpress.com", "phone": "+1-555-1012",
         "address": "963 Transport Blvd, Memphis, TN 38101", "amount": 21000, "ageing": 32,
         "facebook": "https://facebook.com/logisticsexpress"}
    ]
    
    created_cases = []
    case_number = 1
    
    for config in customers_config:
        # Calculate priority based on amount and ageing
        amount = config["amount"]
        ageing = config["ageing"]
        
        if amount > 100000 or ageing > 120:
            priority = Priority.P1
            sla_days = 3
        elif amount > 50000 or ageing > 60:
            priority = Priority.P2
            sla_days = 7
        else:
            priority = Priority.P3
            sla_days = 14
        
        # Calculate AI recovery score (simplified)
        normalized_amount = min(amount / 200000, 1.0)
        normalized_ageing = min(ageing / 180, 1.0)
        ai_score = max(0, 1 - (normalized_amount * 0.5 + normalized_ageing * 0.5))
        
        # Create case
        created_at = datetime.now(timezone.utc) - timedelta(days=ageing)
        
        case = Case(
            case_id=f"CASE-2026-{case_number:06d}",
            customer_name=config["name"],
            customer_email=config["email"],
            customer_phone=config["phone"],
            customer_address=config.get("address", ""),
            customer_website_url=config.get("website", ""),
            customer_social_media_instagram=config.get("instagram", ""),
            customer_social_media_facebook=config.get("facebook", ""),
            customer_social_media_linkedin=config.get("linkedin", ""),
            overdue_amount=amount,
            ageing_days=ageing,
            priority=priority,
            status=CaseStatus.OPEN,
            sla_due_date=datetime.now(timezone.utc) + timedelta(days=sla_days),
            sla_status=SLAStatus.ON_TRACK,
            ai_recovery_score=ai_score,
            created_at=created_at,
            notes=f"Case created on {created_at.strftime('%Y-%m-%d')}"
        )
        
        session.add(case)
        created_cases.append(case)
        case_number += 1
    
    session.commit()
    print(f"   ✓ Created {len(created_cases)} cases")
    return created_cases


def assign_cases_to_dcas(session, cases, dcas):
    """Assign all cases to appropriate DCAs with 100% assignment guarantee."""
    print("\n🔗 Assigning cases to DCAs...")
    
    assigned_count = 0
    
    for case in cases:
        # Find suitable DCAs based on debt range
        suitable_dcas = [
            dca for dca in dcas
            if dca.min_debt_amount <= case.overdue_amount <= dca.max_debt_amount
            and dca.active_cases_count < dca.max_capacity
        ]
        
        if suitable_dcas:
            # Pick the DCA with most available capacity
            selected_dca = max(suitable_dcas, key=lambda x: x.max_capacity - x.active_cases_count)
        else:
            # No suitable DCA by debt range, pick any with capacity
            available_dcas = [dca for dca in dcas if dca.active_cases_count < dca.max_capacity]
            if available_dcas:
                selected_dca = max(available_dcas, key=lambda x: x.max_capacity - x.active_cases_count)
            else:
                # All full - expand capacity of largest DCA
                selected_dca = max(dcas, key=lambda x: x.max_capacity)
                selected_dca.max_capacity += 10
                print(f"   ⚠️  Expanded capacity of {selected_dca.name} to {selected_dca.max_capacity}")
        
        # Assign case to DCA
        case.dca_id = selected_dca.id
        case.assigned_at = case.created_at + timedelta(hours=2)
        case.allocation_reason = f"Assigned to {selected_dca.name} based on capacity and debt range"
        selected_dca.active_cases_count += 1
        assigned_count += 1
        
        # Simulate some cases in progress
        if random.random() > 0.6:
            case.status = CaseStatus.IN_PROGRESS
    
    session.commit()
    print(f"   ✓ Assigned {assigned_count}/{len(cases)} cases (100% assignment)")
    
    # Verify no unassigned cases
    unassigned = session.query(Case).filter(Case.dca_id == None).count()
    if unassigned > 0:
        print(f"   ⚠️  Warning: {unassigned} cases remain unassigned")
    else:
        print("   ✅ All cases successfully assigned!")


def main():
    parser = argparse.ArgumentParser(description='Data Management Script')
    parser.add_argument('--delete-all', action='store_true', help='Delete all data')
    parser.add_argument('--init', action='store_true', help='Initialize fresh data')
    parser.add_argument('--reset', action='store_true', help='Delete and reinitialize (full reset)')
    
    args = parser.parse_args()
    
    if not (args.delete_all or args.init or args.reset):
        parser.print_help()
        return
    
    print("=" * 60)
    print("FedEx DCA Management - Data Management Script")
    print("=" * 60)
    
    # Use existing database engine from app.database
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        if args.reset:
            # Full reset: delete + init
            print("\n🔄 Performing FULL RESET...")
            delete_all_data(session)
            init_users(session)
            dcas = init_dcas(session)
            cases = init_cases(session, dcas)
            assign_cases_to_dcas(session, cases, dcas)
            print("\n✅ FULL RESET COMPLETED SUCCESSFULLY!")
            
        elif args.delete_all:
            # Just delete
            delete_all_data(session)
            print("\n✅ DATA DELETION COMPLETED!")
            
        elif args.init:
            # Just initialize
            print("\n🚀 Initializing data...")
            init_users(session)
            dcas = init_dcas(session)
            cases = init_cases(session, dcas)
            assign_cases_to_dcas(session, cases, dcas)
            print("\n✅ DATA INITIALIZATION COMPLETED!")
        
        print("\n" + "=" * 60)
        print("Summary:")
        print(f"  Users: {session.query(User).count()}")
        print(f"  DCAs: {session.query(DCA).count()}")
        print(f"  Cases: {session.query(Case).count()}")
        print(f"  Assigned Cases: {session.query(Case).filter(Case.dca_id != None).count()}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    main()
