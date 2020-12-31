import json
import requests

from http import HTTPStatus

from django.conf import settings

from maria.client import HTTPAPIClient


class MaxicareClient(HTTPAPIClient):
    BASE_URL = settings.MAXICARE_URL_PROD if settings.MAXICARE_PROD else settings.MAXICARE_URL_STAGING

    PRODUCT_EREADY_PLATINUM = ('ZMER', 'P')
    PRODUCT_EREADY_TITANIUM = ('ZMER', 'T')
    PRODUCT_MYMAXICARE_LITE_YELLOW = ('ZLIT', 'Y')
    PRODUCT_MYMAXICARE_LITE_BLUE = ('ZLIT', 'L')
    PRODUCT_PRIMA_SILVER = ('ZPRM', 'S')
    PRODUCT_PRIMA_GOLD = ('ZPRM', 'G')

    def __init__(self, username, password):
        super(MaxicareClient, self).__init__(base_url=self.BASE_URL)
        self.login(username, password)

    def login(self, username, password):
        r = self.post('/userdata/login', data={
            'username': username,
            'password': password,
        })
        if r.status_code == HTTPStatus.OK:
            self.auth = json.loads(r.text)
        else:
            self.auth = None
            raise Exception('Unable to Authenticate')

    def order(self, email, product_type, plan_type):
        r = self.post('/orders', json={
            'email': email,
            'items': [{
                'productType': product_type,
                'planType': plan_type,
                'quantiity': 1
            }],
        }, headers={'Authorization': '{}'.format(self.auth['id'])})
        res = {
            'raw': r.json(),
            'success': r.status_code == HTTPStatus.OK
        }
        if res['success']:
            res['card'] = r.json()['vouchers'][0]['cards'][0]
        return res
