from projen.awscdk import AwsCdkPythonApp
from projen.python import VenvOptions, PoetryPyproject
from projen.vscode import (
    VsCode,
    VsCodeSettings,
)
from projen import (
    Makefile,
)


def to_requirements(dependencies: dict) -> list:
    """Converts a dictionary of dependencies to a list of requirements"""
    requirements = []
    for key, value in dependencies.items():
        dependency_str = key
        if value:
            dependency_str += "[" + ",".join(value.get("extras", [])) + "]"
            version = value.get("version")
            if version:
                dependency_str += version
        requirements.append(dependency_str)
    return requirements


def to_pypoject(dependencies: dict) -> dict:
    """Converts a dictionary of dependencies to a dictionary of pyproject dependencies"""
    pyproject = {}
    for key, value in dependencies.items():
        if value:
            version = value.get("version", "*")
            value.update({"version": version})
            dependency_str = value
        else:
            dependency_str = "*"
        pyproject[key] = dependency_str
    return pyproject


VENV_DIR = ".venv"
DEPENDENCIES = {
    "pydantic": {"extras": ["dotenv"], "version": "<=1.10.11"},
    "pygit2": "",
    "boto3": "",
    "poetry": "",
}
DEV_DEPENDENCIES = {
    "boto3-stubs": {"extras": ["secretsmanager"]},
}
BASE_PROJECT_OPTIONS = {
    "name": "tai-aws-account-bootstrap",
    "description": "Bootstraps a new AWS account with a baseline set of resources",
    "version": "0.0.0",
}
AUTHOR = "Jacob Petterle"
AUTHOR_EMAIL = "jacobpetterle@gmail.com"
MODULE_NAME = "_".join(BASE_PROJECT_OPTIONS["name"].split("-"))
project: AwsCdkPythonApp = AwsCdkPythonApp(
    author_name=AUTHOR,
    author_email=AUTHOR_EMAIL,
    cdk_version="2.89.0",
    module_name=MODULE_NAME,
    venv_options=VenvOptions(envdir=VENV_DIR),
    deps=to_requirements(DEPENDENCIES),
    dev_deps=to_requirements(DEV_DEPENDENCIES),
    **BASE_PROJECT_OPTIONS,
)
poetry_project = PoetryPyproject(
    project=project,
    homepage="https://github.com/tai-team-ai/tai-aws-account-bootstrap",
    authors=[AUTHOR],
    packages=[{"include": MODULE_NAME}],
    license="MIT",
    readme="README.md",
    dependencies=to_pypoject(DEPENDENCIES),
    dev_dependencies=to_pypoject(DEV_DEPENDENCIES),
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
make_file.add_rule(
    targets=["publish"],
    recipe=[
        "projen",
        "@echo 'Please enter your MYPI API key: '; read -s MYPI_API_TOKEN; poetry config pypi-token.pypi $$MYPI_API_TOKEN",
        "poetry build",
        "@read -p 'Are you sure you want to publish this package? [y/n]: ' REPLY; if [ $$REPLY = 'y' ]; then poetry publish; fi"
    ],
)

vscode = VsCode(project)

vscode_settings: VsCodeSettings = VsCodeSettings(vscode)
vscode_settings.add_setting("python.formatting.provider", "none")
vscode_settings.add_setting("python.testing.pytestEnabled", True)
vscode_settings.add_setting("python.testing.pytestArgs", ["tests"])
vscode_settings.add_setting("editor.formatOnSave", True)

project.synth()
