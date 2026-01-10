# FedEx DCA Management Platform - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Start the Application
```bash
cd "fedx Competation Projects"
docker-compose up --build
```

Wait for all services to start (approximately 2-3 minutes).

### Step 2: Access the Application

**Frontend (Main Application):**
- Open browser: http://localhost:4567
- Login with: `admin@fedex.com` / `admin123`

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Step 3: Test the Platform

#### Create Your First Case
1. Navigate to "Cases" in the top menu
2. Click "Create New Case"
3. Fill in sample data:
   - Customer: "Test Corporation"
   - Email: "test@example.com"
   - Amount: $35,000
   - Ageing: 75 days
4. Click "Create Case"

**What Happens Automatically:**
- ✅ Priority calculated (P2 - medium priority)
- ✅ SLA due date set (7 days)
- ✅ AI recovery score predicted (~0.45)
- ✅ DCA allocated automatically
- ✅ Audit log created

#### View Dashboard
- Navigate to "Dashboard"
- See real-time statistics
- Monitor SLA status

#### Manage Case
1. Go to "Cases" and click on your case
2. Click "Move to In Progress"
3. Add notes if needed
4. Try "Escalate Case" button

#### View Audit Trail
- Navigate to "Audit Log"
- See all actions logged with timestamps

---

## 🎯 Demo Flow for Judges

### Scenario 1: High-Priority Case
**Input:**
- Customer: "Major Client Inc"
- Amount: $85,000
- Ageing: 100 days

**Expected Results:**
- Priority: P1 (High)
- SLA: 3 days
- AI Score: ~0.12 (low recovery probability)
- Assigned to: Swift Debt Solutions (best performing DCA at 92.1%)

### Scenario 2: Load Balancing
Create multiple P2/P3 cases and observe:
- Cases distributed across DCAs
- Active case counts update
- Load balancing in action

### Scenario 3: Workflow Validation
- Try invalid status transition (e.g., Closed → Open)
- See validation error returned
- Observe audit log captures failed attempt

---

## 🔑 Credentials

**Admin (Full Access):**
- Email: `admin@fedex.com`
- Password: `admin123`
- Can create/manage DCAs, view all logs

**Internal User:**
- Email: `user@fedex.com`
- Password: `user123`
- Can manage cases, view dashboards

**Customer Portal Access:**
- Go to: http://localhost:4567/customer-login
- Enter any customer email from test cases (e.g., `accounts@acmecorp.com`)
- Access individual case dashboards
- Available actions: Pay Now, Register Complaint, Update Info, File Grievance

---

## 📊 Pre-loaded Data

### Users
- 1 Admin user
- 1 Internal user

### DCAs (Debt Collection Agencies)
- **Swift Debt Solutions** - Performance: TBD, Range: $50K-$500K
- **Premium Recovery Services** - Performance: TBD, Range: $10K-$200K  
- **Global Collections Inc** - Performance: TBD, Range: $5K-$1M
- **Elite Recovery Partners** - Performance: TBD, Range: $20K-$300K
- **National Debt Specialists** - Performance: TBD, Range: $1K-$100K
- **Metro Collections Agency** - Performance: TBD, Range: $15K-$250K

### Cases
- **12 Comprehensive Test Cases** with:
  - Customer addresses, social media links (Instagram, Facebook, LinkedIn)
  - Website URLs for data scraping
  - Various debt amounts ($21K - $178K)
  - Different ageing periods (32 - 165 days)
  - AI recovery scores
  - Some pre-assigned to DCAs (preferring new DCAs)

---

## 🛠️ Tech Stack at a Glance

- **Backend:** Python + FastAPI
- **Frontend:** React + TypeScript
- **Database:** PostgreSQL
- **AI/ML:** scikit-learn (Logistic Regression)
- **Deployment:** Docker Compose

---

## 🐛 Quick Troubleshooting

### Services not starting?
```bash
# Stop all containers
docker-compose down

# Remove volumes and restart
docker-compose down -v
docker-compose up --build
```

### Frontend can't connect to backend?
- Check both services are running: `docker-compose ps`
- Backend should be at: http://localhost:8000
- Check browser console for errors

### Database connection errors?
```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

---

## 📱 Key Pages

1. **Login** (`/login`) - JWT authentication for admin/staff
2. **Customer Login** (`/customer-login`) - Email-based customer access ⭐NEW
3. **Customer Dashboard** (`/customer/dashboard/:caseId`) - Customer case management ⭐NEW
4. **Dashboard** (`/dashboard`) - Statistics and KPIs
5. **Cases** (`/cases`) - List and filter cases
6. **Case Detail** (`/cases/:id`) - Full case information
7. **Create Case** (`/cases/create`) - New case form with social media links
8. **DCA Management** (`/dcas`) - Manage agencies with performance metrics
9. **Audit Log** (`/audit-logs`) - Complete audit trail
10. **🧪 Testing** (`/testing`) - DCA testing interface with Reset All Data button ⭐UPDATED

---

## 🎓 Key Features to Demonstrate

### 1. DCA Assignment Options ⭐NEW
- **AI Auto-Assign (Default)**:
  - System automatically selects best DCA
  - Based on performance score, capacity, and debt range
  - Smart load balancing
- **Manual Selection**:
  - Admin can choose specific DCA
  - Dropdown shows performance and capacity
  - Override AI recommendation when needed

### 2. Testing Interface Enhancements ⭐NEW
- **Reset All Data Button**: 
  - One-click reset of all dummy data
  - Reinitializes cases and DCAs
  - Perfect for demo scenarios
- **All Cases Assigned**: No unassigned cases in dummy data
- **Improved Button Layout**: Fixed overlapping action buttons

### 2. Testing Interface Enhancements ⭐NEW
- **Reset All Data Button**: 
  - One-click reset of all dummy data
  - Reinitializes cases and DCAs
  - Perfect for demo scenarios
- **All Cases Assigned**: No unassigned cases in dummy data
- **Improved Button Layout**: Fixed overlapping action buttons

### 3. AI Intelligence
- Show AI recovery score calculation
- Explain how it uses amount + ageing
- Mention production would use more features

### 4. Workflow Automation
- Priority auto-calculated
- SLA auto-set based on priority
- Status transition validation

### 5. Smart Allocation
- P1 → Best performing DCA
- P2/P3 → Load balanced
- Prefer new DCAs for new cases
- Debt range matching ($min - $max)
- Capacity management

### 6. Enterprise Features
- Role-based access control
- Complete audit trail
- RESTful API design
- Real-time SLA tracking

### 7. DCA Performance Tracking ⭐NEW
- **Performance Score**: Initially "TBD", calculated dynamically based on:
  - Completion rate (40% weight)
  - Average completion time (30% weight)
  - Rejection rate (30% weight)
- **Metrics Tracked**:
  - Total cases completed
  - Total cases rejected
  - Total delays
  - Average completion time in days
- **Debt Collection Range**: Each DCA has min/max debt amounts they handle

### 8. Enhanced Data Collection ⭐NEW
- **DCA Additional Parameters**:
  - Website URL for data scraping
  - Document upload capability
  - Extracted meaningful info storage
  
- **Case Additional Parameters**:
  - Customer address
  - Social media links (Instagram, Facebook, LinkedIn)
  - Customer website URL
  - Family member information
  - Document upload capability
  - Hyperlinks for easy access to social profiles

### 9. DCA Testing Interface ⭐NEW
- Dedicated testing page at `/testing`
- Simulate DCA responses:
  - Start case processing
  - Complete cases with confirmation
  - Reject cases
  - Report delays
- Real-time performance score updates
- Filter cases by DCA
- View comprehensive DCA metrics
- **🔄 Reset All Data button** for quick testing ⭐NEW

### 10. Customer Portal ⭐NEW
- **Separate login at `/customer-login`**
- Email-based case lookup (no password needed)
- Customer-specific dashboard per case
- **Available Actions**:
  - 💳 **Pay Now** - Submit payment requests
  - 📢 **Register Complaint** - Log complaints for admin review
  - ✏️ **Update Information** - Request profile updates (requires admin approval)
  - ⚖️ **File Grievance** - Submit formal grievances
- Real-time case status tracking
- No access to admin features (DCA management, testing, etc.)
- Beautiful modal-based interface

---

## 📖 API Testing with Swagger

1. Go to http://localhost:8000/docs
2. Click "Authorize" button
3. Login to get token:
   - POST `/api/v1/auth/login`
   - Use form: `username=admin&password=admin123`
   - Copy the `access_token`
4. Click "Authorize" and paste token
5. Now you can test all endpoints!

**Try These:**
- `GET /api/v1/dashboard` - Dashboard stats
- `GET /api/v1/cases/` - List all cases
- `POST /api/v1/cases/` - Create new case

---

## ⏱️ Estimated Demo Time

- **Setup:** 2-3 minutes
- **Case Creation Demo:** 3-5 minutes
- **Feature Walkthrough:** 5-10 minutes
- **AI Explanation:** 3-5 minutes
- **Q&A:** 5-10 minutes

**Total:** 20-30 minutes

---

## 🎯 Evaluation Checklist

✅ **Working Application** - Runs end-to-end  
✅ **GitHub Repository** - Clean, documented code  
✅ **PPT Alignment** - Architecture matches slides  
✅ **AI Integration** - Real ML model (not stub)  
✅ **Scalability** - Enterprise-ready architecture  
✅ **Code Quality** - Clean, maintainable, tested  
✅ **Documentation** - Comprehensive README  
✅ **Innovation** - AI-driven automation  

---

## 📞 Support

For issues or questions during evaluation:
- Check README.md for detailed docs
- Review API docs at /docs endpoint
- Inspect Docker logs: `docker-compose logs`

---

**Good luck with your evaluation! 🚀**
