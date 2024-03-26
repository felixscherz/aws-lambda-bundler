import sys
import tempfile
from pathlib import Path

import aws_lambda_bundler


def test_install_to_dir():
    dependencies = ["requests"]
    python = sys.executable
    scratch_dir = Path(tempfile.mkdtemp())
    aws_lambda_bundler._install_to_dir(python, scratch_dir, dependencies)
    assert len(list(scratch_dir.glob("*")))


def test_install_to_dir_specifying_index():
    dependencies = ["requests"]
    python = sys.executable
    scratch_dir = Path(tempfile.mkdtemp())
    aws_lambda_bundler._install_to_dir(python, scratch_dir, dependencies, index_url="https://pypi.org./simple")
    assert len(list(scratch_dir.glob("*")))


def test_install_to_dir_specifying_platform():
    dependencies = ["requests"]
    python = sys.executable
    scratch_dir = Path(tempfile.mkdtemp())
    aws_lambda_bundler._install_to_dir(python, scratch_dir, dependencies, platform="manylinux_2014_x86_64")
    assert len(list(scratch_dir.glob("*")))


def test_zip_dir():
    scratch_dir = Path(tempfile.mkdtemp())
    output = Path(tempfile.mkdtemp()) / "out.zip"

    with open(scratch_dir / "test", "w") as handle:
        handle.write("hello")

    aws_lambda_bundler._zip_dir(output=output, scratch_dir=scratch_dir)
    assert len(list(output.parent.glob("*")))
