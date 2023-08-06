"""Define a base stack that provides some nice usability features."""
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_iam as iam,
)
from accountbootstrap.stack_config_models import (
    StackConfigBaseModel,
)

class BaseStack(Stack):
    """Define the stack for the TAI API service."""

    def __init__(
        self,
        scope: Construct,
        config: StackConfigBaseModel,
    ) -> None:
        """Initialize the stack for the TAI API service."""
        super().__init__(
            scope=scope,
            id=config.stack_id,
            stack_name=config.stack_name,
            description=config.description,
            env=config.deployment_settings.aws_environment,
            tags=config.tags,
            termination_protection=config.termination_protection,
        )
        self._namer = lambda name: f"{config.stack_name}-{name}"
        self._config = config
