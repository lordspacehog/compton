from datetime import date
from marshmallow import Schema, fields, pprint, post_load
from marshmallow_sqlalchemy import ModelSchema
from . import models


class EventSchema(ModelSchema):
    class Meta:
        model = models.Event


class ProductSchema(Schema):

    __model__ = models.Product

    id = fields.Method('dump_id', deserialize='load_id')
    name = fields.String()
    slug = fields.String()
    description = fields.String()
    prod_type = fields.String(load_from="type", allow_none=True)
    hw_ver = fields.String(load_from="hardware_version")
    config_id = fields.String()
    platform_id = fields.Integer()
    fw_id = fields.Integer(load_from="product_id")
    organization_id = fields.String(load_from="organization")
    req_act_code = fields.Boolean(load_from="requires_activation_codes")

    def dump_id(self, obj):
        if isinstance(obj.id, str):
            if obj.id.isnumeric():
                return int(obj.id)
            return obj.id
        return obj.id

    def load_id(self, value):
        return str(value)

    @post_load
    def make_object(self, data):
        return self.__model__(**data)


class ProductDeviceSchema(Schema):
    pass


class ProductGroupSchema(Schema):
    pass


class ProductCustomerSchema(Schema):
    pass
