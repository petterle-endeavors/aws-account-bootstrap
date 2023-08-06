"""Create the bootstrap application."""
from aws_cdk import App, RemovalPolicy

from accountbootstrap.bootstrap_stack import BootstrapStack
from accountbootstrap.stack_config_models import (
    AWSDeploymentSettings,
    DeploymentType,
    StackConfigBaseModel,
)


AWS_DEPLOYMENT_SETTINGS = AWSDeploymentSettings()
is_prod_deployment = AWS_DEPLOYMENT_SETTINGS.deployment_type == DeploymentType.PROD
TERMINATION_PROTECTION = True if is_prod_deployment else False
REMOVAL_POLICY = RemovalPolicy.RETAIN if is_prod_deployment else RemovalPolicy.DESTROY
TAGS = {'blame': 'jacob'}
BASE_SETTINGS = {
    "deployment_settings": AWS_DEPLOYMENT_SETTINGS,
    "termination_protection": TERMINATION_PROTECTION,
    "removal_policy": REMOVAL_POLICY,
    "tags": TAGS,
}

app: App = App()

bootstrap_stack_config = StackConfigBaseModel(
	stack_id="account-bootstrap",
	stack_name="account-bootstrap",
	description="Stack for bootstrapping the aws account. This sets up a vpc and other resources that are needed for the account.",
    duplicate_stack_for_development=False,
    **BASE_SETTINGS,
)
bootstrap_stack = BootstrapStack(
    scope=app,
    config=bootstrap_stack_config,
)

app.synth()
