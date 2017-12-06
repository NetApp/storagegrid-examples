# Python Examples for accessing StorageGRID S3

## Prerequisites

First, install the necessary library for S3:
```
$ pip install boto3
```

## Connecting to StorageGRID S3

For connecting to StorageGRID S3, we first need to load the `boto3` library:
```python
import boto3
import boto3.session
```

Configure the StorageGRID S3 endpoint and profile name:
```python
session = boto3.session.Session(profile_name='my_profile')
endpoint = 'https://s3.mycompany.com:8082'
```

Now we can connect securely via HTTPS or ignore any SSL errors:
```python
# Securely via self-signed CA
s3 = session.resource(service_name='s3', endpoint_url=endpoint, verify='ca_cert.pem')

# Ignore SSL verification (do not use in production)
s3 = session.resource(service_name='s3', endpoint_url=endpoint, verify=False)

# Some boto3 calls require the client object
client = s3.meta.client
```
## Bucket Operations

Creating new buckets:
```python
bucket = s3.Bucket('new-bucket').create()
```

List all buckets for the S3 tenant:
```python
for bucket in s3.buckets.all():
    print(bucket.name)
```

Delete an empty bucket:
```python
s3.Bucket('new-bucket').delete()
```

Enable Bucket Versioning:
```python
s3.Bucket('new-bucket').Versioning().enable()

# Get Bucket Versioning status (None, Enabled, or Suspended)
print s3.Bucket('new-bucket').Versioning().status
```

Using Bucket Policies:
```python
# Load Policy from local policy.json file and attach it to bucket
with open('policy.json', 'r') as f:
    s3.BucketPolicy('my-bucket').put(Policy=f.read())
```

Remove currently active Bucket Policy from the bucket:
```python
s3.BucketPolicy('my-bucket').delete()
```

## Object Operations

Put a new object to a bucket:
```python
s3.Object('my-bucket', 'object_name.txt').put(
          Body='This is my object\'s data')
```

Put a new object with metadata and server side encryption:
```python
s3.Object('my-bucket', 'object_name.txt').put(
          Body='This is my object\'s data',
          Metadata={'customerid': '1234', 'location': 'germany'},
          ServerSideEncryption='AES256')
```

Put a new object with object tags:
```python
s3.Object('my-bucket', 'object_name.txt').put(
          Body='This is my object\'s data',
          Tagging='customerid=1234&location=germany')
```

Delete an object:
```python
s3.Object('my-bucket', 'object_name.txt').delete()

# Delete an explicit version of an object
s3.Object('my-bucket', 'object_name.txt').Version('Mzc0MzV...DAtMDAwMDAwQkFBNEM2').delete()
```

Upload/download an object directly from/to a file:
```python
s3.Object('my-bucket', 'object_name.txt').upload_file(
                '/path/to/source-file',
                ExtraArgs={'Metadata': {'customer_id': '42'},
                           'ServerSideEncryption': 'AES256'})

s3.Object('my-bucket', 'object_name.txt').download_file('/path/to/target-file')
```

Copy an existing object to a new object:
```python
s3.Object('my-bucket', 'copy.txt').copy_from(CopySource='/source-bucket/original.txt')

# Copy a specific version (if version is enabled)
s3.Object('my-bucket', 'copy.txt').copy_from(
    CopySource={'Bucket': 'source-bucket',
                'Key': 'original.txt',                
                'VersionId': 'Mzc0MzV...DAtMDAwMDAwQkFBNEM2'})
```

List all visible objects in a bucket:
```python
for o in s3.Bucket('my-bucket').objects.all():
    print("Key: " + o.key)
    print("Size: " + str(o.size))
    print("Time: " + str(o.last_modified)) 
```

List all objects (including versioned objects) in a bucket:
```python
for o in s3.Bucket('my-bucket').object_versions.all():
    print("Key: " + o.key)
    print("Version: " + o.version_id)
    print("Size: " + str(o.size))
    print("Time: " + str(o.last_modified))
    print("Is latest: " + str(o.is_latest))
```

Read object from bucket:
```python
response = s3.Object('my-bucket', 'object_name.txt').get()
data = response['Body'].read()
metadata = response['Metadata']
print("Data: %s // Metadata: %s" % (data, metadata))
```

Perform a byte-range read:
```python
# Read first 4 bytes of an object
response = s3.Object('metadata-bucket', 'object_name.txt').get(Range='bytes=0-3')

# Read byte 5 to 8 of an object
response = s3.Object('metadata-bucket', 'object_name.txt').get(Range='bytes=4-7')

# Read the last 4 bytes an object
response = s3.Object('metadata-bucket', 'object_name.txt').get(Range='bytes=-4')
```

Generate a pre-signed URL (only possible via client, not directly via Object object):
```python
url = client.generate_presigned_url('get_object', 
                                    {'Bucket': 'my-bucket', 'Key': 'object_name.txt'},
                                    ExpiresIn=3600)
print("Pre-signed URL: %s" % (url))
```

Multipart Upload via `S3Transfer` helper:
```python
from boto3.s3.transfer import TransferConfig, S3Transfer

config = TransferConfig(
    multipart_threshold = 512 * 1024 * 1024,
    multipart_chunksize = 512 * 1024 * 1024,
    max_concurrency = 10,
    num_download_attempts = 10)

transfer = S3Transfer(client, config)
transfer.upload_file('/path/to/source/file.zip', 'my-bucket', 'file.zip')
transfer.download_file('my-bucket', 'file.zip', '/path/to/destination/file.zip')
```
