#!python

import pandas as pd
import sys


def compare_df(baseline: pd.DataFrame, data: pd.DataFrame) -> set[str]:
    res = set()
    for row in baseline["filename"]:
        baseline_row = baseline[baseline["filename"] == row]
        data_row = data[data["filename"] == row]

        assert len(data_row) == len(baseline_row) == 1

        if baseline_row["opt-codesize"].iloc[0] != data_row["opt-codesize"].iloc[0]:
            res.add(row)
        if baseline_row["opt-none"].iloc[0] != data_row["opt-none"].iloc[0]:
            res.add(row)
    return res

def handle_file_result(filename: str, commits: list[str], baseline: pd.DataFrame, csvs: list[pd.DataFrame]) -> pd.DataFrame:
    new_dict = {"filename": [filename]}
    baseline_row = baseline[baseline["filename"] == filename]
    assert len(baseline_row) == 1
    baseline_opt_codesize = baseline_row["opt-codesize"].iloc[0]
    baseline_opt_none = baseline_row["opt-none"].iloc[0]
    new_dict[commits[0] + "-opt-codesize"] = [baseline_opt_codesize]
    new_dict[commits[0] + "-opt-codesize-diff"] = [0]
    new_dict[commits[0] + "-opt-none"] = [baseline_opt_none]
    new_dict[commits[0] + "-opt-none-diff"] = [0]
    for csv, commit in zip(csvs[1:], commits[1:]):
        csv_row = csv[baseline["filename"] == filename]
        assert len(csv_row) == 1
        opt_codesize = csv_row["opt-codesize"].iloc[0]
        opt_none = csv_row["opt-none"].iloc[0]

        new_dict[commit + "-opt-codesize"] = [opt_codesize]
        new_dict[commit + "-opt-codesize-diff"] = [opt_codesize - baseline_opt_codesize]
        new_dict[commit + "-opt-none"] = [opt_none]
        new_dict[commit + "-opt-none-diff"] = [opt_none - baseline_opt_none]

    return pd.DataFrame(new_dict)

def run(files: list[str]):
    csvs: list[pd.DataFrame] = [pd.read_csv(file) for file in files]

    assert len(csvs) > 1, len(csvs)

    baseline: pd.DataFrame = csvs[0]


    different = set()
    for csv in csvs[1:]:
        different = different.union(different, compare_df(baseline, csv))


    commits: list[str] = [arg.split(".")[0].replace("/tmp/", "") for arg in files]

    cols: list[str] = []

    for commit in commits:
        cols.append(commit + "-opt-codesize")
        cols.append(commit + "-opt-codesize-diff")
        cols.append(commit + "-opt-none")
        cols.append(commit + "-opt-none-diff")

    result = pd.DataFrame(columns=["filename"] + cols)
    for filename in different:
        new_dict = {"filename": [filename]}
        for col in cols:
            new_dict[col] = [0]
        new_row = handle_file_result(filename, commits, baseline, csvs)
        result = pd.concat([result, new_row], ignore_index=True)

    result.to_csv(sys.stderr)
