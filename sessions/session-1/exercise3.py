import argparse
import boto3


EC2 = boto3.resource('ec2')
EC2_CLIENT = boto3.client('ec2')


def create_subnet(availability_zone, cidr, vpc_id):
    """  Get availability zone, cidr and vpc id
         create a subnet and return its description
    """
    response = EC2.create_subnet(
        AvailabilityZone=availability_zone,
        CidrBlock=cidr,
        VpcId=vpc_id,
    )
    return response


def allocate_address():
    """ Allocate elastic IP address and return the response """
    response = EC2.allocate_address(
    )
    return response


def create_nat_gateway(subnet_id, eip):
    """ Get subnet id, elastic ip and creates a
        Nat gateway in the subnet id, using the
        elastic ip given
    """
    response = EC2.create_nat_gateway(
        AllocationId=eip,
        SubnetId=subnet_id
    )
    return response


def create_route_table(vpc_id):
    """ Get a vpc id and create a route table, return it's description"""
    response = EC2.create_route_table(
        VpcId=vpc_id
    )
    return response


def associate_route_table(route_table_id, subnet_id):
    """ Gets route table id and subnet id and associate the route table
        to the subnet
    """
    response = EC2.associate_route_table(
        RouteTableId=route_table_id,
        SubnetId=subnet_id
    )
    return response


def wait_for_nat_gateway(nat_gateway_id):
    """ Use waiter method to wait till the nat gateway is ready """
    waiter = EC2.get_waiter('nat_gateway_available')
    print("Starting wait loop till Nat Gateway is available")
    waiter.wait(
        NatGatewayIds=[
            nat_gateway_id,
            ],
        WaiterConfig={
            'Delay': 20,
            'MaxAttempts': 15
        }
    )


def add_nat_gateway_route(route_table_id, destination, nat_gateway_id):
    """ Gets route table id, destination(default gateway in our case)
        and nat gateway id and create a default gateway route in the
        given route table, return the response
    """
    response = EC2.create_route(
        DestinationCidrBlock=destination,
        RouteTableId=route_table_id,
        NatGatewayId=nat_gateway_id
    )
    return response


def main(args):
    print("lets start")


if __name__ == "__main__":
    main()
