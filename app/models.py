from sqlalchemy import Column, Integer, String, JSON

from app.database import Base


class ITDRRecord(Base):

    __tablename__ = "itdr_records"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, nullable=False, unique=True, index=True)
    source = Column(String, nullable=False)
    raw_data = Column(JSON, nullable=False)