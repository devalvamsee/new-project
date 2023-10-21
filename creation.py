import boto3

def create_instance(name_prefix, instance_type, count):
    ec2 = boto3.client('ec2', region_name='ap-south-1')  # Updated region

    tags_list = [{'Key': 'Name', 'Value': f'{name_prefix}-{i}'} for i in range(1, count + 1)]
    instances = ec2.run_instances(
        ImageId='ami-0287a05f0ef0e9d9a',  # Updated AMI ID
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

def store_instance_data(instances):
    dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')  # Updated region
    table = dynamodb.Table('InstanceInfo')

    for instance in instances:
        table.put_item(
            Item={
                'InstanceId': instance['InstanceId'],
                'InstanceName': [tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'][0],
                'PrivateIp': instance['PrivateIpAddress'],
                'PublicIp': instance['PublicIpAddress']
            }
        )

try:
    instances = create_instance('app-instance', 't2.micro', 5)
    store_instance_data(instances)
except Exception as e:
    print(f"An error occurred: {e}")
