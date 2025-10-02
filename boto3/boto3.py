import boto3

ec2_client = boto3.client('ec2')
autoscaling_client = boto3.client('autoscaling')

# --- Configuration ---
AMI_ID = 'ami-03aa99ddf5498ceb9'  # Replace with a valid Amazon Linux 2 AMI
INSTANCE_TYPE = 't2.micro'
KEY_NAME = 'Amithab_OCC'  # Replace with your key pair name
SECURITY_GROUP_ID = 'sg-045614e703a91e7d4'  # Replace with your security group
IAM_INSTANCE_PROFILE = 'amithab_occ_BE'  # Name, not ARN
DOCKER_IMAGE = 'assignment-containerization-and-container-orchestration-backend:latest'  # Or ECR
REGION = 'us-west-2'

LAUNCH_TEMPLATE_NAME = 'Amithab_cco_be_launch_template'
ASG_NAME = 'Amithab_cco_fr_asg'

# --- User data script to install Docker and run app ---
USER_DATA = f"""#!/bin/bash
yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user
docker run -d -p 80:80 {DOCKER_IMAGE}
"""

# --- 1. Create Launch Template ---
response = ec2_client.create_launch_template(
    LaunchTemplateName=LAUNCH_TEMPLATE_NAME,
    LaunchTemplateData={
        'ImageId': AMI_ID,
        'InstanceType': INSTANCE_TYPE,
        'KeyName': KEY_NAME,
        'SecurityGroupIds': [SECURITY_GROUP_ID],
        'IamInstanceProfile': {
            'Name': IAM_INSTANCE_PROFILE
        },
        'UserData': USER_DATA.encode('utf-8').decode('utf-8'),
        'TagSpecifications': [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': 'Amithab_cco_fr'}
                ]
            }
        ]
    }
)

launch_template_id = response['LaunchTemplate']['LaunchTemplateId']
print(f"Launch Template Created: {launch_template_id}")

# --- 2. Create Auto Scaling Group ---
autoscaling_client.create_auto_scaling_group(
    AutoScalingGroupName=ASG_NAME,
    LaunchTemplate={
        'LaunchTemplateId': launch_template_id,
        'Version': '$Latest'
    },
    MinSize=1,
    MaxSize=3,
    DesiredCapacity=1,
    VPCZoneIdentifier='subnet-0abc12345def67890,subnet-0123456789abcdef0',  # Replace with valid subnet IDs
    Tags=[
        {
            'ResourceId': ASG_NAME,
            'ResourceType': 'auto-scaling-group',
            'Key': 'Name',
            'Value': 'Amithab_cco_fr',
            'PropagateAtLaunch': True
        }
    ]
)

print("Auto Scaling Group Created")
