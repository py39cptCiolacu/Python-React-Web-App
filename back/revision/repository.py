from sqlalchemy.orm import Session
from back.revision.model import Revision

def get_revisions(
    db: Session,
):
    return db.query(Revision).all()


def create_revision(
    db: Session,
    name: str
):
    revision = Revision(name=name)
    db.add(revision)
    db.commit()