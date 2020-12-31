from decimal import Decimal
from http import HTTPStatus

from django.conf import settings

from maria.client import HTTPAPIClient, BearerAuth
from maria.utils import random_code

CURRENCY = 'PHP'


class BilleaseAddress(object):

    def __init__(self, country, province, city, barangay, street, address):
        self.country = country
        self.province = province
        self.city = city
        self.barangay = barangay
        self.street = street
        self.address = address

    def json(self):
        return {
            'country': self.country,
            'province': self.province,
            'city': self.city,
            'barangay': self.barangay,
            'street': self.street,
            'address': self.address,
        }


class BilleaseCustomer(object):

    def __init__(self, user_id, full_name, email, phone, address=None):
        self.internal_user_id = user_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.address = address

    def json(self):
        return {
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'internal_user_id': self.internal_user_id
        }


class BilleaseItem(object):
    ITEM_TYPE_ITEM = 'item'
    ITEM_TYPE_FEE = 'fee'

    def __init__(self, sku, label, price, quantity):
        self.code = sku
        self.item = label
        self.price = price
        self.quantity = quantity

    def json(self):
        return {
            "code": self.code,
            "item": self.item,
            "price": str(self.price),
            "quantity": self.quantity,
            "currency": CURRENCY,
            "item_type": self.ITEM_TYPE_FEE
        }


class BilleaseClient(HTTPAPIClient):

    BASE_URL = settings.BILLEASE_PROD_API_URL if settings.BILLEASE_PROD else settings.BILLEASE_STAGING_API_URL

    CHECKOUT_TYPE_STANDARD = 'standard'
    CHECKOUT_TYPE_QUICK = 'quick'
    CHECKOUT_TYPE_QR = 'qr'

    DP_TYPE_COURIER = 'cs'
    DP_TYPE_BILLEASE = 'be'
    DP_TYPE_MERCHANT = 'me'

    def __init__(self):
        super(BilleaseClient, self).__init__(base_url=self.BASE_URL)
        self.API_KEY = settings.BILLEASE_API_KEY
        self.API_SHOP_CODE = settings.BILLEASE_API_SHOP_CODE
        self.API_MERCHANT_CODE = settings.BILLEASE_API_MERCHANT_CODE
        self.API_CALLBACK_URL = settings.BILLEASE_API_CALLBACK_URL

    def get_auth(self):
        return BearerAuth(self.API_KEY)

    def get_default_headers(self):
        return None

    def ping(self):
        r = self.get('/ping')
        return r.json()

    def get_transaction_status(self, trxid):
        r = self.get('/trx/{}/status'.format(trxid))
        return r.json()

    def get_transaction(self, trxid):
        r = self.get('/trx/{}'.format(trxid))
        return r.json()

    def create_transaction(self, order_id, items, customer, url_redirect):
        items = [item.json() for item in items]
        amount = sum((Decimal(item['price']) * item['quantity'] for item in items))
        data = {
            'shop_code': self.API_SHOP_CODE,
            'merchant_code': self.API_MERCHANT_CODE,
            'checkout_type': self.CHECKOUT_TYPE_STANDARD,
            'url_redirect': url_redirect,
            'callbackapi_url': self.API_CALLBACK_URL,
            'is_async': False,
            'currency': CURRENCY,
            'amount': str(amount),
            'order_id': order_id,
            'items': items,
            'customer': customer.json()
        }
        r = self.post(
            '/trx/checkout',
            json=data
        )
        return r.json()
