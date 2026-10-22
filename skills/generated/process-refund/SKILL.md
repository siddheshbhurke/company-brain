---
name: process-refund
skill_id: process_refund
description: "Validate a customer refund request, evaluate the refund policy, obtain required approval, and prepare a controlled refund workflow."
---

# Process Customer Refund

Validate a customer refund request, evaluate the refund policy, obtain required approval, and prepare a controlled refund workflow.

## Skill Metadata

- **Skill ID:** `process_refund`
- **Version:** `1.0.0`
- **Risk Level:** high
- **Status:** active

## Inputs

- `customer_id`
- `order_id`
- `refund_amount`
- `refund_reason`

## Outputs

- `refund_eligibility`
- `approval_status`
- `refund_status`
- `support_ticket_status`
- `audit_record`

## Capabilities

- `validate_customer_identity`
- `retrieve_order_details`
- `evaluate_refund_policy`
- `determine_refund_eligibility`
- `request_manager_approval`
- `execute_authorized_refunds`
- `update_support_tickets`
- `notify_customers`
- `record_audit_events`

## Constraints

- Verify customer identity and order details before evaluating a refund.
- Apply the configured refund policy and eligibility rules.
- Require manager approval when policy or refund thresholds demand it.
- Never execute a refund without the required authorization.
- Do not invent missing customer, order, or policy information.
- Record the outcome of each workflow step.
- Stop and request clarification when required inputs are missing.

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
