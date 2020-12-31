from django.conf import settings

from maria.client import HTTPAPIClient


class PioneerClient(HTTPAPIClient):
    BASE_URL = settings.PIONEER_URL_PROD if settings.PIONEER_PROD else settings.PIONEER_URL_STAGING

    PRODUCT_TYPE_MEDICASH_DENGUE = 'MD'
    PRODUCT_TYPE_LEPTOSPIROSIS = 'ML'

    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'

    CIVIL_STATUS_SINGLE = 'S'
    CIVIL_STATUS_MARRIED = 'M'

    def __init__(self, username, password, api_key):
        super(PioneerClient, self).__init__(base_url=self.BASE_URL)
        self.login(username, password, api_key)

    def build_url(self, path):
        url = '{}{}?api_key={}'.format(
            self.base_url.format(
                self.username,
                self.password
            ),
            path,
            self.api_key
        )
        print(url)
        return url

    def get_auth(self):
        return (self.username, self.password)

    def login(self, username, password, api_key):
        self.username = username
        self.password = password
        self.api_key = api_key

    def order(
        self,
        issuance_source,
        branch_of_purchase,
        product_type,
        email,
        firstname,
        middlename,
        lastname,
        gender,
        mobileno,
        bdate,
        civ_stat,
        province,
        city,
        zipcode,
        street_brgy,
        insured_email,
        insured_firstname,
        insured_middlename,
        insured_lastname,
        insured_gender,
        insured_mobileno,
        insured_bdate,
        insured_civ_stat,
        insured_province,
        insured_city,
        insured_zipcode,
        insured_street_brgy,
        cc_email,
        bcc_email,
    ):  # spelling these all out for explicitness (instead of using kwargs)
        r = self.post('/register_medicash', json={
            'issuance_source': issuance_source,
            'branch_of_purchase': branch_of_purchase,
            'product_type': product_type,
            'email': email,
            'firstname': firstname,
            'middlename': middlename,
            'lastname': lastname,
            'gender': gender,
            'mobileno': mobileno,
            'bdate': bdate,
            'civ_stat': civ_stat,
            'province': province,
            'city': city,
            'zipcode': zipcode,
            'street_brgy': street_brgy,
            'insured_email': insured_email,
            'insured_firstname': insured_firstname,
            'insured_middlename': insured_middlename,
            'insured_lastname': insured_lastname,
            'insured_gender': insured_gender,
            'insured_mobileno': insured_mobileno,
            'insured_bdate': insured_bdate,
            'insured_civ_stat': insured_civ_stat,
            'insured_province': insured_province,
            'insured_city': insured_city,
            'insured_zipcode': insured_zipcode,
            'insured_street_brgy': insured_street_brgy,
            'cc_email': cc_email,
            'bcc_email': bcc_email,
        })
        return(r)
