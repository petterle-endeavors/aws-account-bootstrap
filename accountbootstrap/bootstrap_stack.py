"""Define a bootstrap stack to bootstrap an AWS account."""
from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
)
from accountbootstrap.base_stack import BaseStack
from accountbootstrap.stack_config_models import (
    StackConfigBaseModel,
)


class BootstrapStack(BaseStack):
    """Define the stack for bootstrapping an AWS account."""

    def __init__(self, scope: Construct, config: StackConfigBaseModel) -> None:
        """Initialize the stack for bootstrapping an AWS account."""
        super().__init__(scope=scope, config=config)
        self._vpc = self._create_vpc()
        self._cloudtop_security_group = self._get_cloudtop_security_group()

    @property
    def vpc(self) -> ec2.Vpc:
        """Return the VPC for the stack."""
        return self._vpc

    @property
    def cloudtop_security_group(self) -> ec2.SecurityGroup:
        """Return the security group for cloudtops in the account."""
        return self._cloudtop_security_group

    def _create_vpc(self) -> ec2.Vpc:
        subnet_configurations = []
        subnet_configurations.append(
            ec2.SubnetConfiguration(
                name=self._namer("subnet-isolated"),
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
            )
        )
        subnet_configurations.append(
            ec2.SubnetConfiguration(
                name=self._namer("subnet-public"),
                subnet_type=ec2.SubnetType.PUBLIC,
            )
        )
        vpc = ec2.Vpc(
            scope=self,
            id=self._namer("vpc"),
            vpc_name=self._namer("vpc"),
            max_azs=3,
            nat_gateways=1,
            subnet_configuration=subnet_configurations,
        )
        subnets = ec2.SubnetSelection(one_per_az=True)
        ec2.InterfaceVpcEndpoint(
            scope=self,
            id="secrets-manager-endpoint",
            vpc=vpc,
            service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER,
            subnets=subnets,
        )
        return vpc

    def _get_cloudtop_security_group(self) -> ec2.SecurityGroup:
        sg = ec2.SecurityGroup(
            scope=self,
            id=self._namer("cloudtop-security-group"),
            vpc=self._vpc,
            security_group_name=self._namer("cloudtop-security-group"),
            description="Security group for connecting to cloudtops in the account.",
        )
        sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description="Allow ssh access from anywhere.",
        )
        return sg
