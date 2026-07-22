from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.models import IngestionRun, Detection
import json


def seed():
    session: Session = SessionLocal()
    try:
        run = IngestionRun(source='sample', metadata={'notes': 'seed data'})
        session.add(run)
        session.flush()

        det = Detection(run_id=run.id, geometry={'type': 'Polygon', 'coordinates': [[[-60.0, -10.0], [-60.0, -10.1], [-59.9, -10.1], [-59.9, -10.0], [-60.0, -10.0]]]}, confidence=0.85, properties={'example': True})
        session.add(det)
        session.commit()
        print('Seeded ingestion_run id=', run.id)
    except Exception as e:
        session.rollback()
        print('Error seeding DB:', e)
    finally:
        session.close()


if __name__ == '__main__':
    seed()
