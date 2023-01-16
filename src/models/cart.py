import mongoengine


class CartItem(mongoengine.Document):
    meta = {
        # 'db_alias': 'mydb',
        'collection': 'cart'
    }

    cart_uuid = mongoengine.UUIDField(primary_key=True)
    user_id = mongoengine.IntField()
    products_uuid = mongoengine.ListField(mongoengine.UUIDField())
    amount = mongoengine.IntField()
