import json
from http import HTTPStatus

from django.conf import settings

from maria.client import HTTPAPIClient, BearerAuth


class AventusClient(HTTPAPIClient):

    BASE_URL = settings.AVENTUS_URL_PROD if settings.AVENTUS_PROD else settings.AVENTUS_URL_STAGING

    PRODUCT_CLASSIC = 'Classic'
    PRODUCT_ELITE = 'Elite'
    PRODUCT_PREMIUM = 'Premium'
    PRODUCT_PRESTIGE = 'Prestige'
    PRODUCT_PRIME = 'Prime'
    PRODUCT_KIDDIE_KIT = 'Kiddie Kit'
    PRODUCT_ACCESS = 'Access'

    GENDER_MALE = 'Male'
    GENDER_FEMALE = 'Female'

    def __init__(self, username, password):
        super(AventusClient, self).__init__(base_url=self.BASE_URL)
        self.login(username, password)

    def login(self, username, password):
        r = self.post(
            '/auth/loginAPI',
            data={
                'username': username,
                'password': password,
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        if r.status_code == HTTPStatus.OK:
            self.auth = json.loads(r.text)
        else:
            self.auth = None
            raise Exception('Unable to Authenticate')

    def get_auth(self):
        return BearerAuth(self.auth['access_token'])

    def place_order(
        self,
        ref_code,
        first_name,
        middle_initial,
        last_name,
        mobile_number,
        email_address,
        gender,
        birthday,
        date_applied,
        surehealth_variant,
    ):
        r = self.post(
            '/surehealth/MariaHealth',
            json={
                'refCode': ref_code,
                'SurehealthVariant': surehealth_variant,
                'FirstName': first_name,
                'MiddleInitial': middle_initial[:1],
                'LastName': last_name,
                'MobileNumber': mobile_number,
                'EmailAddress': email_address,
                'Gender': gender.title(),
                'Birthday': birthday,
                'DateApplied': date_applied,
            }
        )
        return(r)

    def search_order(self, ref_code):
        r = self.get(
            '/surehealth/MariaHealth/search',
            json={
                'refCode': ref_code,
            }
        )
        return(r)
