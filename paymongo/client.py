from django.conf import settings

from maria.client import HTTPAPIClient


class PayMongoClient(HTTPAPIClient):

    BASE_URL = settings.PAYMONGO_API_URL

    def __init__(self):
        super(PayMongoClient, self).__init__(base_url=self.BASE_URL)
        self.SECRET_KEY = settings.PAYMONGO_SECRET_KEY
        self.PUBLIC_KEY = settings.PAYMONGO_PUBLIC_KEY

    def get_auth(self):
        return (self.SECRET_KEY, None)

    def get_default_headers(self):
        return {"Content-Type": "application/json"}

    def create_payment_intent(self, amount, description=None, statement_descriptor=None, metadata=None):
        data = {
            "data": {
                "attributes": {
                    "amount": int(amount * 100),  # amount is in cents
                    "payment_method_allowed": ["card"],
                    "payment_method_options": {"card": {"request_three_d_secure": "any"}},
                    "currency": "PHP",
                    **{
                        k: v for k, v in [
                            ("description", description),
                            ("statement_descriptor", statement_descriptor),
                            ("metadata", metadata,)
                        ] if v
                    }
                }
            }
        }

        r = self.post(
            '/payment_intents',
            json=data
        )
        return r.json()

    def get_payment_intent(self, id):
        r = self.get('/payment_intents/{}'.format(id))
        return r.json()

    def attach_payment_method(self, client_key, method_id):
        intent_id = client_key.split('_client')[0]
        data = {
            "data": {
                "attributes": {
                    "payment_method": method_id,
                }
            }
        }
        r = self.post(
            '/payment_intents/{}/attach'.format(intent_id),
            json=data
        )
        return r.json()

    def pay_amount(
        self,
        amount,
        payment_method_id,
        description=None,
        statement_descriptor=None,
        metadata=None
    ):
        pi_res = self.create_payment_intent(
            amount,
            description=description,
            statement_descriptor=statement_descriptor,
            metadata=metadata
        )
        if 'errors' in pi_res:
            return pi_res
        else:
            client_key = pi_res['data']['attributes']['client_key']
            apm_res = self.attach_payment_method(
                client_key,
                payment_method_id
            )
            return apm_res
