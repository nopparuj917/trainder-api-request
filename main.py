from random_address import random_address
import requests
import json
import random
import string
from faker import Faker
from geopy.geocoders import Nominatim
from geopy import geocoders
from random_address import real_random_address_by_state


# set the base URL of your API
BASE_URL = 'http://localhost:8080/'

ENDPOINTS_LOGIN = [
    {
        'name': 'login',
        'url': 'login',
        'method': 'POST',
        'data': {
            'username': 'test_user',
            'password': 'test_password'
        }
    },
]
ENDPOINTS_PROTECTED = [
    {
        'name': 'get_user',
        'url': 'protected/user',
        'method': 'GET',
        'auth_required': True
    },
    {
        'name': 'update_user',
        'url': 'protected/update',
        'method': 'PUT',
        'auth_required': True,
        'data': {
            'usertype': 'Trainer',
            'firstname': 'John',
            'lastname': 'Doe',
            'birthdate': '1990-01-01',
            'citizenId': '1234567890123',
            'gender': 'Male',
            'phoneNumber': '0812345678',
            'address': '123 Main Street'
        }
    }

]


def generate_address():
    res = real_random_address_by_state('CA')
    add1, add2, city, state, postal_code, coordinates = res.values()
    if add2 == "":
        address = f"{add1}, {city}, {state} {postal_code}"
    else:
        address = f"{add1}, {add2}, {city}, {state} {postal_code}"
    return address, coordinates['lat'], coordinates['lng']


def generate_user(username, user_type):
    fake = Faker()
    gender = random.choice(['Male', 'Female', 'Other'])
    first_name = fake.first_name_male() if gender == 'Male' else fake.first_name_female()
    last_name = fake.last_name()
    add, lat, lng = generate_address()
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=50)
    citizen_id = ''.join(random.choices(string.digits, k=13))
    phoneNumber = ''.join(random.choices(string.digits, k=10))
    user = {
        'username': username,
        'password': '123456789',
        'usertype': user_type,
        'firstname': first_name,
        'lastname': last_name,
        'birthdate': birthdate.strftime('%Y-%m-%d'),
        'citizenId': citizen_id,
        'gender': gender,
        'phoneNumber': phoneNumber,
        'address': add,
        'lat': lat,
        'lng': lng
    }
    return user


def test_endpoint(endpoint):
    url = BASE_URL + endpoint['url']
    data = endpoint.get('data', {})
    response = requests.request(
        endpoint['method'], url,  json=data)
    if response.status_code != 200:
        print(f'{endpoint["name"]} failed: {response.status_code}')
    else:
        print(f'{endpoint["name"]} succeeded')


def test_endpoint_protected(endpoint):
    payload = {
        'username': "test01",
        'password': "123456789"
    }
    response = requests.post(BASE_URL+"/login", json=payload)
    if response.status_code == 200:
        token = json.loads(response.text)['access_token']
        headers = {'Authorization': f'Bearer {token}'}
    else:
        print("login failed")
        return

    url = BASE_URL + endpoint['url']
    data = endpoint.get('data', {})
    response = requests.request(
        endpoint['method'], url, headers=headers, json=data)
    print(f'{endpoint["name"]} {response.status_code}')


def test_register(usertype, n):
    url = BASE_URL + 'register'
    for i in range(4):
        data = generate_user(f'{usertype}{n}0{i}', usertype)
        response = requests.request('POST', url,  json=data)
        print(i, response)


def main():
    test_register("Trainee", 2)
    pass


if __name__ == "__main__":
    main()
