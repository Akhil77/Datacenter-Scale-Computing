#!/usr/bin/env python3

import argparse
import os
import time
from pprint import pprint

import googleapiclient.discovery
import google.auth
import google.oauth2.service_account as service_account

#
# Use Google Service Account - See https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html#module-google.oauth2.service_account
#
credentials = service_account.Credentials.from_service_account_file(filename='service-credentials.json')
project = 'csci-5253-lab-5'
compute = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

# [START list_instances]
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None
# [END list_instances]

# [START create_instance]
def create_instance(compute, project, zone, name, bucket):
    # Get the latest Debian Jessie image.
    image_response = compute.images().getFromFamily(
        project='ubuntu-os-cloud', family='ubuntu-1804-lts').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/f1-micro" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startup-script-vm.sh'), 'r').read()
    image_url = "http://storage.googleapis.com/gce-demo-input/photo.jpg"
    image_caption = "Ready for dessert?"

    service_credentials = open(
        os.path.join(
            os.path.dirname(__file__), 'service-credentials.json'), 'r').read()
    
    vm1_launch_vm2_code = open(
        os.path.join(
            os.path.dirname(__file__), 'part3-VM-Internal.py'), 'r').read()
    
    vm2_startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startup-script.sh'), 'r').read()

    config = {
        'name': name,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            },{
                'key': 'vm2-startup-script',
                'value': vm2_startup_script
            },{
                'key': 'service-credentials',
                'value': service_credentials
            },{
                'key': 'vm1-launch-vm2-code',
                'value': vm1_launch_vm2_code
            },{
                'key': 'project',
                'value': project
            },{
                'key': 'url',
                'value': image_url
            }, {
                'key': 'text',
                'value': image_caption
            }, {
                'key': 'bucket',
                'value': bucket
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]


# [START delete_instance]
def delete_instance(compute, project, zone, name):
    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()
# [END delete_instance]


# [START wait_for_operation]
def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)
# [END wait_for_operation]


# [START run]
def main(bucket='dcsc-bucket', zone='us-west1-b', instance_name = 'dcsc-instance', wait=True):

    print('Creating instance.')

    operation = create_instance(compute, project, zone, instance_name, bucket)
    wait_for_operation(compute, project, zone, operation['name'])

    instances = list_instances(compute, project, zone)

    print('Instances in project %s and zone %s:' % (project, zone))
    for instance in instances:
        print(' - ' + instance['name'])

    print("""
Instance created.
It will take a minute or two for the instance to complete work.
""".format(bucket))

    firewall_body = {
    "name": "allow-5000",
    "allowed": [
    {   
      "IPProtocol": "tcp",
      "ports": [
        "5000"
      ]
    }
    ],
    "targetTags": [
    "allow-5000"
    ],
    "sourceRanges":[
        "0.0.0.0/0"
    ]
    }
    try:
        request = compute.firewalls().insert(project=project, body=firewall_body)
        response = request.execute()
    except:
        print("Firewall is already present")
    request = compute.instances().get(project=project, zone=zone, instance=instance_name)
    response = request.execute()
    tags_body = {
     "items": [
    "allow-5000"
    ]}
    tags_body["fingerprint"] = response["tags"]["fingerprint"]
    request = compute.instances().setTags(project=project, zone=zone, instance=instance_name, body=tags_body)
    response = request.execute()
    
    # get ip:
    request = compute.instances().get(project=project, zone=zone, instance=instance_name)
    response = request.execute()
    print("Flask running - http://" + response["networkInterfaces"][0]["accessConfigs"][0]["natIP"] + ":5000")

if __name__ == '__main__':
    project_id = 'csci-5253-lab-5'
    bucket_name='dcsc-bucket-1'
    zone='us-west1-b'
    name = 'dcsc-instance-vm1'

    main(bucket_name, zone, name)
# [END run]