---
skill_id: employee_onboarding
name: Employee Onboarding
version: 1.0.0
description: Coordinate employee onboarding using approved company procedures and authorized internal tools.
risk_level: medium
status: draft
---

# Employee Onboarding

Coordinate employee onboarding using approved company procedures and authorized internal tools.

## Inputs

- `employee_id`
- `start_date`
- `department`

## Outputs

- `onboarding_plan`
- `completion_status`

## Capabilities

- `employee_lookup`
- `document_retrieval`
- `task_management`
- `notification_service`

## Constraints

- Use current approved HR policies.
- Do not expose confidential employee information.
- Require authorization before modifying employee records.

## Procedure

### Step 1: retrieve_hr_policy

**Action:** `retrieve_approved_hr_policy`

**Tool:** `document_retrieval`

### Step 2: validate_employee

**Action:** `validate_employee_record`

**Tool:** `employee_lookup`

### Step 3: prepare_onboarding_plan

**Action:** `prepare_onboarding_checklist`

### Step 4: create_onboarding_tasks

**Action:** `create_onboarding_tasks`

**Tool:** `task_management`

### Step 5: notify_responsible_team

**Action:** `notify_onboarding_team`

**Tool:** `notification_service`

## Execution Notes

- Follow the steps in the defined order.
- Use only authorized tools and approved company information.
- Enforce applicable policies and approval requirements before actions.
- Record execution outcomes through the authorized audit mechanism.
- Stop and request clarification or approval when required information,
  authorization, or policy decisions are missing.
