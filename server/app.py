# TODO:

from dotenv import load_dotenv
import os

from endpoints.data_import import fetch_data_year
from utils.utils import authenticate_service_account, print_json

load_dotenv()

PRIVATE_KEY_PATH = os.getenv('PRIVATE_KEY_PATH')
SERVICE_ACCOUNT = os.getenv('SERVICE_ACCOUNT')

authenticate_service_account(SERVICE_ACCOUNT, PRIVATE_KEY_PATH)
data = fetch_data_year(37.7749, -122.4194, '2021')

print_json(data)
