
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from database.database import get_db_session
from database.models import Supply
from handlers import supply

class SupplyRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_supplies(self):
        with self.db_session() as session:
            supplies: list[Supply] = session.execute(select(Supply)).scalars().all()
        return supplies

    def get_supply(self, suplly_id: int) -> Supply | None:
        query = select(Supply).where(Supply.id == suplly_id)
        with self.db_session() as session:
            supply: Supply = session.execute(query).scalar_one_or_none()
        return supply

    def create_supply(self, supply: Supply) -> Supply:
        with self.db_session() as session:
            session.add(supply)
            session.commit()
            session.refresh(supply)
        return supply


    def delete_supply(self, suplly_id: int) -> bool:
        query =  delete(Supply).where(Supply.id == suplly_id)
        with self.db_session() as session:
            result = session.execute(query)
            session.commit()
            return result.rowcount > 0

def get_suplies_repository() -> SupplyRepository:
    db_session = get_db_session()
    return SupplyRepository(db_session)

