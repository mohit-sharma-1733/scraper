from mongoengine import Document, StringField, IntField

class Property(Document):
    property_name = StringField(max_length=500)
    property_cost = StringField(max_length=500)
    property_type = StringField(max_length=500)
    property_area = StringField(max_length=500)
    property_locality = StringField(max_length=500)
    property_city = StringField(max_length=500)
    individual_property_link = StringField(max_length=1000)
