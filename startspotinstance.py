#!/usr/bin/env python3
import boto3
import logging
import argparse
import textwrap
#
# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')
# Arguments
parser = argparse.ArgumentParser(description="Start Instance")
parser.add_argument("Name",
                    help='Start Instance Until its not stopped')
parser.add_argument("-r", "--region", help="Region")
#
args = parser.parse_args()
instanceid = args.Name
iregion = args.region
#
#filters = [{"Name":"tag:auto-delete","Values":["no"]},{"Name":"tag:awssupport:patchwork","Values":["patch"]}]
filters = [{"Name": "instance-id", "Values": [instanceid]}]
#


def lambda_handler(event, context):
    # List all regions
    client = boto3.client('ec2')
    if iregion is None:
        regions = [region['RegionName']
                   for region in client.describe_regions()['Regions']]
    else:
        regions = [iregion]
    for region in regions:
        session = boto3.Session(region_name=region)
        ec2resource = session.resource('ec2')
        instances = ec2resource.instances.filter(Filters=filters)
        for instance in instances:
            while instance.state['Name'] == 'stopped':
                print(f'Starting instance {instance.instance_id}')
                try:
                    instance.start()
                except:
                    print(f'Could not start instance {instance.instance_id}')

    #
#
lambda_handler('null', 'null')
#
# The end
#########
