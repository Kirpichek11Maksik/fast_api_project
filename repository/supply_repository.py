
from sqlalchemy import delete, select, func
from sqlalchemy.orm import Session
from database.accessor import get_db_session
from models import Device, Supply
from handlers import supply



class SupplyRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_supplies(self):
        with self.db_session() as session:
            supplies: list[Supply] = session.execute(select(Supply)).scalars().all()
        return supplies

    def get_supply(self, supply_id: int):
        query = select(Supply).where(Supply.id == supply_id)

        total_price_query = select(
            func.coalesce(func.sum(Supply.quantity * Supply.unit_price), 0)
        ).where(Supply.id == supply_id)
        with self.db_session() as session:
            supply = session.get(Supply, supply_id)
            if supply is None:
                return None
            registered = session.scalar(
                select(func.count()).select_from(Device).where(Device.supply_id == supply_id)
            )
            supply: Supply = session.execute(query).scalar_one_or_none()
            total_price = session.execute(total_price_query).scalar_one_or_none()
        return supply, {"Общая сумма поставки": total_price, "Пришло с поставки": supply.quantity, "Используемый": registered, "На складе": supply.quantity - registered,} 
 
           
            

    def get_supply_remaining(self, supply_id: int):
        with self.db_session() as session:
            supply = session.get(Supply, supply_id)
            if supply is None:
                return None
            registered = session.scalar(
                select(func.count()).select_from(Device).where(Device.supply_id == supply_id)
            )
        return {
            "ordered": supply.quantity,
            "registered": registered,
            "remaining": supply.quantity - registered,
        }


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


