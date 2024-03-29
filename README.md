# aws-lambda-bundler

[![PyPI - Version](https://img.shields.io/pypi/v/aws-lambda-bundler.svg)](https://pypi.org/project/aws-lambda-bundler)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aws-lambda-bundler.svg)](https://pypi.org/project/aws-lambda-bundler)

-----

## What is it?

`aws-lambda-bundler` is a utility to build zip archives to run AWS Lambda functions from a list of dependencies.


## Installation

```console
pip install aws-lambda-bundler
```

## Usage

```console
aws-lambda-bundler --output my-lambda.zip requests boto3
```

## License

`aws-lambda-bundler` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
