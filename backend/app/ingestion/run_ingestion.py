from pathlib import Path

from app.core.database import SessionLocal
from app.ingestion.service import ingest_directory


def main():

    project_root = Path(__file__).resolve().parents[3]

    data_directory = project_root / "data"

    db = SessionLocal()

    try:

        print("=" * 60)
        print("COMPANY BRAIN INGESTION ENGINE")
        print("=" * 60)

        ingest_directory(
            db,
            data_directory
        )

        print()
        print("Ingestion completed.")

    finally:

        db.close()


if __name__ == "__main__":
    main()
