import boto3

def create_instance(name_prefix, instance_type, count):
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    
    tags_list = [{'Key': 'Name', 'Value': f'{name_prefix}'}]
    instances = ec2.run_instances(
        ImageId='ami-0287a05f0ef0e9d9a',
        InstanceType=instance_type,
        MinCount=count,
        MaxCount=count,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': tags_list
            },
        ]
    )
    return instances['Instances']

def update_instance_names(instances):
    ec2 = boto3.resource('ec2', region_name='ap-south-1')
    for i, instance in enumerate(instances, start=1):
        ec2_instance = ec2.Instance(instance['InstanceId'])
        ec2_instance.create_tags(
            Tags=[{'Key': 'Name', 'Value': f"{instance['Tags'][0]['Value']}-{i}"}]
        )

def store_instance_data(instances):
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
    table = dynamodb.Table('InstanceInfo')
    
    for instance in instances:
        public_ip = instance.get('PublicIpAddress', 'N/A')  # Handle missing PublicIpAddress
        table.put_item(
            Item={
                'InstanceId': instance['InstanceId'],
                'InstanceName': [tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'][0],
                'PrivateIp': instance['PrivateIpAddress'],
                'PublicIp': public_ip  # Use the default value if PublicIpAddress is missing
            }
        )

try:
    instances = create_instance('app-instance', 't2.micro', 5)
    update_instance_names(instances)
    store_instance_data(instances)
except Exception as e:
    print(f"An error occurred: {e}")
