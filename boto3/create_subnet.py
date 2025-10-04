import boto3

ec2 = boto3.client('ec2')

def create_subnet(vpc_id, cidr_block, availability_zone):
    resp = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock=cidr_block,
        AvailabilityZone=availability_zone
    )
    subnet_id = resp['Subnet']['SubnetId']
    print(f"Created subnet {subnet_id}")
    return subnet_id

if __name__ == '__main__':
    # example usage:
    # vpc_id = 'vpc-xxxxxx'
    # subnet = create_subnet(vpc_id, '10.0.1.0/24', 'us-east-1a')
    pass
