import argparse
import subprocess
import sys
from pathlib import Path


def _install_to_dir(
    python: str, scratch_dir: Path, dependencies: list[str], index_url=None, platform=None, requirements=None
):
    cmd = [python, "-m", "pip", "install", "-t", scratch_dir.as_posix()]
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
    print(f"installing dependencies to {scratch_dir.absolute().as_posix()}", file=sys.stderr)
    if not p.returncode == 0:
        print("pip failed to install dependencies:", file=sys.stderr)
        print(p.stderr, file=sys.stderr)
        sys.exit(p.returncode)


def _zip_dir(output: Path, scratch_dir: Path):
    p = subprocess.run(
        ["zip", "-r", output.absolute().as_posix(), "."],
        cwd=scratch_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(
        f"zipping contents of {scratch_dir.absolute().as_posix()} to {output.absolute().as_posix()}",
        file=sys.stderr,
    )
    if not p.returncode == 0:
        print(p.stderr, file=sys.stderr)
        sys.exit(p.returncode)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch-dir", required=True, help="directory used to install dependencies into")
    parser.add_argument("--output", required=True)
    parser.add_argument("--interpreter", required=False, default=sys.executable, help="path to the python interpreter")
    parser.add_argument("--index-url", required=False, help="index url to pass on to pip")
    parser.add_argument("--platform", required=False, help="install only wheel compatible with <platform>")
    parser.add_argument("--requirements", "-r", required=False, help="requirements file passed on to pip")
    parser.add_argument("dependencies", nargs="*")
    args = parser.parse_args()

    python = args.interpreter
    scratch_dir: Path = Path(args.scratch_dir)
    output: Path = Path(args.output)
    if not output.is_absolute():
        output = Path.cwd().joinpath(output)
    dependencies: list[str] = args.dependencies
    platform = args.platform
    index_url = args.index_url
    requirements = args.requirements

    if not requirements and not dependencies:
        print("must at least specify one of --requirements or dependencies", file=sys.stderr)

    if not scratch_dir.is_absolute():
        scratch_dir = Path.cwd().joinpath(scratch_dir)

    _install_to_dir(
        python=python,
        scratch_dir=scratch_dir,
        dependencies=dependencies,
        index_url=index_url,
        platform=platform,
        requirements=requirements,
    )
    _zip_dir(output=output, scratch_dir=scratch_dir)

    sys.stdout.write(f"{output.absolute().as_posix()}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
