import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = []
PASSWORD = os.getenv('PASSWORD')
URL_OCC = os.getenv('URL_OCC', 'https://www.occ.com.mx')

i = 0
while True:
    email = os.getenv(f'EMAIL_{i}')
    if email is not None:
        EMAIL.append(email)
        i+=1
    else:
        break