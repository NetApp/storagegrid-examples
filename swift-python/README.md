# Python Examples for accessing StorageGRID Swift

## Prerequisites

First, install the necessary Python library for swift:
```
$ pip install python-swiftclient
```

## Connecting to StorageGRID Swift

For connecting to StorageGRID Swift, we first need to load the `swiftclient` library:
```python
import swiftclient
```

Configure the StorageGRID Swift endpoint and credentials:
```python
username = '38774727888584148627:swiftadmin'
password = 'supersecret'
authurl = 'https://swift.mycompany.com:8083/auth/v1.0'
```

Now we can connect securely via HTTPS or ignore any SSL errors:
```python
# Securely via self-signed CA
cacert = '/path/to/server/cert'
swift = swiftclient.client.Connection(auth_version='1', user=username, key=password, cacert=cacert, authurl=authurl)

# Ignore SSL verification (do not use in production)
swift = swiftclient.client.Connection(auth_version='1', user=username, key=password, insecure=True, authurl=authurl)
```

Get authentication information:
```python
print(swift.get_auth())
```

## Container Operations

Create new container:
```python
swift.put_container("test-container")
```

List all containers and account information:
```python
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
```

Get information for a single container:
```python
response = swift.get_container("test-container")
print "Container details: ", response
```

Delete an empty container:
```python
swift.delete_container("test-container")
```

## Object Operations


Put object into container:
```python
swift.put_object("test-container", "object.txt",
    contents='This is my object\'s content',
    headers={'X-Object-Meta-CustomerID':'42',
             'X-Object-Meta-Color':'red'})
```

List contents in a container:
```python
for obj in swift.get_container("test-container")[1]:
    print "Object key: ", obj['name']
    print "Object size: ", obj['bytes']
    print "Object last modified: ", obj['last_modified']
```

Get object from container
```python
response = swift.get_object("test-container", "object.txt")
object_headers = response[0]
object_content = response[1]
print "Object headers: ", object_headers
print "Object content: ", object_content
```

Delete an object:
```python
swift.delete_object("test-container", "object.txt")
```
