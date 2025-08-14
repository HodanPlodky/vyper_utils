import sys
import subprocess
import sizediff

def create_data(pyenv: str, vyper_dir: str, tests_dir: str, commits: list[str]):
    env = {
        "CHECK_PYENV":pyenv,
        "VYPER_DIR":vyper_dir,
        "TEST_DIR":tests_dir
    };
    subprocess.run([f"./check.sh", *commits], env=env)


args = sys.argv
commits = args[4:]
pyenv = args[1]
vyper_dir = args[2]
tests_dir = args[3]

create_data(pyenv, vyper_dir, tests_dir, commits)

files = ["/tmp/"+ commit.replace("/", "-") + ".tmp.csv" for commit in commits]

sizediff.run(files)
