from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.ext.declarative import (
    declarative_base
)

Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    data = Column(String)
    ttl = Column(Integer)
    timestamp = Column(DateTime)
    core_id = Column(String)
    user_id = Column(String)
    version = Column(Integer)
    public = Column(Boolean)
    product_id = Column(Integer)
    device_id = Column(Integer)


class Product(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.slug = kwargs.get('slug')
        self.description = kwargs.get('description')
        self.prod_type = kwargs.get('prod_type')
        self.hw_ver = kwargs.get('hw_ver')
        self.config_id = kwargs.get('config_id')
        self.platform_id = kwargs.get('platform_id')
        self.fw_id = kwargs.get('fw_id')
        self.organization_id = kwargs.get('organization_id')
        self.req_act_code = kwargs.get('req_act_code')
