from sqlalchemy import delete, select, func
from sqlalchemy.orm import Session
from database.models import Device
from database.database import get_db_session

class DeviceRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_devices(self):
        with self.db_session() as session:
            supplies: list[Device] = session.execute(select(Device)).scalars().all()
        return supplies

    def get_device(self, ser_num: str):
        query = select(Device).where(Device.ser_number == ser_num)
        with self.db_session() as session:
            device: Device = session.execute(query).scalar_one_or_none()
        return device

    def create_device(self, device:Device):
        with self.db_session() as session:
            session.add(device)
            session.commit()
            session.refresh(device)
        return device

    def delete_device(self, ser_num) -> bool:
        query =  delete(Device).where(Device.ser_number == ser_num)
        with self.db_session() as session:
            result = session.execute(query)
            session.commit()
        return result.rowcount > 0

def get_devices_repository() -> DeviceRepository:
    db_session = get_db_session()
    return DeviceRepository(db_session)