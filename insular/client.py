import json
from http import HTTPStatus

from maria.client import HTTPAPIClient
from django.conf import settings


class InsularClient(HTTPAPIClient):
    BASE_URL = settings.INSULAR_URL_PROD if settings.INSULAR_PROD else settings.INSULAR_URL_STAGING

    SEND_EMAIL_FALSE = '0'
    SEND_EMAIL_TRUE = '1'

    def __init__(self, username, password):
        super(InsularClient, self).__init__(base_url=self.BASE_URL)
        self.login(username, password)

    def get_default_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            "User-Agent": "maria-useragent",
        }
        return headers

    def get_auth(self):
        return BearerAuth(self.auth['access_token'])

    def login(self, username, password):
        data = {
            'grant_type': 'client_credentials',
            'client_id': username,
            'client_secret': password,
        }
        r = self.post('/oauth/token', json=data)
        if r.status_code == HTTPStatus.OK:
            self.auth = json.loads(r.text)
        else:
            self.auth = None
            raise Exception('Unable to Authenticate')

    def get_products(self):
        r = self.get('/api/products')
        return r.json()['data']

    def get_statuses(self):
        r = self.get('/api/products')
        return r.json()['data']

    def get_provinces(self):
        r = self.get('/api/provinces')
        return r.json()['data']

    def get_city(self, province):
        r = self.get('/api/provinces/{}/cities'.format(province))
        return r.json()['data']

    def get_serial(self, serial_number):
        r = self.get('/api/voucher/{}'.format(serial_number))
        return r.json()['data']

    def get_order(self, reference_number):
        r = self.get('/api/purchase/{}'.format(reference_number))
        return r.json()['data']

    def purchase(
        self,
        reference_number,
        first_name,
        last_name,
        email,
        contact_number,
        sku,
        quantity,
        send_email=True
    ):
        data = {
            "buyer_firstname": first_name,
            "buyer_lastname": last_name,
            "buyer_email": email,
            "buyer_contact_no": contact_number,
            "send_email": self.SEND_EMAIL_TRUE if send_email else self.SEND_EMAIL_FALSE,
            "ref_no": reference_number,
            "products":  [{
                "sku": sku,
                "qty": quantity,
            }],
        }
        r = self.post('/api/purchase', json=data)
        return r.json()['data']

    def register(
        self,
        serial_number,
        lastname,
        firstname,
        birthdate,
        gender,
        civilstatus,
        streetaddress,
        citycode,
        provincecode,
        emailaddress,
        mobileno,
        send_email=True
    ):
        data = {
            "lastname": lastname,
            "firstname": firstname,
            "birthdate": birthdate,
            "gender": gender,
            "civilstatus": civilstatus,
            "streetaddress": streetaddress,
            "citycode": citycode,
            "provincecode": provincecode,
            "emailaddress": emailaddress,
            "mobileno": mobileno,
            "serialno": serial_number,
            "send_email": self.SEND_EMAIL_TRUE if send_email else self.SEND_EMAIL_FALSE,
        }
        r = self.post('/api/register', json=data)
        return r.json()['data']
