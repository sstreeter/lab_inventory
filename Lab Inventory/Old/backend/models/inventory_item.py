# InventoryItem model added here
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()
class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    id = Column(Integer, primary_key=True)
    device_name = Column(String(255))
    serial_number = Column(String(255))
    lab = Column(String(255))
    image_path = Column(String(255))