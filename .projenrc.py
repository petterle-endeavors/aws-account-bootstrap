from projen.awscdk import AwsCdkPythonApp
from projen.python import VenvOptions
from projen.vscode import (
    VsCode,
    VsCodeSettings,
)
from projen import (
    Project,
    Makefile,
)

VENV_DIR = ".venv"
project: Project = AwsCdkPythonApp(
    author_email="jacobpetterle+aiforu@gmail.com",
    author_name="Jacob Petterle",
    cdk_version="2.89.0",
    module_name="accountbootstrap",
    name="tai-aws-account-bootstrap",
    package_name="tai-aws-account-bootstrap",
    description="Bootstraps a new AWS account with a baseline set of resources",
    version="0.1.0",
    venv_options=VenvOptions(envdir=VENV_DIR),
    deps=[
        "pydantic[dotenv]<=1.10.11",
        "pygit2",
        "boto3",
    ],
    dev_deps=[
        "boto3-stubs[secretsmanager]",
    ],
)

make_file: Makefile = Makefile(
    project,
    "./makefile",
)
make_file.add_rule(
    targets=["deploy-all"],
    recipe=[
        "cdk deploy --all --require-approval never",
    ],
)
make_file.add_rule(
    targets=["unit-test"],
    recipe=[
        "python3 -m pytest -vv tests/unit --cov=taiservice --cov-report=term-missing --cov-report=xml:test-reports/coverage.xml --cov-report=html:test-reports/coverage",
    ]
)
make_file.add_rule(
    targets=["functional-test"],
    recipe=[
        "python3 -m pytest -vv tests/functional --cov=taiservice --cov-report=term-missing --cov-report=xml:test-reports/coverage.xml --cov-report=html:test-reports/coverage",
    ]
)
make_file.add_rule(
    targets=["full-test"],
    prerequisites=["unit-test", "functional-test"],
)
make_file.add_rule(
    targets=["test-deploy-all"],
    prerequisites=["full-test", "deploy-all"],
)

vscode = VsCode(project)

vscode_settings: VsCodeSettings = VsCodeSettings(vscode)
vscode_settings.add_setting("python.formatting.provider", "none")
vscode_settings.add_setting("python.testing.pytestEnabled", True)
vscode_settings.add_setting("python.testing.pytestArgs", ["tests"])
vscode_settings.add_setting("editor.formatOnSave", True)

project.synth()
