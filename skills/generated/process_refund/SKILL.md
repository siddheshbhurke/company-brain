---
skill_id: process_refund
name: Process Customer Refund
version: 1.0.0
description: Validate a customer refund request, evaluate the refund policy, obtain required approval, and prepare a controlled refund workflow.
risk_level: high
status: active
---

# Process Customer Refund

Validate a customer refund request, evaluate the refund policy, obtain required approval, and prepare a controlled refund workflow.

## Inputs

- No inputs specified.

## Outputs

- No outputs specified.

## Capabilities

- No capabilities specified.

## Constraints

- No constraints specified.

## Procedure

### Step 1: validate_customer

**Action:** `validate_customer`

**Tool:** `customer_lookup`

### Step 2: retrieve_order

**Action:** `retrieve_order`

**Tool:** `order_lookup`

### Step 3: check_eligibility

**Action:** `check_refund_eligibility`

**Tool:** `refund_rule_engine`

### Step 4: evaluate_policy

**Action:** `evaluate_refund_policy`

**Tool:** `refund_rule_engine`

### Step 5: request_manager_approval

**Action:** `request_approval`

**Tool:** `approval_service`

### Step 6: execute_refund

**Action:** `execute_refund`

**Tool:** `refund_service`

### Step 7: update_ticket

**Action:** `update_support_ticket`

**Tool:** `ticket_service`

### Step 8: notify_customer

**Action:** `notify_customer`

**Tool:** `notification_service`

### Step 9: record_audit

**Action:** `record_execution_audit`

**Tool:** `audit_service`

## Execution Notes

- Follow the steps in the defined order.
- Use only authorized tools and approved company information.
- Enforce applicable policies and approval requirements before actions.
- Record execution outcomes through the authorized audit mechanism.
- Stop and request clarification or approval when required information,
  authorization, or policy decisions are missing.
