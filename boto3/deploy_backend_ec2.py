import boto3

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

def launch_instance(subnet_id, security_group_id, user_data_script, ami_id='ami-03aa99ddf5498ceb9', instance_type='t3.micro'):
    instances = ec2.create_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        SubnetId=subnet_id,
        SecurityGroupIds=[security_group_id],  # Pass as variable, not hardcoded
        UserData=user_data_script,
        MinCount=1,
        MaxCount=1
    )
    instance = instances[0]
    instance.wait_until_running()
    instance.reload()
    print(f"Launched instance {instance.id} in state {instance.state['Name']}")
    return instance.id

if __name__ == '__main__':
    # Example user_data_script to install Docker and run your container
    user_data_script = '''#!/bin/bash
    sudo apt update -y
    sudo apt install docker.io -y
    sudo systemctl start docker
    sudo docker run -d -p 80:80 your-ecr-image-uri
    '''

    # Replace with your actual subnet and security group IDs
    subnet_id = 'subnet-06bd72b2e4cb41d10'
    security_group_id = 'sg-045614e703a91e7d4'

    launch_instance(subnet_id, security_group_id, user_data_script)