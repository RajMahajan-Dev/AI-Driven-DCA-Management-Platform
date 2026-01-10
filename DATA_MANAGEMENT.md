# Data Management Guide

## Overview
This project includes comprehensive tools for managing database data, including deleting all data and initializing fresh dummy data with proper relationships.

## Available Scripts

### 1. Python Script (Direct Execution)
Located at: `backend/reset_and_init_data.py`

**Usage:**
```bash
# Full reset (delete all + initialize fresh data)
docker-compose exec backend python reset_and_init_data.py --reset

# Delete all data only
docker-compose exec backend python reset_and_init_data.py --delete-all

# Initialize fresh data only (requires empty database)
docker-compose exec backend python reset_and_init_data.py --init
```

### 2. Interactive Scripts (Recommended)

#### For Windows PowerShell:
```powershell
.\manage_data.ps1
```

#### For Linux/Mac Bash:
```bash
chmod +x manage_data.sh
./manage_data.sh
```

These scripts provide an interactive menu with options:
1. Delete all data
2. Initialize fresh data
3. Full reset (delete + initialize)
4. Exit

## What Gets Created

### Users
- **Admin**: admin@fedex.com / admin123
- **Regular User**: user@fedex.com / user123

### DCAs (6 agencies)
1. **Swift Debt Solutions** - Capacity: 150, Range: $50K-$500K
2. **Premium Recovery Services** - Capacity: 100, Range: $10K-$200K
3. **Global Collections Inc** - Capacity: 150, Range: $5K-$1M
4. **Elite Recovery Partners** - Capacity: 120, Range: $20K-$300K
5. **National Debt Specialists** - Capacity: 200, Range: $1K-$100K
6. **Metro Collections Agency** - Capacity: 90, Range: $15K-$250K

### Cases (12 cases)
- All cases include complete customer information
- Social media links (Instagram, Facebook, LinkedIn)
- Website URLs where applicable
- Varied debt amounts and aging days
- **100% Assignment Guarantee**: All cases are automatically assigned to appropriate DCAs

## Assignment Logic

The script uses a 3-tier fallback system to ensure 100% case assignment:

1. **Tier 1**: Match by debt range and available capacity
2. **Tier 2**: Any DCA with available capacity
3. **Tier 3**: Expand capacity of largest DCA if all DCAs are full

## Features

✅ Deletes all audit logs, cases, and DCAs (preserves users for login)  
✅ Creates comprehensive dummy data with proper relationships  
✅ Ensures 100% case assignment (no unassigned cases)  
✅ Provides detailed logging with emoji indicators  
✅ Shows summary statistics after completion  
✅ Handles foreign key constraints properly  

## Testing Button Integration

The "Reset All Data" button in the Testing page now calls the same comprehensive initialization function, ensuring:
- All data is properly deleted
- Fresh data is created with correct relationships
- All cases are assigned to DCAs
- Performance scores start as "TBD"

## Safety Features

- **User Preservation**: Admin and user accounts are never deleted
- **Transaction Safety**: All operations are wrapped in database transactions
- **Error Handling**: Comprehensive error handling with rollback on failure
- **Foreign Key Management**: Deletes data in correct order to respect constraints

## Troubleshooting

If you encounter errors:

1. **Check container status**: `docker-compose ps`
2. **View backend logs**: `docker-compose logs backend --tail=50`
3. **Restart containers**: `docker-compose restart`
4. **Full rebuild**: `docker-compose down && docker-compose up --build -d`

## Example Output

```
============================================================
FedEx DCA Management - Data Management Script
============================================================

🔄 Performing FULL RESET...
🗑️  Deleting all existing data...
   ✓ Deleted all audit logs
   ✓ Deleted all cases
   ✓ Deleted all DCAs
✅ All data deleted successfully!

👥 Creating users...
   ✓ Admin user already exists
   ✓ Regular user already exists

🏢 Creating DCAs...
   ✓ Created DCA: Swift Debt Solutions
   ✓ Created DCA: Premium Recovery Services
   ✓ Created DCA: Global Collections Inc
   ✓ Created DCA: Elite Recovery Partners
   ✓ Created DCA: National Debt Specialists
   ✓ Created DCA: Metro Collections Agency

📊 Creating cases...
   ✓ Created 12 cases

🔗 Assigning cases to DCAs...
   ✓ Assigned 12/12 cases (100% assignment)
   ✅ All cases successfully assigned!

✅ FULL RESET COMPLETED SUCCESSFULLY!

============================================================
Summary:
  Users: 2
  DCAs: 6
  Cases: 12
  Assigned Cases: 12
============================================================
```

## Notes

- All timestamps use UTC timezone
- Performance scores start as "TBD" and update based on DCA actions
- Case aging and SLA dates are calculated from creation date
- Social media links and website URLs vary by case
- Some fields (like customer documents) are intentionally left null for realism
