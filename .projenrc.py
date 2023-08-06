from projen.awscdk import AwsCdkPythonApp
from projen.python import VenvOptions, PoetryPyproject
from projen.vscode import (
    VsCode,
    VsCodeSettings,
)
from projen import (
    Project,
    Makefile,
)

VENV_DIR = ".venv"
DEPENDENCIES = [
    "pydantic[dotenv]<=1.10.11",
    "pygit2",
    "boto3",
]
DEV_DEPENDENCIES = [
    "boto3-stubs[secretsmanager]",
]
BASE_PROJECT_OPTIONS = {
    "name": "tai-aws-account-bootstrap",
    "description": "Bootstraps a new AWS account with a baseline set of resources",
    "version": "0.1.0",
}
AUTHOR = "Jacob Petterle"
AUTHOR_EMAIL = "jacobpetterle@gmail.com"
project: AwsCdkPythonApp = AwsCdkPythonApp(
    author_name=AUTHOR,
    author_email=AUTHOR_EMAIL,
    cdk_version="2.89.0",
    module_name="accountbootstrap",
    venv_options=VenvOptions(envdir=VENV_DIR),
    deps=DEPENDENCIES,
    dev_deps=DEV_DEPENDENCIES,
    **BASE_PROJECT_OPTIONS,
)
poetry_project = PoetryPyproject(
    project=project,
    packages=["tai-aws-account-bootstrap"],
    homepage="https://github.com/tai-team-ai/tai-aws-account-bootstrap",
    authors=[AUTHOR],
    license="MIT",
    readme="README.md",
    dependencies=DEPENDENCIES,
    dev_dependencies=DEV_DEPENDENCIES,
    repository="https://github.com/tai-team-ai/tai-aws-account-bootstrap",
    **BASE_PROJECT_OPTIONS,
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
