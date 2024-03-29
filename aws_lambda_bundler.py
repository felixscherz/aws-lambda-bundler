import argparse
import subprocess
import sys
import hashlib
from pathlib import Path
from typing import Optional

AWS_LAMBDA_BUNDLER_DEFAULT_APP = ".aws_lambda_bundler"


def _install_to_dir(
    python: str, target_dir: Path, dependencies: list[str], index_url=None, platform=None, requirements=None
):
    cmd = [python, "-m", "pip", "install", "-t", target_dir.as_posix()]
    if index_url:
        cmd += ["--index-url", index_url]
    if platform:
        cmd += ["--platform", platform, "--only-binary", ":all:"]
    if requirements:
        cmd += ["-r", requirements]
    cmd += dependencies
    p = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(f"using interpreter {python} to run pip and install dependencies...", file=sys.stderr)
    print(f"installing dependencies to {target_dir.absolute().as_posix()}", file=sys.stderr)
    if not p.returncode == 0:
        print("pip failed to install dependencies:", file=sys.stderr)
        print(p.stderr, file=sys.stderr)
        sys.exit(p.returncode)


def _zip_dir(output: Path, dir: Path):
    p = subprocess.run(
        ["zip", "-r", output.absolute().as_posix(), "."],
        cwd=dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(
        f"zipping contents of {dir.absolute().as_posix()} to {output.absolute().as_posix()}",
        file=sys.stderr,
    )
    if not p.returncode == 0:
        print(p.stderr, file=sys.stderr)
        sys.exit(p.returncode)

def _generate_dirname(app_dir: Path, dependencies: list[str], requirements: Optional[str] = None) -> Path:
    key = hashlib.md5("".join(dependencies).encode())
    if requirements:
        with open(requirements,"rb") as handle:
            key.update(handle.read())

    return  app_dir / key.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--app-dir", default=AWS_LAMBDA_BUNDLER_DEFAULT_APP)
    parser.add_argument("--output", required=True)
    parser.add_argument("--interpreter", required=False, default=sys.executable, help="path to the python interpreter")
    parser.add_argument("--index-url", required=False, help="index url to pass on to pip")
    parser.add_argument("--platform", required=False, help="install only wheel compatible with <platform>")
    parser.add_argument("--requirements", "-r", required=False, help="requirements file passed on to pip")
    parser.add_argument("dependencies", nargs="*")
    args = parser.parse_args()

    app_dir = Path(args.app_dir)
    if not app_dir.is_dir():
        app_dir.mkdir(parents=True)

    python = args.interpreter
    dependencies: list[str] = args.dependencies
    platform = args.platform
    index_url = args.index_url
    requirements = args.requirements

    if not requirements and not dependencies:
        print("must at least specify one of --requirements or dependencies", file=sys.stderr)

    target_dir = _generate_dirname(app_dir, dependencies, requirements)

    if not target_dir.is_dir():
        _install_to_dir(
            python=python,
            target_dir=target_dir,
            dependencies=dependencies,
            index_url=index_url,
            platform=platform,
            requirements=requirements,
        )


    output = Path(args.output)
    _zip_dir(output=output, dir=target_dir)

    sys.stdout.write(f"{output.absolute().as_posix()}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
