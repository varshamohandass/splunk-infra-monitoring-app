import boto3
import json

# Initialize EC2 client
ec2 = boto3.client('ec2', region_name='ap-southeast-2',aws_access_key_id = 'YOUR_AWS_ACCESS_KEY', aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY')

# Get list of regions
regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
print(regions)

# Initialize dictionary to store instance details
instances_by_region = {}

# Iterate over each region
for region in regions:
    # Initialize EC2 resource for the region
    ec2_resource = boto3.resource('ec2', region_name=region,aws_access_key_id = 'YOUR_AWS_ACCESS_KEY', aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY')

    # Get running instances
    running_instances = list(ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]))
    running_count = len(running_instances)
    running_instances_details = [{'InstanceId': instance.id, 'State': instance.state['Name']} for instance in running_instances]

    # Get stopped instances
    stopped_instances = list(ec2_resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]))
    stopped_count = len(stopped_instances)
    stopped_instances_details = [{'InstanceId': instance.id, 'State': instance.state['Name']} for instance in stopped_instances]

    # Add counts to dictionary
    instances_by_region[region] = {'running_count': running_count, 'running_instances': running_instances_details, 'stopped_count': stopped_count, 'stopped_instances': stopped_instances_details}

# Convert dictionary to JSON
json_output = json.dumps(instances_by_region, indent=4)

# Print JSON output
print(json_output)