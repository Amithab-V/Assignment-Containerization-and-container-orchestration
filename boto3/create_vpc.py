import boto3

ec2 = boto3.client('ec2')

def create_vpc():
    resp = ec2.create_vpc(CidrBlock='10.0.0.0/16')
    vpc_id = resp['Vpc']['VpcId']
    ec2.get_waiter('vpc_available').wait(VpcIds=[vpc_id])
    # enable DNS hostname for VPC
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
    print(f"Created VPC {vpc_id}")
    return vpc_id

if __name__ == '__main__':
    create_vpc()
