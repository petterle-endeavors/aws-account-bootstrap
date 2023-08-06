.PHONY: all
all:

deploy-all:
	cdk deploy --all --require-approval never

unit-test:
	python3 -m pytest -vv tests/unit --cov=taiservice --cov-report=term-missing --cov-report=xml:test-reports/coverage.xml --cov-report=html:test-reports/coverage

functional-test:
	python3 -m pytest -vv tests/functional --cov=taiservice --cov-report=term-missing --cov-report=xml:test-reports/coverage.xml --cov-report=html:test-reports/coverage

full-test: unit-test functional-test

test-deploy-all: full-test deploy-all

publish:
	projen
	@echo 'Please enter your MYPI API key: '; read -s MYPI_API_TOKEN; poetry config pypi-token.pypi $$MYPI_API_TOKEN
	poetry build
	@read -p 'Are you sure you want to publish this package? [y/n]: ' REPLY; if [ $$REPLY = 'y' ]; then poetry publish; fi
