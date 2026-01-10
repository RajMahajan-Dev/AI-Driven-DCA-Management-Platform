# FedEx SMART Hackathon – AI-Driven DCA Management Platform

## 🎯 Project Overview

An **enterprise-grade AI-driven Debt Collection Agency (DCA) Management Platform** built for the FedEx SMART Hackathon. This platform centralizes overdue case management, automates workflows with AI-powered decision-making, and provides real-time SLA tracking and escalation capabilities.

### Key Features

✅ **Centralized Case Management** - Unified view of all overdue cases  
✅ **AI-Powered Recovery Scoring** - Machine learning model predicts recovery probability  
✅ **Automated Workflow Engine** - Rule-based priority assignment and SLA calculation  
✅ **Smart DCA Allocation** - Performance-based automatic case assignment with debt range matching  
✅ **Real-time SLA Tracking** - Proactive breach detection and alerting  
✅ **Comprehensive Audit Trail** - Complete logging for compliance and tracking  
✅ **Role-Based Access Control** - Admin and internal user roles  
✅ **RESTful API Architecture** - Clean, versioned, documented APIs  
✅ **DCA Performance Tracking** - Dynamic scoring based on completion rate, time, and rejections  
✅ **Enhanced Data Collection** - Social media links, document uploads, web scraping support  
✅ **Testing Interface** - Dedicated page to simulate DCA responses and test workflows  

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│  - Dashboard  - Case Management  - DCA Management        │
│  - Audit Logs  - Authentication  - Real-time Updates     │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST API
┌────────────────────▼────────────────────────────────────┐
│               Backend API (FastAPI)                      │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────────┐ │
│  │  Auth        │  │ Workflow    │  │  AI/ML         │ │
│  │  (JWT)       │  │ Engine      │  │  Predictor     │ │
│  └──────────────┘  └─────────────┘  └────────────────┘ │
│  ┌──────────────────────────────────────────────────┐   │
│  │           Service Layer                           │   │
│  │  - Case Service  - DCA Service  - Audit Service  │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │ SQLAlchemy ORM
┌────────────────────▼────────────────────────────────────┐
│               PostgreSQL Database                        │
│  - Users  - Cases  - DCAs  - Audit Logs  - SLA Data     │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + TypeScript | Modern UI with type safety |
| **Backend** | Python 3.11 + FastAPI | High-performance async API |
| **Database** | PostgreSQL 15 | Reliable relational data storage |
| **ORM** | SQLAlchemy 2.0 | Database abstraction layer |
| **Auth** | JWT (python-jose) | Stateless authentication |
| **AI/ML** | scikit-learn | Machine learning models |
| **Deployment** | Docker + Docker Compose | Containerized deployment |

---

## 🤖 AI/ML Intelligence

### Recovery Probability Predictor

The platform uses a **Logistic Regression model** to predict debt recovery probability.

**Input Features:**
- Overdue Amount ($)
- Ageing Days (days overdue)

**Output:**
- Recovery Score (0-1 probability)

**Model Training:**
```python
# Synthetic training data for demonstration
# In production, this would use historical recovery data
X_train = [
    [5000, 15],    # Small amount, recent → 90% recovery
    [50000, 120],  # Large amount, old → 20% recovery
    ...
]
y_train = [1, 0, ...]  # 1 = recovered, 0 = not recovered

model = LogisticRegression()
model.fit(X_scaled, y_train)
```

**How It's Used:**
1. **Case Creation** - Score calculated automatically
2. **Priority Adjustment** - Higher scores may influence priority
3. **Dashboard Insights** - Aggregate recovery predictions
4. **DCA Performance** - Track actual vs predicted recovery

**Future Enhancements:**
- Additional features: customer payment history, industry, geography
- Deep learning models (neural networks)
- Real-time model retraining
- A/B testing of models
- Explainability (SHAP values)

---

## ⚙️ Workflow Engine

### Priority Calculation

**Rules:**
```
P1 (High):    Amount ≥ $50,000  OR  Ageing ≥ 90 days
P2 (Medium):  Amount ≥ $20,000  OR  Ageing ≥ 60 days
P3 (Low):     All other cases
```

### SLA Calculation

**SLA Deadlines:**
- **P1**: 3 days from creation
- **P2**: 7 days from creation
- **P3**: 14 days from creation

**SLA Status:**
- **On Track**: > 24 hours remaining
- **At Risk**: < 24 hours remaining
- **Breached**: Past due date

### Status Transitions

**Allowed Flows:**
```
Open → In Progress → Closed
     ↘ Closed
In Progress → Open (re-open)
```

**Validation:**
- Transitions are validated server-side
- Invalid transitions return error
- All transitions logged to audit trail

---

## 🏢 DCA Allocation System

### Allocation Rules

**High Priority (P1):**
- Assigned to **best performing DCA** (highest performance score)
- Ensures critical cases get best resources
- If score is "TBD", uses debt range and capacity matching

**Medium/Low Priority (P2/P3):**
- **Load balanced** across available DCAs
- Assigned to DCA with lowest active case count
- **Prefers new DCAs** for new cases (those with "TBD" score)
- **Debt range matching**: Only assigns if case amount is within DCA's min/max range

**Capacity Management:**
- DCAs have max capacity limit
- Cases only assigned if DCA has capacity
- Real-time active case count tracking

**Performance Score Calculation:**
When cases are completed, performance score is calculated dynamically:
- **Completion Rate** (40% weight): total_completed / (total_completed + total_rejected)
- **Time Factor** (30% weight): Based on average completion time
- **Rejection Factor** (30% weight): Based on rejection rate
- Initial score: "TBD" (To Be Determined)
- Score updates automatically after each case completion/rejection/delay

**Example:**
```python
# P1 Case
dca = select_best_performing_dca()  # Score: 92.1
reason = "High priority case assigned to best performing DCA"

# P2 Case
dca = select_least_loaded_dca()  # Active: 15/100
reason = "Load balanced to DCA with 15 active cases"
```

---

## 📊 Database Schema

### Core Tables

**Users**
- id, email, username, hashed_password
- role (admin, internal_user)
- is_active, created_at

**Cases**
- id, case_id, customer_name, customer_email, customer_phone
- customer_address (string)
- customer_social_media_instagram, customer_social_media_facebook, customer_social_media_linkedin
- customer_website_url, customer_document_url
- scraped_customer_data (JSON), family_info (text)
- overdue_amount, ageing_days
- status, priority, sla_status, sla_due_date
- ai_recovery_score
- dca_id, allocation_reason
- assigned_at, completed_at, confirmation_received (boolean)
- notes, created_at, updated_at

**DCAs (Debt Collection Agencies)**
- id, name, contact_person, email, phone
- performance_score (string: "TBD" or calculated score)
- total_cases_completed, total_cases_rejected, total_delays
- avg_completion_time_days (float)
- min_debt_amount, max_debt_amount (debt range)
- website_url, document_url, scraped_data (JSON)
- active_cases_count, max_capacity
- is_active, created_at

**Audit_Logs**
- id, user_id, case_id
- action_type, description
- old_value, new_value, timestamp

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Git

### Installation & Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd "fedx Competation Projects"
```

2. **Start all services**
```bash
docker-compose up --build
```

This will start:
- **PostgreSQL**: localhost:5432
- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:3000

3. **Access the application**
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

### Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**User Account:**
- Username: `user`
- Password: `user123`

### Sample Data

The system initializes with:
- 2 user accounts (admin + user)
- 6 pre-configured DCAs:
  - Swift Debt Solutions (Range: $50K-$500K, Score: TBD)
  - Premium Recovery Services (Range: $10K-$200K, Score: TBD)
  - Global Collections Inc (Range: $5K-$1M, Score: TBD)
  - Elite Recovery Partners (Range: $20K-$300K, Score: TBD) ⭐NEW
  - National Debt Specialists (Range: $1K-$100K, Score: TBD) ⭐NEW
  - Metro Collections Agency (Range: $15K-$250K, Score: TBD) ⭐NEW
- 12 comprehensive test cases with:
  - Real company data (Acme Corp, Tech Innovations, Global Traders, etc.)
  - Complete contact information and addresses
  - Social media profiles (Instagram, Facebook, LinkedIn)
  - Website URLs for data scraping
  - Various debt amounts ($21K - $178K)
  - Different ageing periods (32 - 165 days)
  - AI recovery scores
  - 8 cases pre-assigned to DCAs (preferring new DCAs)

---

## 📁 Project Structure

```
fedx Competation Projects/
├── docker-compose.yml
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py                 # FastAPI application
│   │   ├── config.py               # Configuration
│   │   ├── database.py             # Database connection
│   │   ├── models/
│   │   │   └── models.py           # SQLAlchemy models
│   │   ├── schemas/
│   │   │   └── schemas.py          # Pydantic schemas
│   │   ├── api/
│   │   │   ├── auth_routes.py      # Authentication endpoints
│   │   │   ├── case_routes.py      # Case management endpoints
│   │   │   ├── dca_routes.py       # DCA management endpoints
│   │   │   ├── dashboard_routes.py # Dashboard & audit endpoints
│   │   │   └── testing_routes.py   # Testing/simulation endpoints ⭐NEW
│   │   ├── auth/
│   │   │   └── auth.py             # JWT authentication
│   │   ├── workflows/
│   │   │   └── workflow_engine.py  # Business rules
│   │   ├── ai/
│   │   │   └── predictor.py        # ML model
│   │   ├── services/
│   │   │   ├── case_service.py     # Case business logic
│   │   │   └── dca_service.py      # DCA business logic
│   │   └── init_dummy_data.py      # Comprehensive dummy data ⭐NEW
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── tsconfig.json
    ├── public/
    │   └── index.html
    └── src/
        ├── index.tsx
        ├── App.tsx                 # Main application
        ├── App.css
        ├── services/
        │   └── api.ts              # API client
        ├── context/
        │   └── AuthContext.tsx     # Authentication context
        ├── components/
        │   ├── Layout.tsx          # Main layout
        │   └── Navbar.tsx          # Navigation bar
        └── pages/
            ├── Login.tsx           # Login page
            ├── Dashboard.tsx       # Dashboard
            ├── Cases.tsx           # Case list
            ├── CaseDetail.tsx      # Case details
            ├── CreateCase.tsx      # Create case form
            ├── DCAManagement.tsx   # DCA management
            ├── DCATestingPage.tsx  # DCA testing interface ⭐NEW
            └── AuditLog.tsx        # Audit log viewer
```

---

## 🔌 API Endpoints

### Authentication
```
POST   /api/v1/auth/register    # Register new user
POST   /api/v1/auth/login       # Login (get JWT token)
GET    /api/v1/auth/me          # Get current user info
```

### Cases
```
POST   /api/v1/cases/                    # Create case
GET    /api/v1/cases/                    # List cases (with filters)
GET    /api/v1/cases/{id}                # Get case details
PATCH  /api/v1/cases/{id}/status         # Update case status
POST   /api/v1/cases/{id}/escalate       # Escalate case
POST   /api/v1/cases/update-sla-statuses # Batch update SLA (admin)
```

### DCAs
```
POST   /api/v1/dcas/        # Create DCA (admin)
GET    /api/v1/dcas/        # List DCAs
GET    /api/v1/dcas/{id}    # Get DCA details
PATCH  /api/v1/dcas/{id}    # Update DCA (admin)
DELETE /api/v1/dcas/{id}    # Delete DCA (admin)
```

### Dashboard & Audit
```
GET    /api/v1/dashboard    # Get dashboard statistics
GET    /api/v1/audit-logs   # Get audit logs (with filters)
```

### Testing (DCA Simulation)
```
GET    /api/v1/testing/cases              # Get all cases for testing
POST   /api/v1/testing/update-status      # Update case status (simulate DCA response)
GET    /api/v1/testing/dcas               # Get all DCAs with performance metrics
POST   /api/v1/testing/simulate-rejection/{case_id}  # Simulate case rejection
POST   /api/v1/testing/simulate-delay/{case_id}      # Simulate case delay
```

**Full API Documentation**: http://localhost:8000/docs

---

## 👥 User Roles

### Admin
- Create/manage DCAs
- View all cases and audit logs
- Batch SLA updates
- Full system access

### Internal User
- View dashboard
- Create and manage cases
- View DCA information
- Trigger manual escalation
- View audit logs

---

## 🧪 Testing the System

### 1. Create a High-Priority Case

**Input:**
- Customer: "ABC Corporation"
- Amount: $75,000
- Ageing: 95 days

**Expected:**
- Priority: **P1** (amount > $50k, ageing > 90 days)
- SLA: 3 days
- AI Score: ~0.15 (low recovery probability)
- Assigned to: Best DCA (Swift Debt Solutions - 92.1%)

### 2. Create a Medium-Priority Case

**Input:**
- Customer: "XYZ Inc"
- Amount: $25,000
- Ageing: 45 days

**Expected:**
- Priority: **P2** (amount > $20k)
- SLA: 7 days
- AI Score: ~0.65 (moderate recovery)
- Assigned to: Load-balanced DCA

### 3. Test Status Workflow

**Valid:**
- Open → In Progress ✅
- In Progress → Closed ✅

**Invalid:**
- Closed → In Progress ❌ (returns error)

### 4. Test SLA Tracking

- Create case
- Wait or manually update timestamp
- Check SLA status changes: On Track → At Risk → Breached

---

## 📈 Future Enhancements

### Short Term
- [ ] Email/SMS notifications
- [ ] Advanced filtering and search
- [ ] Export to Excel/PDF
- [ ] Real-time WebSocket updates
- [ ] Case assignment to specific agents

### Medium Term
- [ ] External DCA portal
- [ ] Payment tracking integration
- [ ] Customer communication history
- [ ] Advanced analytics and reporting
- [ ] Mobile application

### Long Term
- [ ] Multi-tenant architecture
- [ ] Advanced AI models (deep learning)
- [ ] Predictive analytics dashboard
- [ ] Integration with ERP systems
- [ ] Blockchain-based audit trail
- [ ] Natural language processing for case notes

---

## ⭐ Enhanced Features (Latest Updates)

### 1. Dynamic DCA Performance Tracking
- **Performance Score**: Starts as "TBD" for new DCAs
- **Automatic Calculation**: Updates dynamically based on:
  - **Completion Rate** (40%): Percentage of cases successfully completed
  - **Time Efficiency** (30%): Average completion time in days
  - **Rejection Rate** (30%): How often cases are rejected
- **Metrics Dashboard**: Real-time tracking of:
  - Total cases completed
  - Total cases rejected
  - Total delays reported
  - Average completion time

### 2. Smart DCA Allocation
- **Debt Range Matching**: Each DCA has min/max debt amounts they specialize in
- **Prefer New DCAs**: System prioritizes assigning cases to DCAs with "TBD" scores
- **Intelligent Distribution**: Balances workload while respecting specialization

### 3. Enhanced Data Collection

**DCA Additional Parameters:**
- Website URL for data scraping
- Document upload capability (PDF links)
- Scraped data storage (JSON format)

**Case Additional Parameters:**
- Customer full address
- Social media links with hyperlinks:
  - Instagram profile
  - Facebook profile
  - LinkedIn profile
- Customer website URL
- Family member information
- Document upload capability
- Automated data scraping support

### 4. 🧪 DCA Testing Interface
**New Page**: `/testing`

**Features:**
- **DCA Performance Dashboard**: Grid view of all DCAs with live metrics
- **Case Management Table**: Filter cases by DCA, status, priority
- **Simulate DCA Actions**:
  - Start case processing (Open → In Progress)
  - Complete cases with confirmation
  - Reject cases (updates rejection metrics)
  - Report delays (tracks delay count)
- **Real-time Updates**: Performance scores recalculate automatically
- **Interactive UI**: Click DCA cards to filter cases, color-coded statuses

**Use Cases:**
- Test workflow automation
- Verify performance score calculations
- Simulate various DCA response scenarios
- Train staff on system behavior
- Demo platform capabilities

### 5. Comprehensive Dummy Data
- **12 Realistic Test Cases** with complete customer profiles
- **6 DCAs** (3 existing + 3 new) with varied debt ranges
- **Pre-assigned Cases**: 8 cases already distributed to DCAs
- **Full Social Media Integration**: Real-looking Instagram, Facebook, LinkedIn links
- **Diverse Scenarios**: Different priorities, amounts, ageing periods

---

## 🎓 Technical Highlights

### Backend
✅ **FastAPI** - Modern async Python framework  
✅ **SQLAlchemy 2.0** - Latest ORM features  
✅ **JWT Authentication** - Stateless security  
✅ **Pydantic** - Runtime type validation  
✅ **Clean Architecture** - Separation of concerns  
✅ **Dependency Injection** - Testable code  

### Frontend
✅ **React 18** - Latest React features  
✅ **TypeScript** - Type safety  
✅ **Context API** - State management  
✅ **React Router v6** - Client-side routing  
✅ **Axios Interceptors** - Automatic auth  
✅ **Responsive Design** - Mobile-friendly  

### DevOps
✅ **Docker Compose** - Multi-container orchestration  
✅ **Health Checks** - Service reliability  
✅ **Auto-restart** - High availability  
✅ **Volume Persistence** - Data retention  

---

## 📝 Development Notes

### Database Migrations

Currently using `Base.metadata.create_all()` for simplicity. For production:

```bash
# Install Alembic
pip install alembic

# Initialize
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### Environment Variables

Create `.env` files for configuration:

**backend/.env**
```env
DATABASE_URL=postgresql://dcauser:dcapass123@postgres:5432/dca_management
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

**frontend/.env**
```env
REACT_APP_API_URL=http://localhost:8000
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change ports in docker-compose.yml
ports:
  - "5433:5432"  # PostgreSQL
  - "8001:8000"  # Backend
  - "3001:3000"  # Frontend
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs postgres

# Restart services
docker-compose restart
```

### Frontend Can't Reach Backend
- Check CORS settings in `backend/app/main.py`
- Verify `REACT_APP_API_URL` in frontend

---

## 👨‍💻 Development Team

This project was developed as a comprehensive enterprise solution for the FedEx SMART Hackathon, demonstrating:
- Full-stack development expertise
- AI/ML integration capabilities
- Enterprise architecture design
- Clean code principles
- Production-ready practices

---

## 📄 License

This project is developed for the FedEx SMART Hackathon evaluation.

---

## 🎉 Conclusion

This platform demonstrates a **production-ready** approach to AI-driven debt collection management:

✅ **Scalable Architecture** - Clean separation of concerns  
✅ **AI Integration** - Real ML model (not stub)  
✅ **Enterprise Features** - Audit, RBAC, SLA tracking  
✅ **Developer Experience** - Docker, docs, clean code  
✅ **Business Value** - Automation, efficiency, insights  

**Ready for Demo** ✨  
**Ready for Evaluation** ✨  
**Ready for Enterprise** ✨
