#*** Create a VPC ****
#
#- Write a script that gets 3 args: region, cidr, tenancy
#
#Example for parsing args function:
#
#hints/vpc/example_parse_args
#
#- Create the vpc with CIDR 10.21.0.0/16, in us-east-1 and tenancy default
#
#Example for creating a vpc:
#hints/vpc/example_create_vpc
#
#
#If you finished:
#
#- Use the method wait_until_available upon the vpc resource to wait until the vpc reached available state
#
#Example for setting the wait:
#
#hints/vpc/example_wait_for_vpc
#
#- Tag the VPC with name: opsschool-1
#
#No hints... Use boto documentation...
#
#- Run pylint on your code and fix the finding (pylint yourcode.py)
#If it's not already installed, here is a reference: https://www.pylint.org/

import argparse
import boto3


EC2 = boto3.resource('ec2')
EC2_CLIENT = boto3.client('ec2')

def args_parser():
    """ validate arguments and return them """
    parser = argparse.ArgumentParser(add_help=True, description="VPC Arguments")
    parser.add_argument("--region", "-r", help="Get target region",
                        required=True)
    parser.add_argument("--cidr", "-c", help="Get cidr",
                        required=True)
    parser.add_argument("--tenancy", "-t", help="Get tenancy",
                        required=True)
    return parser.parse_args()


def create_vpc(cidr, tenancy, region):
    """ Return VPC description after creation """
    response = EC2.create_vpc(CidrBlock=cidr, InstanceTenancy=tenancy)
    return response


def main(args):
    print(args.cidr)
    vpc = create_vpc(args.cidr, args.tenancy, args.region)
    print(f"VPC is created with ID:{vpc.id} \nCIDR Block: {vpc.cidr_block}")

    response = EC2_CLIENT.describe_vpcs()
    i = 0
    while i < len(response['Vpcs']):
        print(f"VpcId: {response['Vpcs'][i]['VpcId']}")
        i += 1


if __name__ == "__main__":
    args = args_parser()
    main(args)
