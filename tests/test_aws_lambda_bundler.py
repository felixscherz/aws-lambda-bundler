import sys
import tempfile
from pathlib import Path

import aws_lambda_bundler


def test_install_to_dir():
    dependencies = ["requests"]
    python = sys.executable
    target_dir = Path(tempfile.mkdtemp())
    aws_lambda_bundler._install_to_dir(python, target_dir, dependencies)
    assert len(list(target_dir.glob("*")))


def test_install_to_dir_specifying_index():
    dependencies = ["requests"]
    python = sys.executable
    target_dir = Path(tempfile.mkdtemp())
    aws_lambda_bundler._install_to_dir(python, target_dir, dependencies, index_url="https://pypi.org./simple")
    assert len(list(target_dir.glob("*")))


def test_install_to_dir_specifying_platform():
    dependencies = ["requests"]
    python = sys.executable
    target_dir = Path(tempfile.mkdtemp())
    aws_lambda_bundler._install_to_dir(python, target_dir, dependencies, platform="manylinux_2014_x86_64")
    assert len(list(target_dir.glob("*")))


def test_zip_dir():
    target_dir = Path(tempfile.mkdtemp())
    output = Path(tempfile.mkdtemp()) / "out.zip"

    with open(target_dir / "test", "w") as handle:
        handle.write("hello")

    aws_lambda_bundler._zip_dir(output=output, dir=target_dir)
    assert len(list(output.parent.glob("*")))
