"""Console presentation for a report dict.
 
Owns *only* formatting/output. It has no opinion on where the data
came from — that's `report.py`'s job — which keeps this module
reusable for any dict of string labels to string values.
"""
def print_report(report: dict) -> None:
    """Print a report dict to the console in an aligned, bordered layout.
 
    Args:
        report: Mapping of labels to values, as produced by
            `report.build_report()`.
    """

    width = max(len(key) for key in report)

    print("=" * 60)
    print("        SYSTEM INFORMATION INSPECTOR")
    print("=" * 60)

    for key, value in report.items():

        print(f"{key.ljust(width)} : {value}")

    print("=" * 60)