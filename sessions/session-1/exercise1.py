import argparse
import boto3


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
    EC2 = boto3.resource('ec2', region)
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
