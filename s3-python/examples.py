import boto3
import boto3.session

session = boto3.session.Session(profile_name='my_profile')
endpoint = 'https://s3.mycompany.com:8082'

'''
Do not use this in production - disabling SSL verification is discouraged!
When using a self-signed certificate, make sure to pass it into the constructor:

s3 = session.resource(service_name='s3', endpoint_url=endpoint, verify='server_cert.pem')
'''

s3 = session.resource(service_name='s3', endpoint_url=endpoint, verify=False)
client = s3.meta.client

'''
Bucket related operations
'''

# Create new bucket for S3 account
s3.Bucket('my-bucket').create()

# List all buckets for S3 account
for bucket in s3.buckets.all():
    print(bucket.name)

# Delete bucket
s3.Bucket('my-bucket').delete()

'''
Object related operations
'''

# Put a new object to a bucket
obj = s3.Object('test', 'my-key')
obj.put(Body='This is my object\'s data',
        Metadata={'customerid': '1234', 'location': 'germany'},
        ServerSideEncryption='AES256')

# Put object directly from a file
obj.upload_file('source-file', ExtraArgs={'Metadata': {'customer_id': '42'}, 'ServerSideEncryption': 'AES256'})

# Get an object directly to a file
obj.download_file('target-file')

# Copy an existing object
copied_obj = s3.Object('test', 'my-copied-key')
copied_obj.copy_from(CopySource='/test/my-key')

# Get object from bucket
response = obj.get()
data = response['Body'].read()
metadata = response['Metadata']
print("Data: %s // Metadata: %s" % (data, metadata))

# List all objects for a bucket
for obj in s3.Bucket('test').objects.all():
    print(obj.key)

# Generate a pre-signed URL (only possible via client, not directly via Object object)
url = client.generate_presigned_url('get_object', {'Bucket': 'test', 'Key': 'my-key'}, ExpiresIn=3600)
print("Pre-signed URL: %s" % (url))

# Delete the object from its bucket
obj.delete()

# Create versioned bucket
bucket = s3.Bucket('versioned-bucket')
bucket.create()
bucket.Versioning().enable()

# Check versioning status
print bucket.Versioning().status

# List all objects, including older versions in bucket
for o in bucket.object_versions.all():
    print("Key: " + o.key)
    print("Version: " + o.version_id)
    print("Size: " + str(o.size))
    print("Timestamp: " + str(o.last_modified))
    print("IsLatest: " + str(o.is_latest))

# Read older version of an object
obj = bucket.Object('object-key').Version('Mzc0MzVGNjItNjNBNS0xMUU2LTgwMDAtMDAwMDAwQkFBNEM2')
response = obj.get()
data = response['Body'].read()
print("Data: " + data)

# Restore older version to new object
obj = bucket.Object('restored_old_version')
obj.copy_from(CopySource={'Bucket': 'versioned-bucket',
                          'Key': 'object-key',
                          'VersionId': 'Mzc0MzVGNjItNjNBNS0xMUU2LTgwMDAtMDAwMDAwQkFBNEM2'})

# Delete version of object forever
bucket.Object('object-key').Version('Mzc0MzVGNjItNjNBNS0xMUU2LTgwMDAtMDAwMDAwQkFBNEM2').delete()
