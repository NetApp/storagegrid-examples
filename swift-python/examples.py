# See README.md for more examples

import swiftclient

username = '38774727888584148627:swiftadmin'
password = 'supersecret'
authurl = 'https://swift.mycompany.com:8083/auth/v1.0'

swift = swiftclient.client.Connection(auth_version='1', user=username, key=password, insecure=True, authurl=authurl)

'''
If you are using self-signed certificates, you can use the following code:

cacert = '/path/to/server/cert'
swift = swiftclient.client.Connection(auth_version='1', user=username, key=password, cacert=cacert, authurl=authurl)
'''

container = 'test-container'
obj_key = 'test-object'

# Get authentication information
print(swift.get_auth())

# Create container
swift.put_container(container)

# List all containers and account information
response = swift.get_account()
account_info = response[0]
containers = response[1]

print "Bytes used by account: ", account_info['x-account-bytes-used']
print "Number of containers in account: ", account_info['x-account-container-count']
print "Number of objects in account: ", account_info['x-account-object-count']

for c in containers:
    name = c['name']
    num_objects = c['count']
    size = c['bytes']
    print("Container name: %s (total: %s objects, %s bytes)" % (name, num_objects, size))

# Get information of a single container
response = swift.get_container(container)
print "Container: ", response

# Put object into container
swift.put_object(container, obj_key,
    contents='This is my object\'s content',
    headers={'X-Object-Meta-CustomerID':'42',
             'X-Object-Meta-Color':'red'})

# List contents of a container
for obj in swift.get_container(container)[1]:
    print "Object key: ", obj['name']
    print "Object size: ", obj['bytes']
    print "Object last modified: ", obj['last_modified']

# Get object from container
response = swift.get_object(container, obj_key)
object_headers = response[0]
object_content = response[1]
print "Object headers: ", object_headers
print "Object content: ", object_content

# Delete object
swift.delete_object(container, obj_key)

# Delete container
swift.delete_container(container)
