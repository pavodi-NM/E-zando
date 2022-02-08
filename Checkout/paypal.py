import sys
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AfAJjTbmkp4jc_x2za1Vm44HDxX3BnHwHuEw42AceArJwOw3cLissKo_UxTrHLYLBeVMVKLm2iqOZe3x"
        self.client_secret = "EDeT4O9dImJhbYrtdGBS9FgUhYOt6q4ntqNiHerjm4ALqO2Yl8bfP4fe9KdI2UZFdvPbHMpP0SAVJ3JP"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)