from pathlib import Path
import json

from app.core.config import settings
from app.graph.connection import get_driver


BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"


def load_customers(tx, customers):
    for customer in customers:
        tx.run(
            """
            MERGE (c:Customer {id: $id})
            SET c.name = $name,
                c.email = $email,
                c.tier = $tier,
                c.city = $city
            """,
            id=customer["customer_id"],
            name=customer["name"],
            email=customer["email"],
            tier=customer["tier"],
            city=customer["city"],
        )


def load_orders(tx, orders):
    for order in orders:
        tx.run(
            """
            MERGE (o:Order {id: $id})
            SET o.customer_id = $customer_id,
                o.product = $product,
                o.amount = $amount,
                o.order_date = $order_date,
                o.delivery_date = $delivery_date,
                o.status = $status,
                o.returnable = $returnable,
                o.refund_status = $refund_status
            """,
            id=order["order_id"],
            customer_id=order["customer_id"],
            product=order["product"],
            amount=order["amount"],
            order_date=order["order_date"],
            delivery_date=order["delivery_date"],
            status=order["status"],
            returnable=order["returnable"],
            refund_status=order["refund_status"],
        )

        tx.run(
            """
            MATCH (c:Customer {id: $customer_id})
            MATCH (o:Order {id: $order_id})
            MERGE (c)-[:PLACED]->(o)
            """,
            customer_id=order["customer_id"],
            order_id=order["order_id"],
        )


def load_refund_policy(tx):
    tx.run(
        """
        MERGE (p:Policy {id: $id})
        SET p.name = $name,
            p.version = $version,
            p.type = $type
        """,
        id="TM-REFUND-001",
        name="TechMart Refund and Return Policy",
        version="2.1",
        type="refund",
    )

    tx.run(
        """
        MERGE (r:Rule {id: $id})
        SET r.name = $name,
            r.condition = $condition,
            r.action = $action,
            r.priority = $priority
        """,
        id="TM-REFUND-RULE-001",
        name="High Value Refund Approval",
        condition="refund_amount > 50000",
        action="manager_approval_required",
        priority=1,
    )

    tx.run(
        """
        MATCH (p:Policy {id: "TM-REFUND-001"})
        MATCH (r:Rule {id: "TM-REFUND-RULE-001"})
        MERGE (p)-[:CONTAINS]->(r)
        """
    )

    tx.run(
        """
        MERGE (role:Role {id: $id})
        SET role.name = $name
        """,
        id="ROLE-CUSTOMER-OPS-MANAGER",
        name="Customer Operations Manager",
    )

    tx.run(
        """
        MATCH (r:Rule {id: "TM-REFUND-RULE-001"})
        MATCH (role:Role {id: "ROLE-CUSTOMER-OPS-MANAGER"})
        MERGE (r)-[:REQUIRES]->(role)
        """
    )


def connect_orders_to_policy(tx):
    tx.run(
        """
        MATCH (o:Order)
        MATCH (p:Policy {id: "TM-REFUND-001"})
        MERGE (o)-[:SUBJECT_TO]->(p)
        """
    )


def load_employees(tx, employees):
    for employee in employees:
        tx.run(
            """
            MERGE (e:Employee {id: $id})
            SET e.name = $name,
                e.role = $role,
                e.department = $department
            """,
            id=employee["employee_id"],
            name=employee["name"],
            role=employee["role"],
            department=employee["department"],
        )

        if employee.get("role"):
            role_id = "ROLE-" + employee["role"].upper().replace(" ", "-")

            tx.run(
                """
                MERGE (r:Role {id: $id})
                SET r.name = $name
                """,
                id=role_id,
                name=employee["role"],
            )

            tx.run(
                """
                MATCH (e:Employee {id: $employee_id})
                MATCH (r:Role {id: $role_id})
                MERGE (e)-[:HAS_ROLE]->(r)
                """,
                employee_id=employee["employee_id"],
                role_id=role_id,
            )


def load_refund_process(tx):
    tx.run(
        """
        MERGE (p:Process {id: $id})
        SET p.name = $name,
            p.description = $description
        """,
        id="PROCESS-REFUND",
        name="Refund Processing",
        description="End-to-end TechMart refund processing workflow",
    )

    tasks = [
        ("TASK-01", "Verify Customer", "verify_customer", False),
        ("TASK-02", "Retrieve Order", "retrieve_order", False),
        ("TASK-03", "Verify Refund Eligibility", "verify_refund_eligibility", False),
        ("TASK-04", "Retrieve Current Policy", "retrieve_current_policy", False),
        ("TASK-05", "Evaluate Refund Amount", "evaluate_refund_amount", False),
        ("TASK-06", "Request Manager Approval", "request_manager_approval", True),
        ("TASK-07", "Execute Refund", "execute_refund", True),
        ("TASK-08", "Update Support Ticket", "update_ticket", False),
        ("TASK-09", "Notify Customer", "notify_customer", False),
        ("TASK-10", "Create Audit Record", "create_audit_record", False),
    ]

    for task_id, name, action, requires_approval in tasks:
        tx.run(
            """
            MERGE (t:Task {id: $id})
            SET t.name = $name,
                t.action = $action,
                t.requires_approval = $requires_approval
            """,
            id=task_id,
            name=name,
            action=action,
            requires_approval=requires_approval,
        )

        tx.run(
            """
            MATCH (p:Process {id: "PROCESS-REFUND"})
            MATCH (t:Task {id: $task_id})
            MERGE (p)-[:CONTAINS]->(t)
            """,
            task_id=task_id,
        )


def load_refund_skill(tx):
    tx.run(
        """
        MERGE (s:Skill {id: $id})
        SET s.name = $name,
            s.version = $version,
            s.status = $status,
            s.risk_level = $risk_level
        """,
        id="SKILL-PROCESS-REFUND",
        name="process_refund",
        version="1.0",
        status="validated",
        risk_level="high",
    )

    tx.run(
        """
        MATCH (s:Skill {id: "SKILL-PROCESS-REFUND"})
        MATCH (p:Process {id: "PROCESS-REFUND"})
        MERGE (s)-[:IMPLEMENTS]->(p)
        """
    )


def load_refund_tool(tx):
    tx.run(
        """
        MERGE (t:Tool {id: $id})
        SET t.name = $name,
            t.type = $type
        """,
        id="TOOL-REFUND-API",
        name="Refund API",
        type="enterprise_api",
    )

    tx.run(
        """
        MATCH (s:Skill {id: "SKILL-PROCESS-REFUND"})
        MATCH (t:Tool {id: "TOOL-REFUND-API"})
        MERGE (s)-[:USES]->(t)
        """
    )


def load_graph():
    customers_path = DATA_DIR / "company" / "customers.json"
    orders_path = DATA_DIR / "company" / "orders.json"
    employees_path = DATA_DIR / "company" / "employees.json"

    with open(customers_path, "r", encoding="utf-8") as f:
        customers = json.load(f)

    with open(orders_path, "r", encoding="utf-8") as f:
        orders = json.load(f)

    with open(employees_path, "r", encoding="utf-8") as f:
        employees = json.load(f)

    driver = get_driver()

    try:
        with driver.session() as session:
            session.execute_write(load_customers, customers)
            session.execute_write(load_orders, orders)
            session.execute_write(load_refund_policy)
            session.execute_write(connect_orders_to_policy)
            session.execute_write(load_employees, employees)
            session.execute_write(load_refund_process)
            session.execute_write(load_refund_skill)
            session.execute_write(load_refund_tool)

        print("TechMart knowledge graph loaded successfully.")

    finally:
        driver.close()


if __name__ == "__main__":
    load_graph()
