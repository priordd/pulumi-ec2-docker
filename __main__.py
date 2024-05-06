"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import pulumi_docker as docker

size = "t2.micro"

ami = aws.ec2.get_ami(
    owners=["099720109477"],  # The AWS account ID for Canonical
    most_recent=True,
    filters=[
        aws.ec2.GetAmiFilterArgs(
            name="name",
            values=["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"],
        ),
        aws.ec2.GetAmiFilterArgs(
            name="architecture",
            values=["x86_64"],
        ),
        aws.ec2.GetAmiFilterArgs(
            name="root-device-type",
            values=["ebs"],
        ),
    ],
)

security_group = aws.ec2.SecurityGroup(
    "securitygroup",
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": ["0.0.0.0/0"],
        },
        {
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "cidr_blocks": ["0.0.0.0/0"],
        },
        # {
        #     "protocol": "tcp",
        #     "from_port": 2376,
        #     "to_port": 2376,
        #     "cidr_blocks": ["0.0.0.0/0"],
        # },
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}
    ],
)

user_data = """#!/bin/bash
sudo apt update
sudo apt upgrade -y
sudo apt install docker.io -y
"""

# Create a new EC2 instance
ec2_instance = aws.ec2.Instance(
    "rpb-demo-ec2",
    ami=ami.id,
    instance_type=size,
    associate_public_ip_address=True,
    vpc_security_group_ids=[security_group.id],
    # key_name=pulumi.Config().require("sshKeyName"),
    user_data=user_data,
)

# # Using the Docker provider to connect to the created EC2 instance
# docker_provider = docker.Provider(
#     "dockerProvider",
#     host=pulumi.Output.concat("tcp://", ec2_instance.public_ip, ":2376"),
#     # Depending on your setup, you might need to use additional configuration properties like `caMaterial`, `certMaterial`, and `keyMaterial`
# )

# # Create a Docker container on the EC2 instance
# app_container = docker.Container(
#     "appContainer",
#     image="nginx",  # Replace with your desired Docker image
#     ports=[
#         docker.ContainerPortArgs(
#             internal=80,
#             external=80,
#         )
#     ],
#     opts=pulumi.ResourceOptions(provider=docker_provider),
# )


pulumi.export("public_ip", ec2_instance.public_ip)
pulumi.export("public_dns", ec2_instance.public_dns)
pulumi.export("instance_id", ec2_instance.id)
