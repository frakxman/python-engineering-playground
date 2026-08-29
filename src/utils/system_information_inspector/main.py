"""Entry point: build the report, then print it.

Run with:
    python main.py
"""
from report import build_report
from printer import print_report


def main():

    report = build_report()

    print_report(report)


if __name__ == "__main__":
    main()
