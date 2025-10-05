import boto3

ec2 = boto3.resource('ec2')

instances = ec2.create_instances(
    ImageId='ami-03aa99ddf5498ceb9', 
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='your-key-pair-name',
    SecurityGroupIds=['sg-045614e703a91e7d4'],
    UserData='''#!/bin/bash
    yum update -y
    amazon-linux-extras install docker -y
    service docker start
    usermod -a -G docker ec2-user
    docker run -d -p 80:80 your-docker-image-url
    '''
)
print(f"Instance launched: {instances[0].id}")
