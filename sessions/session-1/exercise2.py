import argparse
import boto3


EC2 = boto3.resource('ec2')


def args_parser():
    """ validate arguments and return them """
    parser = argparse.ArgumentParser(add_help=True, description="VPC Arguments")
    parser.add_argument("--region", "-r", help="Get target region",
                        required=True)
    return parser.parse_args()


def create_vpc(cidr, tenancy):
    """ Return VPC description after creation """
    response = EC2.create_vpc(CidrBlock=cidr, InstanceTenancy=tenancy)
    return response


def list_existing_vpcs(args):
    EC2_CLIENT = boto3.client('ec2', args.region)
    vpc_ids=[]
    try:
        response = EC2_CLIENT.describe_vpcs()
        i = 0
        while i < len(response['Vpcs']):
            print(f"List of VPCs: \nVpcId: {response['Vpcs'][i]['VpcId']}")
            vpc_ids.append(response['Vpcs'][i]['VpcId'])
            i += 1
    except Exception as e:
        print(e)

    return vpc_ids


def select_vpc(vpc_ids):
    """ Retrun a selected vpc id chosen by user """
    print("Select vpc to act on:")
    for vpc_id in vpc_ids:
        print(vpc_id)
    id_selected = input("Enter id: ")
    return id_selected


def create_internet_gateway():
    """ Return description of created internet gateway """
    response = EC2.create_internet_gateway()
    return response


def attach_internet_getaway(selected_vpc, ig):
    try:
        ig.attach_to_vpc(VpcId=selected_vpc)
        print(ig.id)
    except Exception as e:
        print(e)


def create_dhcp_options():
    """ Return description of created dhcp options """
    response = EC2.create_dhcp_options(
        DhcpConfigurations=[
            {
                'Key': 'domain-name-servers',
                'Values': [
                    '10.21.0.10',
                    '10.21.2.10',
                ],
            },
        ],
    )
    return response


def attach_dhcp_to_vpc(selected_vpc, dhcp_options):
    """ Return description of created dhcp options """
    response = dhcp_options.associate_with_vpc(
        VpcId=selected_vpc
    )
    return response


def main(args):
    vpc_ids = list_existing_vpcs(args)
    selected_vpc = select_vpc(vpc_ids)
    ig = create_internet_gateway()
    attach_internet_getaway(selected_vpc, ig)
    dhcp_options = create_dhcp_options()
    attach_dhcp_to_vpc(selected_vpc, dhcp_options)


if __name__ == "__main__":
    args = args_parser()
    main(args)
