import requests
from sqlalchemy import delete

url = 'http://127.0.0.1:8000/'
url_login = 'http://127.0.0.1:8000/login'

j = {
    'username': 'Denys',
    'password': 'q',
    'email': 'hromosoma235@gmail.com',
    'gender': 'F'
}

j_login = {
    'gmail': 'hromosoma235@gmail.com',
    'password': 'q'
}

a = requests.post(url + 'login', json=j_login).text
print(a)
