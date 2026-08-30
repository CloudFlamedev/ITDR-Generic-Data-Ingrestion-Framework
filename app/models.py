from sqlalchemy import Column, Integer, String, JSON

from app.database import Base 


class ITDRRecord(Base):

    __tablename__ = "itdr_records" # this is the name of the table in the database

    id = Column(Integer, primary_key=True, index=True) # Unique ID for each database row.
    event_id = Column(String, nullable=False, unique=True, index=True) ## Unique identifier for each event. Used to identify duplicate events.
    source = Column(String, nullable=False) #This stores where the event came from. like- Test data, AWS, AZURE etc(CSV, JSON, XML)
    raw_data = Column(JSON, nullable=False) # Stores the complete original event data as JSON.