#!/usr/bin/env python
"""
This script uses the Boto3 library to connect to the AWS EC2 service and retrieve a list of instances with the "web" tag.
It then creates an inventory dictionary with a group called "web" and adds each instance's public IP address to the group's "hosts" list.
It also adds some Ansible-specific variables to each host in the "_meta" group so that Ansible can connect to the instances using SSH.
"""
import boto3
import json

# Connect to the AWS EC2 service
ec2 = boto3.client('ec2')

# Get all instances with the "web" tag
response = ec2.describe_instances(Filters=[
    {
        'Name': 'tag:Type',
        'Values': ['web']
    }
])

# Create an empty dictionary to hold the inventory
inventory = {
    'web': {
        'hosts': [],
        'vars': {}
    },
    '_meta': {
        'hostvars': {}
    }
}

# Loop through the instances and add them to the inventory
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        inventory['web']['hosts'].append(instance['PublicIpAddress'])
        inventory['_meta']['hostvars'][instance['PublicIpAddress']] = {
            'ansible_host': instance['PublicIpAddress'],
            'ansible_user': 'ec2-user',
            'ansible_ssh_private_key_file': '/Users/vikas.gupta/secret/ansible-test.pem'
        }

# Print the inventory as JSON
print(json.dumps(inventory))
