import requests

url = 'http://127.0.0.1:8000/'

j = {
    'username': 'Denys',
    'password': 'q',
    'email': 'hromosoma235@gmail.com',
    'gender': 'F'
}

a = requests.post(url + 'registration', json=j)