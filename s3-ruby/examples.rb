#!/usr/bin/env ruby
require 'aws-sdk'

endpoint = 'https://s3.mycompany.com:8082'
credentials = Aws::SharedCredentials.new(profile_name: 'my_profile')

# Notes on certificate usage with StorageGRID Webscale
# ----------------------------------------------------
# Set ssl_verfiy_peer to true if StorageGRID's certificate is CA-signed or if you want to use a self-signed certificate
# If you use a self-signed certificate, set ssl_ca_bundle to the self-signed certificate

client = Aws::S3::Client.new(region: 'us-east-1',
    endpoint: endpoint,
    credentials: credentials,
    force_path_style: true,
    ssl_verify_peer: false,
    #ssl_ca_bundle: 'server_cert.crt'
)

# Use resource style access
s3 = Aws::S3::Resource.new(client: client)

# Bucket related operations
# -------------------------

# List buckets
s3.buckets.each do |bucket|
    puts "Bucket: #{bucket.name}"
    puts " -> created: #{bucket.creation_date}"
end

# Create bucket
s3.bucket('new-bucket').create

# Delete bucket
s3.bucket('new-bucket').delete

# Object related operations
# -------------------------

# Create Object
s3.bucket('test').object('my_object').put(
    metadata: {
        'mykey1' => 'myvalue1',
        'mykey2' => 'myvalue2'
    },
    body: 'Hello, I\'m the object\'s data!',
    # encrypt object if desired
    server_side_encryption: 'AES256'
)

# Copy existing Object
s3.bucket('test').object('copied_object').copy_from('test/my_object')

# List objects
s3.bucket('test').objects.each do |object|
    puts "Object key: #{object.key}"
    puts " -> Size: #{object.size} bytes"
    puts " -> Last modified: #{object.last_modified}"
end

# Get object
get_response = s3.bucket('test').object('my_object').get
puts "Object content: #{get_response.body.string}"

# Byte-range reads for byte 15 to 20 of the object
get_response = s3.bucket('test').object('my_object').get({
  range: "bytes=15-20"
})
puts "Object byte 15-20 content: #{get_response.body.string}"

# Get object metadata and size
metadata = s3.bucket('test').object('my_object').metadata
size = s3.bucket('test').object('my_object').content_length
puts "Object metadata: #{metadata}"
puts "Object content length: #{size}"

# Generate a pre-signed URL that is valid for one hour
url = s3.bucket('test').object('my_object').presigned_url(:get, expires_in: 3600)
puts url

# Delete object
s3.bucket('test').object('my_object')
