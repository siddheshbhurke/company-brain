from neo4j import GraphDatabase

from app.core.config import settings


CONSTRAINTS = [
    """
    CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
    FOR (n:Customer)
    REQUIRE n.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT order_id_unique IF NOT EXISTS
    FOR (n:Order)
    REQUIRE n.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT ticket_id_unique IF NOT EXISTS
    FOR (n:Ticket)
    REQUIRE n.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT policy_id_unique IF NOT EXISTS
    FOR (n:Policy)
    REQUIRE n.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT rule_id_unique IF NOT EXISTS
    FOR (n:Rule)
    REQUIRE n.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT process_id_unique IF NOT EXISTS
    FOR (n:Process)
    REQUIRE n.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT task_id_unique IF NOT EXISTS
    FOR (n:Task)
    REQUIRE n.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT skill_id_unique IF NOT EXISTS
    FOR (n:Skill)
    REQUIRE n.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT employee_id_unique IF NOT EXISTS
    FOR (n:Employee)
    REQUIRE n.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT role_id_unique IF NOT EXISTS
    FOR (n:Role)
    REQUIRE n.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT tool_id_unique IF NOT EXISTS
    FOR (n:Tool)
    REQUIRE n.id IS UNIQUE
    """,

    """
    CREATE CONSTRAINT document_id_unique IF NOT EXISTS
    FOR (n:Document)
    REQUIRE n.id IS UNIQUE
    """
]


def initialize_graph():
    driver = GraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(
            settings.NEO4J_USER,
            settings.NEO4J_PASSWORD
        )
    )

    try:
        with driver.session() as session:
            for constraint in CONSTRAINTS:
                session.run(constraint)

        print("Company Brain Neo4j schema initialized successfully.")

    finally:
        driver.close()


if __name__ == "__main__":
    initialize_graph()
