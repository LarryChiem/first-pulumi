"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3, ec2

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)

sg = ec2.SecurityGroup('web-server-sg', description="security group for web servers")

allow_ssh = ec2.SecurityGroupRule("AllowSSH", type="ingress", from_port=22, to_port=22, protocol="tcp", cidr_blocks=["0.0.0.0/0"], security_group_id=sg.id)

allow_http = ec2.SecurityGroupRule("AllowHTTP", type="ingress", from_port=80, to_port=80, protocol="tcp", cidr_blocks=["0.0.0.0/0"], security_group_id=sg.id)

allow_all = ec2.SecurityGroupRule("AllowAll", type="egress", from_port=0, to_port=0, protocol="-1", cidr_blocks=["0.0.0.0/0"], security_group_id=sg.id)

instance_names = ["web1", "web2", "web3"]
output_public_ip = []

for instance in instance_names:
    ec2_instance = ec2.Instance(instance,
                                ami="ami-0cf2b4e024cdb6960",
                                instance_type="t2.micro",
                                key_name="ec2privatekey",
                                vpc_security_group_ids=[sg.id],
                                tags={
                                    "Name": instance
                                })
    output_public_ip.append(ec2_instance.public_ip)

# pulumi.export('public_ip', ec2_instance.public_ip)
pulumi.export('public_ip', output_public_ip)
# pulumi.export('instance_url', pulumi.Output.concat("http://", ec2_instance.public_dns))