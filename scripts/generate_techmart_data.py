import csv
import json
from pathlib import Path
from datetime import datetime, timedelta
import random


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

DOCUMENTS = DATA / "documents"
TICKETS = DATA / "tickets"
EMAILS = DATA / "emails"
EVENTS = DATA / "events"
COMPANY = DATA / "company"

for directory in [
    DOCUMENTS,
    TICKETS,
    EMAILS,
    EVENTS,
    COMPANY,
]:
    directory.mkdir(parents=True, exist_ok=True)


# ============================================================
# 1. REFUND POLICY
# ============================================================

refund_policy = """
# TechMart Refund and Return Policy

Policy ID: TM-REFUND-001
Version: 2.1
Effective From: 2026-01-01
Authority: Customer Operations

## Standard Refund Eligibility

Customers may request a refund when:

1. The order was delivered within the last 30 calendar days.
2. The product is eligible for return.
3. The product has not been marked as non-refundable.
4. The order has not already received a completed refund.

## Automatic Refund Approval

Refunds up to and including INR 50,000 may be approved automatically
when all standard eligibility conditions are satisfied.

## Manager Approval

Refunds greater than INR 50,000 require approval from a Customer
Operations Manager before the refund can be executed.

## Refund Restrictions

The system must not execute a refund when:

- The order cannot be found.
- The customer cannot be verified.
- The order is outside the 30-day refund window.
- The product is non-refundable.
- A completed refund already exists.

## Audit Requirement

Every refund decision must record:

- Customer ID
- Order ID
- Refund amount
- Applicable policy version
- Approval status
- Executing employee or agent
- Timestamp
- Final result
"""

(DOCUMENTS / "refund_policy_v2.1.md").write_text(
    refund_policy.strip(),
    encoding="utf-8"
)


# ============================================================
# 2. REFUND PROCESSING SOP
# ============================================================

refund_sop = """
# TechMart Refund Processing SOP

SOP ID: TM-SOP-REFUND-001
Version: 1.4

## Procedure

Step 1:
Verify the customer identity.

Step 2:
Retrieve the customer's order.

Step 3:
Verify that the order is eligible for refund.

Step 4:
Retrieve the current refund policy.

Step 5:
Determine the refund amount.

Step 6:
If the refund amount is greater than INR 50,000,
request Customer Operations Manager approval.

Step 7:
If approval is granted, execute the refund.

Step 8:
Update the support ticket.

Step 9:
Send the customer a refund confirmation.

Step 10:
Create an audit record containing the evidence and decision.

## Safety Rule

Never execute a refund before completing customer,
order and eligibility validation.
"""

(DOCUMENTS / "refund_processing_sop_v1.4.md").write_text(
    refund_sop.strip(),
    encoding="utf-8"
)


# ============================================================
# 3. COMPLAINT ESCALATION POLICY
# ============================================================

complaint_policy = """
# TechMart Complaint Escalation Policy

Policy ID: TM-COMP-002
Version: 1.2
Effective From: 2026-02-01

Customer complaints must be classified according to severity.

LOW:
Normal product or service complaint.
Handled by Tier 1 support.

MEDIUM:
Repeated complaint, unresolved issue, or customer dissatisfaction
after an initial response.
Escalate to Tier 2 support.

HIGH:
Potential legal issue, safety concern, fraud allegation,
or executive escalation request.
Escalate to Customer Operations Manager.

All escalation decisions must be recorded in the support ticket.
"""

(DOCUMENTS / "complaint_escalation_policy.md").write_text(
    complaint_policy.strip(),
    encoding="utf-8"
)


# ============================================================
# 4. DISCOUNT POLICY
# ============================================================

discount_policy = """
# TechMart Discount Approval Policy

Policy ID: TM-DISCOUNT-003
Version: 1.1
Effective From: 2026-01-15

Sales representatives may approve discounts up to 10%.

Discounts greater than 10% and up to 20% require Sales Manager approval.

Discounts greater than 20% require Regional Sales Director approval.

Discounts must never be applied without recording the approving role.
"""

(DOCUMENTS / "discount_approval_policy.md").write_text(
    discount_policy.strip(),
    encoding="utf-8"
)


# ============================================================
# 5. CUSTOMERS
# ============================================================

customers = [
    {
        "customer_id": "CUST-1001",
        "name": "Aarav Mehta",
        "email": "aarav.mehta@example.com",
        "tier": "gold",
        "city": "Pune"
    },
    {
        "customer_id": "CUST-1002",
        "name": "Isha Kulkarni",
        "email": "isha.kulkarni@example.com",
        "tier": "silver",
        "city": "Mumbai"
    },
    {
        "customer_id": "CUST-1003",
        "name": "Rohan Shah",
        "email": "rohan.shah@example.com",
        "tier": "gold",
        "city": "Ahmedabad"
    },
    {
        "customer_id": "CUST-1004",
        "name": "Neha Patil",
        "email": "neha.patil@example.com",
        "tier": "standard",
        "city": "Pune"
    },
    {
        "customer_id": "CUST-1005",
        "name": "Kabir Joshi",
        "email": "kabir.joshi@example.com",
        "tier": "silver",
        "city": "Bengaluru"
    }
]

with open(COMPANY / "customers.json", "w", encoding="utf-8") as f:
    json.dump(customers, f, indent=2)


# ============================================================
# 6. ORDERS
# ============================================================

orders = [
    {
        "order_id": "ORD-18291",
        "customer_id": "CUST-1001",
        "product": "Professional Laptop",
        "amount": 75000,
        "order_date": "2026-09-05",
        "delivery_date": "2026-09-10",
        "status": "delivered",
        "returnable": True,
        "refund_status": "none"
    },
    {
        "order_id": "ORD-18292",
        "customer_id": "CUST-1002",
        "product": "Mirrorless Camera",
        "amount": 42000,
        "order_date": "2026-09-08",
        "delivery_date": "2026-09-13",
        "status": "delivered",
        "returnable": True,
        "refund_status": "none"
    },
    {
        "order_id": "ORD-18293",
        "customer_id": "CUST-1003",
        "product": "Gaming Monitor",
        "amount": 28000,
        "order_date": "2026-08-20",
        "delivery_date": "2026-08-25",
        "status": "delivered",
        "returnable": True,
        "refund_status": "none"
    },
    {
        "order_id": "ORD-18294",
        "customer_id": "CUST-1004",
        "product": "Wireless Headphones",
        "amount": 12000,
        "order_date": "2026-09-12",
        "delivery_date": "2026-09-16",
        "status": "delivered",
        "returnable": True,
        "refund_status": "none"
    },
    {
        "order_id": "ORD-18295",
        "customer_id": "CUST-1005",
        "product": "Tablet",
        "amount": 36000,
        "order_date": "2026-08-01",
        "delivery_date": "2026-08-05",
        "status": "delivered",
        "returnable": False,
        "refund_status": "none"
    }
]

with open(COMPANY / "orders.json", "w", encoding="utf-8") as f:
    json.dump(orders, f, indent=2)


# ============================================================
# 7. EMPLOYEES
# ============================================================

employees = [
    {
        "employee_id": "EMP-001",
        "name": "Priya Sharma",
        "role": "Customer Support Agent",
        "department": "Customer Operations"
    },
    {
        "employee_id": "EMP-002",
        "name": "Vikram Desai",
        "role": "Customer Operations Manager",
        "department": "Customer Operations"
    },
    {
        "employee_id": "EMP-003",
        "name": "Ananya Rao",
        "role": "Sales Representative",
        "department": "Sales"
    },
    {
        "employee_id": "EMP-004",
        "name": "Rahul Kapoor",
        "role": "Sales Manager",
        "department": "Sales"
    }
]

with open(COMPANY / "employees.json", "w", encoding="utf-8") as f:
    json.dump(employees, f, indent=2)


# ============================================================
# 8. SUPPORT TICKETS
# ============================================================

tickets = [
    {
        "ticket_id": "TKT-5001",
        "customer_id": "CUST-1001",
        "order_id": "ORD-18291",
        "category": "refund",
        "priority": "high",
        "status": "open",
        "description": "Customer requests a full refund for Professional Laptop."
    },
    {
        "ticket_id": "TKT-5002",
        "customer_id": "CUST-1002",
        "order_id": "ORD-18292",
        "category": "refund",
        "priority": "medium",
        "status": "open",
        "description": "Customer reports camera defect and requests refund."
    },
    {
        "ticket_id": "TKT-5003",
        "customer_id": "CUST-1003",
        "order_id": "ORD-18293",
        "category": "complaint",
        "priority": "medium",
        "status": "open",
        "description": "Customer has contacted support twice about a delayed resolution."
    },
    {
        "ticket_id": "TKT-5004",
        "customer_id": "CUST-1004",
        "order_id": "ORD-18294",
        "category": "complaint",
        "priority": "low",
        "status": "open",
        "description": "Customer reports dissatisfaction with delivery experience."
    }
]

with open(TICKETS / "support_tickets.json", "w", encoding="utf-8") as f:
    json.dump(tickets, f, indent=2)


# ============================================================
# 9. EMAILS
# ============================================================

emails = [
    {
        "email_id": "EMAIL-001",
        "from": "customer@example.com",
        "to": "support@techmart.example",
        "subject": "Refund request for ORD-18291",
        "body": "I would like a full refund for my Professional Laptop order ORD-18291.",
        "timestamp": "2026-09-20T10:30:00"
    },
    {
        "email_id": "EMAIL-002",
        "from": "ops.manager@techmart.example",
        "to": "support@techmart.example",
        "subject": "High value refund approval",
        "body": "Refunds above INR 50000 must be approved by Customer Operations Manager.",
        "timestamp": "2026-09-20T11:00:00"
    }
]

with open(EMAILS / "emails.json", "w", encoding="utf-8") as f:
    json.dump(emails, f, indent=2)


# ============================================================
# 10. PROCESS EVENT LOG
# ============================================================

event_rows = [
    ["TKT-5001", "ticket_created", "2026-09-20T10:30:00", "EMP-001"],
    ["TKT-5001", "ticket_assigned", "2026-09-20T10:35:00", "EMP-001"],
    ["TKT-5001", "refund_validation_started", "2026-09-20T10:40:00", "EMP-001"],
    ["TKT-5001", "manager_approval_requested", "2026-09-20T10:45:00", "EMP-001"],

    ["TKT-5002", "ticket_created", "2026-09-19T09:00:00", "EMP-001"],
    ["TKT-5002", "ticket_assigned", "2026-09-19T09:10:00", "EMP-001"],
    ["TKT-5002", "refund_validation_started", "2026-09-19T09:30:00", "EMP-001"],
    ["TKT-5002", "refund_approved", "2026-09-19T09:45:00", "EMP-002"],

    ["TKT-5003", "ticket_created", "2026-09-18T09:00:00", "EMP-001"],
    ["TKT-5003", "ticket_assigned", "2026-09-18T09:15:00", "EMP-001"],
    ["TKT-5003", "tier1_response", "2026-09-18T10:00:00", "EMP-001"],
    ["TKT-5003", "escalated", "2026-09-18T14:00:00", "EMP-001"],
    ["TKT-5003", "tier2_response", "2026-09-18T15:00:00", "EMP-002"],
    ["TKT-5003", "resolved", "2026-09-19T11:00:00", "EMP-002"]
]

with open(EVENTS / "support_process_events.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "case_id",
        "event",
        "timestamp",
        "employee_id"
    ])
    writer.writerows(event_rows)


# ============================================================
# 11. SLACK EXPORT
# ============================================================

slack_messages = [
    {
        "message_id": "SLACK-001",
        "channel": "#customer-operations",
        "author": "EMP-002",
        "timestamp": "2026-09-20T11:00:00",
        "message": "Reminder: refunds above INR 50,000 require manager approval before execution."
    },
    {
        "message_id": "SLACK-002",
        "channel": "#customer-operations",
        "author": "EMP-001",
        "timestamp": "2026-09-20T11:05:00",
        "message": "For high-value refunds, validate the order and eligibility before requesting approval."
    }
]

with open(DATA / "emails" / "slack_export.json", "w", encoding="utf-8") as f:
    json.dump(slack_messages, f, indent=2)


print("TechMart synthetic enterprise dataset created successfully.")
print()
print(f"Documents : {len(list(DOCUMENTS.iterdir()))}")
print(f"Customers : {len(customers)}")
print(f"Orders    : {len(orders)}")
print(f"Employees : {len(employees)}")
print(f"Tickets   : {len(tickets)}")
print(f"Emails    : {len(emails)}")
print(f"Events    : {len(event_rows)}")
print(f"Slack     : {len(slack_messages)}")
