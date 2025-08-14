# Check size
utility scripts for checking the sizes of contracts between the different commits/branches. Final output is created as `csv` file. All sizes are measured with `char` count (`wc -c`).

## Usage
To run all scripts install dependencies from `requirements.txt`

Create data and generate diff
```sh
python check.py "/path/to/env/activate" "/path/to/vyperdir/" "/path/to/tests/" commit1 commit2 ...
```

Only create data (if the commit contains '/' it will be replaced by '-'). Data will be stored in `/tmp`
```sh
CHECK_PYENV=env_dir VYPER_DIR=vyper_dir TEST_DIR=test_dir ./check.sh commit1 commit2 ...
```

Generate diff
```sh
python sizediff.py commit1.tmp.csv commit2.tmp.csv ...
```

I recommend to create the helper script that feeds the places for the environment, vyper directory and test directory to the `check.py`.
