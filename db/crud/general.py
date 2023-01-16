from sqlalchemy.orm import Session

from db.db_conf import Base


def get_instance_by(db: Session, model: Base, by: str,
                    value: int | str) -> Session.query:
    val = getattr(model, by)
    return db.query(model).filter(val == value).first()


def get_all(db: Session, model: Base) -> Session.query:
    return db.query(model).all()


def add_instance(db: Session, item: Base) -> Base:
    db.add(item)
    db.commit()
    return item


def delete_instance(db: Session, item: Base) -> None:
    db.delete(item)
    db.commit()


def update_instance(db: Session, item: Base, data: dict) -> Base:
    for key, value in data.items():
        setattr(item, key, value)
    db.commit()
    return item
