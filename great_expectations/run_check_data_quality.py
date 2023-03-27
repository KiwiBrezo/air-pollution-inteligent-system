import os

import pandas as pd

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

from evidently.test_suite import TestSuite
from evidently.tests import *

file_location = os.path.dirname(__file__)


def quality_check():
    print("--- Started check on data quality ---")

    df_current = pd.read_csv(os.path.join(file_location, "../data/processed/current_processed_data_merged.csv"))
    df_ref = pd.read_csv(os.path.join(file_location, "../data/processed/reference_processed_data_merged.csv"))

    reference = df_current.sample(n=700, replace=False)
    current = df_ref.sample(n=700, replace=False)

    report = Report(metrics=[
        DataDriftPreset(),
    ])

    report.run(reference_data=reference, current_data=current)
    report.save_html(os.path.join(file_location, "../reports/data_report.html"))

    tests = TestSuite(tests=[
        TestNumberOfColumnsWithMissingValues(),
        TestNumberOfRowsWithMissingValues(),
        TestNumberOfConstantColumns(),
        TestNumberOfDuplicatedRows(),
        TestNumberOfDuplicatedColumns(),
        TestColumnsType(),
        TestNumberOfDriftedColumns(),
    ])

    tests.run(reference_data=reference, current_data=current)
    tests.save_html(os.path.join(file_location, "../reports/data_stability.html"))

    print("     -> Done checking on data quality")


if __name__ == "__main__":
    quality_check()
