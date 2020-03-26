# This file is meant to test the functionalities of the API built in this software.
# Official documentation: https://requests.readthedocs.io/en/master/
import requests
import json

# definitions of host and port
host = 'localhost'
port = 4000

fail = False # keeps track if any of the tests had failed

# step 1: get the token
reply = requests.get(f'http://{host}:{port}/api/token/public')
if reply.status_code == 200:
    print('request successful')
    auth = reply.json()
    token = auth['token']
    print('My authentication token is:', token)
else:
    print('request was not successful')
    fail = True

# step 2: getting information about the web service

req_headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'
               }
reply = requests.get(f'http://{host}:{port}/api/', headers=req_headers)

print('Status:', reply.status_code)

if reply.status_code == 200:
    print(reply.json())
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True

# step 3: getting a list of posts/cars
print('\n\nGetting a list of cars')
req_headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'
              }

reply = requests.get(f'http://{host}:{port}/api/cars', headers=req_headers)

print('Code:', reply.status_code)

if reply.status_code == 200:
    for car in reply.json():
        print('Car', car['id'])
        for key, value in car.items():
            if key == 'content':
                print('\t', key.ljust(15), ':', value[:50].replace('\n', ''), '...')
            elif key == 'id':
                continue
            elif isinstance(value, dict):
                print('\t', key, ':')
                for k2, v2 in value.items():
                    print('\t\t', k2.ljust(15), ':', v2)
            else:
                print('\t', key.ljust(15), ':', value)
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True

# step 4: inserting a new post/car
print('\n\nInserting a car')
req_headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'
              }

#post = {'title': 'Define here the title of the student llllll',
 #      'content_type': 'markdown',
 #      'content': 'Define here the content you want in the post',
 #      'user': 1}

car = {'car_name': 'test car',
       'model': 'sedan',
       'license_plate': 'XXX000',
       'fuel': 100,
       'seats': 5
       }

reply = requests.post(f'http://{host}:{port}/api/cars', headers=req_headers, data=json.dumps(post))

if reply.status_code == 201:
    print('Created with success')
    car_received = reply.json()
    print('Car created:')
    car_id = car_recevied['id']
    print('\tid:', car_received['id'])
    print('\tcar name:', car_received['car_name'])
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True
else:
    print('There was an error:', reply.status_code)
    fail = True


# step 5: getting a specific post/car
print('\n\nGetting a car')
req_headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'
              }

reply = requests.get(f'http://{host}:{port}/api/car/{car_id}', headers=req_headers)

if reply.status_code == 200:
    print('Car found:')
    for key, value in reply.json().items():
        print('\t', key, ':', value)
elif reply.status_code == 404:
    print('Car not found! Try another id!')
    fail = True
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True

# step 6: replacing a post/car
print('\n\nReplacing a car')
req_headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'
              }

car = {'car_name': 'test car replaced',
       'model': 'coupe',
       'license_plate': 'OOO777',
       'fuel': 50,
       'seats': 2
       }
reply = requests.put(f'http://{host}:{port}/api/car/{car_id}', headers=req_headers, data=json.dumps(post))

if reply.status_code == 200:
    print('Replaced with success')
    post_received = reply.json()
    print('Car created:')
    print('\tid:', car_received['id'])
    print('\tcar name:', car_received['car_name'])
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True
else:
    print('There was an error:', reply.status_code)
    print(reply.text)
    fail = True

# step 7: editing a post/car
print('\n\nEditing a car')
req_headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'
              }

car = {'car_name': 'test car edited',
       'model': 'hatchback',
       'license_plate': 'III111',
       'fuel': 11,
       'seats': 7
       }

reply = requests.patch(f'http://{host}:{port}/api/car/{car_id}', headers=req_headers, data=json.dumps(post))

if reply.status_code == 200:
    print('Updated with success')
    post_received = reply.json()
    print('Car created:')
    print('\tid:', car_received['id'])
    print('\tcar name:', car_received['car_name'])
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True
else:
    print('There was an error:', reply.status_code)
    print(reply.text)
    fail = True

# step 8: deleting a post/car
print('\n\nDeleting a car')
req_headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {token}'
              }

reply = requests.delete(f'http://{host}:{port}/api/car/{car_id}', headers=req_headers)

if reply.status_code == 200:
    print('Car deleted:')
    for key, value in reply.json().items():
        print('\t', key, ':', value)
elif reply.status_code == 404:
    print('Car not found! Try another id!')
    fail = True
elif reply.status_code == 403:
    print('Your credentials have expired! Get new ones!')
    fail = True
else:
    print('Unknown error:', reply.status_code)
    fail = True
    print(reply.text)


if not fail:
    print('\n\nTHE TESTS WERE SUCCESSFUL')
else:
    print('\n\nTHE TESTS WERE NOT SUCCESSFUL')