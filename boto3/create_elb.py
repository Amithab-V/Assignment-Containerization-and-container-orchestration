import boto3

elbv2 = boto3.client('elbv2')
ec2 = boto3.client('ec2')

def create_target_group(name, vpc_id, port=5000, protocol='HTTP'):
    resp = elbv2.create_target_group(
        Name=name,
        Protocol=protocol,
        Port=port,
        VpcId=vpc_id,
        TargetType='instance'
    )
    tg_arn = resp['TargetGroups'][0]['TargetGroupArn']
    print(f"Created target group {tg_arn}")
    return tg_arn

def create_load_balancer(name, subnet_ids, security_group_ids):
    resp = elbv2.create_load_balancer(
        Name=name,
        Subnets=subnet_ids,
        SecurityGroups=security_group_ids,
        Scheme='internet-facing',
        Type='application',
        IpAddressType='ipv4'
    )
    lb_arn = resp['LoadBalancers'][0]['LoadBalancerArn']
    dns_name = resp['LoadBalancers'][0]['DNSName']
    print(f"Created load balancer {lb_arn}, DNS: {dns_name}")
    return lb_arn, dns_name

def create_listener(lb_arn, tg_arn, port=80, protocol='HTTP'):
    resp = elbv2.create_listener(
        LoadBalancerArn=lb_arn,
        Protocol=protocol,
        Port=port,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': tg_arn
            }
        ]
    )
    listener_arn = resp['Listeners'][0]['ListenerArn']
    print(f"Created listener {listener_arn}")
    return listener_arn
