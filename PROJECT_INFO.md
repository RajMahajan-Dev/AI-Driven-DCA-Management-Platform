# FedEx DCA Management Platform - Detailed Project Information

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [What Problem Does It Solve?](#what-problem-does-it-solve)
3. [Key Features](#key-features)
4. [User Roles & Capabilities](#user-roles--capabilities)
5. [Getting Started](#getting-started)
6. [User Guides](#user-guides)
7. [Feature Walkthroughs](#feature-walkthroughs)
8. [Performance Scoring Explained](#performance-scoring-explained)
9. [SLA Management Explained](#sla-management-explained)
10. [AI-Powered Features](#ai-powered-features)
11. [Reports & Analytics](#reports--analytics)
12. [Customization & Settings](#customization--settings)
13. [Frequently Asked Questions](#frequently-asked-questions)
14. [Troubleshooting Guide](#troubleshooting-guide)
15. [Best Practices](#best-practices)

---

## Project Overview

### What Is This Platform?

The **FedEx DCA Management Platform** is a comprehensive web-based solution designed to streamline the management of **Debt Collection Agencies (DCAs)** and their assigned debt recovery cases. Built with modern technologies (React, FastAPI, PostgreSQL), this platform automates case assignment, tracks performance metrics, monitors SLAs, and provides powerful analytics tools.

### Who Is It For?

- **Collection Managers**: Oversee multiple DCAs, monitor performance, assign cases
- **System Administrators**: Configure platform settings, manage users, view audit logs
- **DCA Representatives**: View assigned cases, update statuses, track their performance
- **Customers**: Self-service portal to track their case status and payment progress

### Technology Highlights

- ⚡ **Fast & Responsive**: React-based modern UI with real-time updates
- 🤖 **AI-Powered**: Intelligent case assignment based on ML predictions
- 📊 **Rich Analytics**: Interactive charts and comprehensive reporting
- 🔒 **Secure**: JWT authentication, role-based access control, encrypted data
- 🐳 **Easy Deployment**: Containerized with Docker for quick setup
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

---

## What Problem Does It Solve?

### Before This Platform

**Manual Case Assignment:**
- Collection managers manually assign cases to DCAs
- No visibility into DCA capacity or performance
- Cases assigned based on gut feeling, not data
- High risk of overloading some DCAs while others are underutilized

**No Performance Tracking:**
- No standardized way to measure DCA effectiveness
- Difficult to identify top performers vs. underperformers
- No accountability for delays, rejections, or SLA breaches

**SLA Management Chaos:**
- Manual tracking of due dates across multiple systems
- No automated alerts for at-risk cases
- SLA breaches discovered too late

**Limited Reporting:**
- Manual report generation takes hours or days
- Data scattered across spreadsheets and emails
- No real-time insights into collection performance

### After This Platform

✅ **Automated Smart Assignment**: AI analyzes debt amount, DCA capacity, performance history, and debt range to assign cases optimally

✅ **Real-Time Performance Tracking**: Automatic scoring based on completion time, rejections, delays, and SLA compliance

✅ **Proactive SLA Management**: Priority-based SLAs (P1: 3 days, P2: 7 days, P3: 14 days) with automatic status updates and visual indicators

✅ **Professional Reporting**: One-click PDF reports for individual cases or comprehensive summaries

✅ **Complete Visibility**: Dashboard with live statistics, charts, and trends

---

## Key Features

### 🎯 1. Intelligent Case Management

**What It Does:**
- Create, view, update, and delete debt collection cases
- Track customer information, debt amounts, aging days, and payment status
- Store social media profiles, documents, and notes for each case
- Search, filter, and sort cases by any criteria

**Why It Matters:**
Centralizes all case information in one place, eliminating the need for multiple spreadsheets and reducing data entry errors.

---

### 🤖 2. AI-Powered Case Assignment

**What It Does:**
- Automatically assigns new cases to the best-suited DCA
- Considers:
  - Debt amount (matches DCA's debt range expertise)
  - DCA capacity (prevents overloading)
  - Performance history (prioritizes high performers)
  - Current workload (balances distribution)

**Why It Matters:**
Eliminates manual assignment work, ensures fair distribution, and maximizes recovery rates by matching cases with the right DCAs.

**Example:**
```
New Case: $250,000 debt

System Analysis:
- DCA A: Range $50K-$500K, Capacity 150, Active 120, Score 105% → ✅ MATCH
- DCA B: Range $10K-$200K, Capacity 100, Active 95, Score 98% → ❌ Outside range
- DCA C: Range $5K-$1M, Capacity 150, Active 150, Score 92% → ❌ At capacity

Result: Case assigned to DCA A with reason "Best match for debt range $50K-$500K, 
         available capacity (120/150), and strong performance score (105%)"
```

---

### 📊 3. Performance Scoring System

**What It Does:**
- Calculates real-time performance scores for each DCA (0-120%)
- Rewards quick resolutions (+5% for cases completed ≤5 days)
- Penalizes delays, rejections, and SLA breaches
- Updates automatically when case statuses change

**Why It Matters:**
Provides objective, data-driven metrics to identify top performers, reward excellence, and address underperformance.

**Scoring Breakdown:**
```
Base Score: 100%

Rewards:
+ 5% for each case completed within 5 days (quick win)

Penalties:
- 5% for each rejected case
- 3% for each delayed case
- 5% for each case completed with "At Risk" status
- 5% for each case completed with "Breached" status
- 2% per day for cases taking more than 10 days to complete

Final Score: Capped between 0% and 120%
```

---

### ⏰ 4. Priority-Based SLA Tracking

**What It Does:**
- Assigns SLA due dates based on case priority:
  - **P1 (High Priority)**: 3 days
  - **P2 (Medium Priority)**: 7 days
  - **P3 (Low Priority)**: 14 days
- Automatic status updates:
  - **On Track**: More than 50% time remaining
  - **At Risk**: Less than 50% time remaining
  - **Breached**: Past due date
- Visual color-coding: Green → Yellow → Red

**Why It Matters:**
Ensures critical cases receive urgent attention, prevents SLA breaches, and provides early warning for at-risk cases.

---

### 🏢 5. DCA Management

**What It Does:**
- Create and manage DCA profiles
- Set capacity limits and debt range expertise
- Track active cases, completed cases, rejections, and delays
- View detailed performance metrics and history
- Enable/disable DCAs without deleting data

**Why It Matters:**
Centralizes DCA information, enforces capacity limits, and provides complete visibility into each agency's performance and workload.

---

### 📈 6. Analytics Dashboard

**What It Does:**
- **Key Statistics**: Total cases, active cases, completion rate, average recovery amount
- **Case Distribution Chart**: Pie chart showing cases by status
- **Priority Breakdown**: Bar chart showing P1/P2/P3 distribution
- **Debt vs Recovery Trends**: Animated line chart showing monthly trends
- **Top Performing DCAs**: Leaderboard with scores
- **Recent Activity**: Latest case updates and assignments

**Why It Matters:**
Provides at-a-glance insights into collection operations, identifies trends, and supports data-driven decision making.

---

### 📄 7. Professional PDF Reports

**What It Does:**
- **Single Case Report**: Detailed report with:
  - Case information (ID, status, priority, SLA)
  - Customer details (name, contact, address, social media)
  - Financial data (debt amount, aging days)
  - DCA assignment details
  - Complete case history and notes
  
- **All Cases Summary Report**: Comprehensive overview with:
  - Summary statistics (total cases, completion rate, average debt)
  - Complete case table with all key fields
  - Professional formatting and branding

**Why It Matters:**
Eliminates manual report creation, ensures consistency, and provides professional documentation for stakeholders, audits, and compliance.

---

### 🧪 8. Testing Interface (Admin Only)

**What It Does:**
- Simulate DCA responses without affecting production data
- Quick actions:
  - Mark as Completed
  - Simulate Rejection (auto-reassigns to another DCA)
  - Simulate Delay
- View real-time performance score updates
- Reset all data to fresh state

**Why It Matters:**
Allows testing of workflows, training new users, and demonstrating platform capabilities without risking real data.

---

### ⚙️ 9. Configurable Settings (Admin Only)

**What It Does:**
- **SLA Configuration**: Adjust P1/P2/P3 day thresholds
- **Performance Parameters**: Customize rewards and penalties
  - Quick completion threshold (default: 5 days)
  - Quick completion reward (default: +5%)
  - Slow processing threshold (default: 10 days)
  - Penalty per extra day (default: -2%)
  - Rejection penalty (default: -5%)
  - Delay penalty (default: -3%)
  - Breach penalty (default: -5%)
- **Theme Settings**: Customize primary/secondary colors and light/dark mode
- **Time & Format**: Set timezone, date format, time format
- **Feature Flags**: Enable/disable AI assignment, email notifications, SMS notifications

**Why It Matters:**
Allows platform customization to match your organization's specific business rules, branding, and operational preferences.

---

### 👤 10. Customer Self-Service Portal

**What It Does:**
- Customers log in with Case ID + Phone Number
- View case status and details
- See assigned DCA contact information
- Track payment progress
- No need to call customer service for status updates

**Why It Matters:**
Reduces customer service calls, improves customer experience, and provides 24/7 access to case information.

---

### 📝 11. Audit Logging

**What It Does:**
- Logs every action in the system:
  - User who performed the action
  - Timestamp (UTC)
  - Action type (Create, Update, Delete, etc.)
  - Details (what changed)
- Searchable and filterable logs
- Exportable for compliance

**Why It Matters:**
Ensures accountability, supports compliance requirements, aids in troubleshooting, and provides complete audit trail.

---

### 🔐 12. Secure Authentication & Authorization

**What It Does:**
- JWT-based authentication
- Role-based access control:
  - **Admin**: Full access to all features
  - **User**: Case and DCA management (no settings or testing)
  - **Customer**: View own case only
- Password hashing with bcrypt
- Session management

**Why It Matters:**
Protects sensitive financial data, ensures only authorized users access specific features, and complies with security best practices.

---

## User Roles & Capabilities

### 👨‍💼 Admin Role

**Default Credentials:**
- Email: `admin@fedex.com`
- Password: `admin123`

**Can Access:**
- ✅ Dashboard (full analytics)
- ✅ Cases (create, view, update, delete)
- ✅ Case Details (with PDF download)
- ✅ DCA Management (create, edit, toggle status)
- ✅ Testing Interface (simulate responses, reset data)
- ✅ Settings (configure all parameters)
- ✅ Audit Logs (view all activity)

**Use Cases:**
- Configure platform settings and thresholds
- Monitor overall system performance
- Manage DCA accounts and capacity
- Generate comprehensive reports
- Test new workflows
- Review audit trails for compliance

---

### 👤 Regular User Role

**Default Credentials:**
- Email: `user@fedex.com`
- Password: `user123`

**Can Access:**
- ✅ Dashboard (view analytics)
- ✅ Cases (create, view, update)
- ✅ Case Details (view and download PDFs)
- ✅ DCA Management (view only, cannot create/edit)
- ✅ Audit Logs (view)
- ❌ Testing Interface
- ❌ Settings

**Use Cases:**
- Day-to-day case management
- Monitor case progress and SLAs
- View DCA performance
- Generate case reports

---

### 🧑‍💼 Customer Role

**Login Method:**
- Case ID + Phone Number (no pre-registration needed)

**Can Access:**
- ✅ Customer Dashboard (own case only)
- ❌ All other features

**Use Cases:**
- Check case status
- View payment progress
- See assigned DCA contact info
- Self-service case tracking

---

## Getting Started

### Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker + Docker Compose** (Linux)
- **Web Browser** (Chrome, Firefox, Safari, or Edge)
- **Minimum 4GB RAM** available for containers
- **5GB Disk Space** for images and data

### Installation Steps

1. **Clone or Download the Project**
   ```bash
   cd "d:\fedx Competation Projects"
   ```

2. **Start All Services**
   ```bash
   docker-compose up -d --build
   ```
   
   This will:
   - Build frontend, backend, and database containers
   - Initialize the database with sample data
   - Start all services in the background

3. **Verify Containers Are Running**
   ```bash
   docker-compose ps
   ```
   
   Expected output:
   ```
   NAME           STATUS
   dca_frontend   Up (healthy)
   dca_backend    Up (healthy)
   dca_postgres   Up (healthy)
   ```

4. **Access the Application**
   - **Landing Page**: http://localhost:4567
   - **Admin Dashboard**: http://localhost:4567/dashboard (after login)
   - **API Documentation**: http://localhost:8000/docs

5. **Login with Default Credentials**
   - Admin: `admin@fedex.com` / `admin123`
   - User: `user@fedex.com` / `user123`

### First-Time Setup Checklist

- [ ] Access landing page successfully
- [ ] Login with admin credentials
- [ ] View dashboard with sample data
- [ ] Create a test case
- [ ] Assign case to DCA (auto-assigned by AI)
- [ ] View DCA performance metrics
- [ ] Download a PDF report
- [ ] Explore settings (admin only)
- [ ] Test customer portal with a case ID

---

## User Guides

### For Collection Managers (Admin/User)

#### How to Create a New Case

1. Navigate to **Cases** page
2. Click **"+ Create Case"** button
3. Fill in the form:
   - **Customer Information**: Name, email, phone, address
   - **Financial Details**: Overdue amount, aging days
   - **Case Priority**: P1 (High), P2 (Medium), or P3 (Low)
   - **Optional**: Social media links, website, documents
4. Click **"Create Case"**
5. System automatically:
   - Calculates SLA due date based on priority
   - Generates AI recovery score
   - Assigns case to best-suited DCA
   - Logs action in audit trail

**Tips:**
- Use P1 for urgent cases (>$100K, critical accounts)
- Include social media links for better customer profiling
- Add detailed notes for DCA context

---

#### How to Monitor Case Progress

1. **Dashboard View**:
   - See total active cases, completion rate
   - View cases by status (pie chart)
   - Check priority distribution (bar chart)

2. **Cases List View**:
   - Search by customer name, case ID, or amount
   - Filter by status (Open, In Progress, Closed)
   - Sort by amount, aging days, or SLA status
   - Color-coded SLA indicators:
     - 🟢 Green: On Track
     - 🟡 Yellow: At Risk
     - 🔴 Red: Breached

3. **Case Detail View**:
   - Click any case to see full details
   - View assigned DCA and allocation reason
   - Check SLA due date and status
   - Download PDF report for the case

---

#### How to Manage DCAs

**View All DCAs:**
1. Navigate to **DCA Management** page
2. See all DCAs with:
   - Performance score
   - Active cases / Max capacity
   - Contact information

**Create New DCA:**
1. Click **"+ Create DCA"** button
2. Fill in:
   - Agency name and contact details
   - Max capacity (e.g., 150 cases)
   - Debt range expertise (e.g., $50K - $500K)
   - Website URL (optional)
3. Click **"Create DCA"**

**Edit DCA:**
1. Click on DCA card
2. Modal opens with detailed information
3. Admins can edit all fields
4. Save changes

**Disable DCA:**
1. Click on DCA card
2. Toggle **"Active"** switch
3. Disabled DCAs won't receive new assignments
4. Existing cases remain assigned

---

### For DCA Representatives

**Note**: DCAs typically interact via the Testing Interface or receive case notifications. Full DCA portal is a future enhancement.

#### Current Workflow:

1. **Receive Case Assignment** (notification or email - future feature)
2. **View Case Details** in Testing Interface
3. **Update Case Status**:
   - Mark as **In Progress** when starting work
   - Mark as **Completed** when recovered
   - **Reject** if unable to handle (auto-reassigns)
   - **Delay** if need more time
4. **Monitor Performance Score** in real-time

---

### For Customers

#### How to Check Your Case Status

1. Visit http://localhost:4567/customer-login
2. Enter:
   - **Case ID** (e.g., CASE-2024-001)
   - **Phone Number** (as registered in system)
3. Click **"Login"**
4. View:
   - Current case status
   - Overdue amount
   - Aging days
   - Priority and SLA status
   - Assigned DCA contact information
   - Payment progress

**Tips:**
- Case ID can be found in any correspondence from FedEx
- Phone number must match what's in the system
- Contact the assigned DCA for payment arrangements

---

## Feature Walkthroughs

### Walkthrough 1: Complete Case Lifecycle

**Scenario**: Create a high-priority case, monitor it, and mark as completed.

**Steps:**

1. **Create Case** (Admin/User)
   - Navigate to Cases → Create Case
   - Enter:
     - Customer: "ABC Corporation"
     - Amount: $150,000
     - Priority: P1 (High)
     - Aging: 45 days
   - Submit → Case auto-assigned to best DCA

2. **Monitor SLA** (Dashboard)
   - Case shows as 🟢 "On Track" (3-day SLA for P1)
   - DCA has 3 days to complete

3. **DCA Works on Case** (Testing Interface)
   - Navigate to Testing page
   - Find the case
   - Click "Mark as In Progress"
   - Status changes from "Open" → "In Progress"

4. **Complete Case** (Testing Interface)
   - Click "Mark as Completed"
   - System:
     - Records completion timestamp
     - Calculates processing time (e.g., 2 days)
     - Awards +5% reward to DCA (completed ≤5 days)
     - Updates DCA's avg completion time
     - Updates performance score
     - Removes from active case count

5. **Verify Results** (Dashboard)
   - Total completed cases increases
   - DCA performance score shows improvement
   - Case appears in "Closed" status

---

### Walkthrough 2: Rejection and Reassignment

**Scenario**: DCA rejects a case, system auto-reassigns to another DCA.

**Steps:**

1. **DCA Rejects Case** (Testing Interface)
   - Select a case
   - Click "Simulate Rejection"
   - Enter rejection reason (optional)

2. **System Response**:
   - Applies -5% penalty to original DCA's score
   - Searches for alternative DCA:
     - Within debt range
     - Has available capacity
     - Not the rejecting DCA
   - Auto-assigns to next best match
   - Adds note to case: "Rejected by [DCA Name], reassigned to [New DCA]"

3. **Verify Reassignment**:
   - Check case details
   - See updated DCA assignment
   - View allocation reason
   - Original DCA's performance score decreased

---

### Walkthrough 3: Generate and Download Reports

**Scenario**: Generate PDF reports for analysis and sharing.

**Single Case Report:**

1. Navigate to **Cases** page
2. Click on any case to open details
3. Click **"📄 Download PDF"** button
4. PDF downloads with:
   - Case summary (ID, status, priority, SLA)
   - Customer information (name, contact, address)
   - Financial details (amount, aging)
   - DCA assignment details
   - Social media links
   - Complete notes

**All Cases Report:**

1. Navigate to **Cases** page
2. Click **"📄 Download PDF Report"** button (top-right)
3. PDF downloads with:
   - Summary statistics (total cases, completion rate, avg amount)
   - Complete table with all cases
   - Sortable by priority, status, amount
   - Professional formatting

**Use Cases:**
- Share with stakeholders
- Monthly performance reviews
- Compliance documentation
- Client presentations

---

### Walkthrough 4: Customize Platform Settings

**Scenario**: Adjust SLA thresholds and performance parameters.

**Steps:** (Admin Only)

1. **Navigate to Settings** page
2. **SLA Configuration**:
   - Change P1 from 3 days → 2 days (more urgent)
   - Change P2 from 7 days → 5 days
   - Keep P3 at 14 days

3. **Performance Parameters**:
   - Quick completion: Change from 5 days → 3 days (stricter)
   - Quick reward: Keep at +5%
   - Slow threshold: Change from 10 days → 8 days
   - Rejection penalty: Increase from -5% → -8% (stricter)

4. **Theme Settings**:
   - Change primary color to match company branding
   - Set theme mode to "Dark"

5. **Save Changes**:
   - Click "Save Settings"
   - All new cases will use updated SLA thresholds
   - Performance scores will recalculate with new penalties

---

## Performance Scoring Explained

### Why Performance Scoring Matters

Performance scores help you:
- **Identify Top Performers**: Reward DCAs who complete cases quickly and efficiently
- **Address Underperformance**: Spot DCAs with delays, rejections, or SLA breaches
- **Make Data-Driven Decisions**: Assign high-value cases to high-performing DCAs
- **Ensure Accountability**: Transparent metrics reduce disputes

### How Scores Are Calculated

**Starting Point**: Every DCA starts with 100%

**Rewards (Add to Score)**:
| Action | Reward | Example |
|--------|--------|---------|
| Quick Completion | +5% per case | Complete in 3 days → +5% |

**Penalties (Subtract from Score)**:
| Issue | Penalty | Example |
|-------|---------|---------|
| Rejection | -5% per case | Reject 2 cases → -10% |
| Delay | -3% per case | Delay 1 case → -3% |
| At Risk Completion | -5% per case | Complete with yellow SLA → -5% |
| Breached Completion | -5% per case | Complete with red SLA → -5% |
| Slow Processing | -2% per extra day | Take 15 days (5 over limit) → -10% |

### Real-World Example

**DCA: Swift Debt Solutions**

**Cases Handled:**
- 10 completed cases total

**Breakdown:**
- 6 cases completed in ≤5 days → **+30%** reward
- 2 cases completed in 6-10 days → **0%** (neutral)
- 2 cases completed in 15 days (5 days over 10-day limit) → **-20%** penalty (5 days × 2 cases × 2%)
- 1 case rejected → **-5%** penalty
- 1 case completed with "At Risk" status → **-5%** penalty
- 0 cases delayed → **0%**
- 0 cases breached → **0%**

**Calculation:**
```
Base:       100%
Rewards:    +30% (6 × 5%)
Penalties:  -20% (slow) -5% (rejection) -5% (at risk) = -30%

Final Score: 100% + 30% - 30% = 100%
```

**Interpretation:** This DCA performs at baseline. While they have good quick completions, the slow cases, rejection, and at-risk completion offset the rewards.

### Score Ranges and What They Mean

| Score Range | Performance Level | Action |
|-------------|-------------------|--------|
| 110-120% | Exceptional | Assign premium cases, consider bonuses |
| 100-109% | Excellent | Increase capacity, assign complex cases |
| 90-99% | Good | Continue monitoring, minor improvements |
| 80-89% | Average | Review processes, provide training |
| 70-79% | Below Average | Performance review, improvement plan |
| 0-69% | Poor | Urgent intervention, consider suspension |

### Tips for Improving Scores

**For DCAs:**
- ✅ Prioritize quick wins (cases that can be resolved in ≤5 days)
- ✅ Communicate early if rejection is necessary
- ✅ Request delays proactively rather than letting cases breach SLA
- ✅ Focus on high-priority (P1) cases first
- ✅ Maintain good records and notes for audit trail

**For Managers:**
- ✅ Review low-scoring DCAs weekly
- ✅ Provide training on best practices
- ✅ Adjust capacity for overloaded DCAs
- ✅ Recognize and reward top performers
- ✅ Use performance data in DCA contracts

---

## SLA Management Explained

### What Are SLAs?

**Service Level Agreements (SLAs)** define the expected timeframe for case resolution based on priority.

### Priority Levels

| Priority | SLA Days | Use For | Example |
|----------|----------|---------|---------|
| **P1 (High)** | 3 days | Urgent, high-value cases | $500K debt, VIP customer, legal deadline |
| **P2 (Medium)** | 7 days | Standard cases | $50K-$500K, normal priority |
| **P3 (Low)** | 14 days | Low-value or routine cases | <$50K, no urgency |

### SLA Statuses

**🟢 On Track (Green)**
- More than 50% of SLA time remaining
- Case is progressing well
- No immediate action needed

**🟡 At Risk (Yellow)**
- Less than 50% of SLA time remaining
- Case needs attention
- Warning to DCA: Act soon or risk breach

**🔴 Breached (Red)**
- Past SLA due date
- Case has failed SLA compliance
- -5% performance penalty
- Urgent escalation required

### How SLA Due Dates Are Calculated

```
SLA Due Date = Case Creation Date + Priority SLA Days

Examples:
- P1 case created Jan 1 → Due Jan 4 (3 days)
- P2 case created Jan 1 → Due Jan 8 (7 days)
- P3 case created Jan 1 → Due Jan 15 (14 days)
```

### SLA Status Updates (Automatic)

The system automatically updates SLA status based on:

1. **Time Elapsed**: Calculates % of SLA time used
2. **Status Changes**: 
   - Green → Yellow when >50% time elapsed
   - Yellow → Red when due date passes
3. **Completion**: SLA stops updating when case marked "Closed"

### Best Practices for SLA Management

**For Managers:**
- ✅ Monitor yellow (At Risk) cases daily
- ✅ Escalate red (Breached) cases immediately
- ✅ Adjust SLA thresholds in Settings if needed
- ✅ Use SLA data in DCA performance reviews

**For DCAs:**
- ✅ Check SLA status before starting work
- ✅ Prioritize red and yellow cases
- ✅ Communicate early if SLA cannot be met
- ✅ Request delays before breach, not after

**For Customers:**
- ✅ Higher priority = faster resolution
- ✅ Check customer portal for SLA status
- ✅ Contact DCA if SLA is breached

---

## AI-Powered Features

### 1. Intelligent Case Assignment

**How It Works:**

When you create a new case, the AI analyzes:

1. **Debt Amount**: Matches case to DCAs with appropriate debt range expertise
   - Example: $250K case → DCAs handling $50K-$500K range preferred

2. **DCA Capacity**: Checks available slots
   - Example: DCA has 120/150 cases → 30 slots available

3. **Performance Score**: Prioritizes high-performing DCAs
   - Example: DCA with 110% score preferred over 85% score

4. **Workload Balance**: Prevents overloading any single DCA
   - Example: If top DCA is 95% full, assigns to next best option

**Fallback Logic:**

- **Tier 1**: Perfect match (debt range + capacity + performance)
- **Tier 2**: Any DCA with capacity (if no perfect match)
- **Tier 3**: Expand capacity of best DCA (if all are full)

**Benefits:**
- Eliminates manual assignment work
- Ensures fair distribution
- Maximizes recovery rates
- Reduces human error

---

### 2. Recovery Score Prediction

**What It Does:**

For each case, the AI calculates a **recovery likelihood score (0-1)**:
- 0.8-1.0: High likelihood of recovery
- 0.5-0.79: Medium likelihood
- 0-0.49: Low likelihood

**Factors Considered:**
- Debt amount
- Aging days (older = lower score)
- Priority level
- Customer profile (if available)

**How to Use:**
- Focus resources on high-score cases
- Adjust priority for low-score cases
- Use in performance analytics

**Note**: Currently uses basic heuristics. Future versions will incorporate machine learning models trained on historical recovery data.

---

## Reports & Analytics

### Available Reports

#### 1. Dashboard Overview
- **Total Statistics**: Cases, active cases, completion rate, avg recovery
- **Visual Charts**: 
  - Pie chart (cases by status)
  - Bar chart (priority distribution)
  - Line chart (debt vs recovery trends)
- **Top Performers**: DCAs ranked by score
- **Recent Activity**: Latest updates

#### 2. Single Case PDF Report
- Complete case details
- Customer information
- DCA assignment
- Financial summary
- Social media links
- Full history and notes

#### 3. All Cases PDF Report
- Summary statistics
- Complete case table
- Exportable and shareable

### How to Use Analytics

**Daily Monitoring:**
- Check dashboard for completion rate
- Review at-risk cases (yellow SLA)
- Monitor top/bottom performing DCAs

**Weekly Review:**
- Download all cases PDF report
- Analyze trends in line chart
- Review DCA performance scores
- Identify bottlenecks

**Monthly Reporting:**
- Generate comprehensive PDFs
- Share with stakeholders
- Update SLA thresholds if needed
- Plan capacity adjustments

---

## Customization & Settings

### What Can Be Customized?

**SLA Parameters:**
- P1, P2, P3 day thresholds
- Adjust based on business needs

**Performance Scoring:**
- Quick completion threshold (days)
- Quick completion reward (%)
- Slow processing threshold (days)
- Processing penalty per day (%)
- Rejection penalty (%)
- Delay penalty (%)
- Breach penalty (%)

**Theme & Branding:**
- Primary color (hex code)
- Secondary color (hex code)
- Light/dark mode

**Time & Localization:**
- Timezone
- Date format (MM/DD/YYYY, DD/MM/YYYY, etc.)
- Time format (12h/24h)

**Feature Flags:**
- Enable/disable AI assignment
- Enable/disable email notifications (future)
- Enable/disable SMS notifications (future)

### How to Change Settings

1. Login as **admin**
2. Navigate to **Settings** page
3. Modify desired parameters
4. Click **"Save Settings"**
5. Changes apply immediately to new cases

### Reset to Defaults

1. Navigate to Settings page
2. Click **"Reset to Defaults"** button
3. Confirm action
4. All settings revert to original values

---

## Frequently Asked Questions

### General Questions

**Q: Who has access to the platform?**
A: Admin users, regular users, and customers (via case ID + phone).

**Q: Can I use this on mobile?**
A: Yes, the UI is responsive and works on tablets and smartphones.

**Q: Is my data secure?**
A: Yes. Passwords are encrypted, JWT tokens are used, and access is role-based.

**Q: Can I export data?**
A: Yes. PDF reports are available, and audit logs can be exported.

---

### Technical Questions

**Q: What happens if a DCA is at capacity?**
A: The system finds another DCA. If all are full, it expands the capacity of the highest-performing DCA.

**Q: How often are performance scores updated?**
A: Immediately when a case is completed, rejected, or delayed.

**Q: Can I change SLA thresholds after cases are created?**
A: Yes, but only new cases use the new thresholds. Existing cases keep original SLAs.

**Q: What if two DCAs have the same score?**
A: The system picks the one with lower current workload (active cases).

---

### Troubleshooting Questions

**Q: I can't login. What should I do?**
A: 
1. Verify credentials (case-sensitive)
2. Check if user is active
3. Try resetting the database (see DATA_MANAGEMENT.md)

**Q: A case isn't assigned to any DCA. Why?**
A: This should never happen due to the 3-tier fallback. Check backend logs for errors.

**Q: Performance score seems wrong. How to fix?**
A: Scores recalculate automatically. If still incorrect, check Settings for penalty parameters.

**Q: PDF download isn't working. What's wrong?**
A: 
1. Check if backend is running (`docker-compose ps`)
2. Verify you're logged in (JWT token required)
3. Check browser console for errors

---

## Troubleshooting Guide

### Application Won't Start

**Symptoms**: Containers fail to start or exit immediately.

**Solutions**:
1. Check Docker is running: `docker ps`
2. View logs: `docker-compose logs backend` or `docker-compose logs frontend`
3. Rebuild: `docker-compose down && docker-compose up --build -d`
4. Check ports 4567, 8000, 5432 aren't in use

---

### Database Connection Errors

**Symptoms**: Backend logs show "connection refused" or "database not ready".

**Solutions**:
1. Check postgres container: `docker-compose ps postgres`
2. Verify health: Should show "healthy"
3. Restart postgres: `docker-compose restart postgres`
4. Wait 10 seconds and restart backend: `docker-compose restart backend`

---

### Frontend Shows Blank Page

**Symptoms**: White screen or "Cannot connect to backend".

**Solutions**:
1. Check backend is running: `docker-compose ps backend`
2. Verify API URL in browser console (should be `http://localhost:8000`)
3. Clear browser cache and hard reload (Ctrl+Shift+R)
4. Check frontend logs: `docker-compose logs frontend`

---

### Performance Score Not Updating

**Symptoms**: Score stays at "TBD" or doesn't change after case completion.

**Solutions**:
1. Complete at least one case (score is "TBD" until first completion)
2. Check backend logs for calculation output: `docker logs dca_backend -f`
3. Verify case has `assigned_at` and `completed_at` timestamps
4. Restart backend: `docker-compose restart backend`

---

### Cannot Download PDF

**Symptoms**: PDF button doesn't work or shows error.

**Solutions**:
1. Verify you're logged in (check for token in localStorage)
2. Check backend logs: `docker-compose logs backend --tail=50`
3. Verify ReportLab is installed: `docker-compose exec backend pip list | grep reportlab`
4. Try single case PDF first, then all cases PDF

---

### Data Reset Issues

**Symptoms**: "Reset All Data" button fails or leaves partial data.

**Solutions**:
1. Use manual reset: `docker-compose exec backend python reset_and_init_data.py --reset`
2. Check output for errors
3. If still failing, drop database and restart: 
   ```bash
   docker-compose down -v
   docker-compose up -d --build
   ```

---

## Best Practices

### For Administrators

✅ **Regular Monitoring**
- Check dashboard daily for SLA breaches
- Review performance scores weekly
- Analyze trends monthly

✅ **Capacity Management**
- Monitor DCA workloads
- Adjust capacity limits as needed
- Add new DCAs before existing ones max out

✅ **Settings Optimization**
- Review SLA thresholds quarterly
- Adjust penalties based on business goals
- Test changes in non-production environment first

✅ **Data Hygiene**
- Archive old cases periodically
- Review audit logs monthly
- Back up database weekly (see DATA_MANAGEMENT.md)

---

### For Users

✅ **Case Creation**
- Include complete customer information
- Choose appropriate priority level
- Add detailed notes for DCA context

✅ **Monitoring**
- Check yellow (At Risk) cases daily
- Follow up on breached cases immediately
- Review completion rates weekly

✅ **Reporting**
- Generate PDFs for monthly reviews
- Share analytics with team
- Use data for process improvements

---

### For DCAs

✅ **Efficiency**
- Prioritize quick wins (≤5 days)
- Work on P1 cases first
- Communicate early on issues

✅ **Communication**
- Request delays proactively
- Reject cases early if unsuitable
- Update case notes regularly

✅ **Quality**
- Maintain high completion rate
- Minimize rejections and delays
- Keep SLA compliance above 90%

---

## Summary

The **FedEx DCA Management Platform** transforms debt collection operations by:

✅ **Automating** case assignment with AI
✅ **Tracking** performance with objective scoring
✅ **Monitoring** SLAs with priority-based tracking
✅ **Providing** rich analytics and professional reports
✅ **Enabling** customization for your business needs
✅ **Ensuring** security and compliance with audit logs

**Next Steps:**
1. Complete the [Getting Started](#getting-started) guide
2. Explore each feature with sample data
3. Customize settings for your organization
4. Train your team with user guides
5. Review the [Architecture Documentation](ARCHITECTURE.md) for technical details

**Need Help?**
- Check [Troubleshooting Guide](#troubleshooting-guide)
- Review [FAQs](#frequently-asked-questions)
- Consult [Data Management Guide](DATA_MANAGEMENT.md)
- See [Architecture Documentation](ARCHITECTURE.md)

---

**Document Version**: 1.0  
**Last Updated**: January 4, 2026  
**For**: FedEx DCA Management Platform  
**Audience**: All Users (Admin, Users, Customers)
