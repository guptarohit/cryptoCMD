#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Command-line interface for cryptoCMD.

Fetch and export historical cryptocurrency price data from coinmarketcap.com
directly from your terminal.

Examples
--------
  # Print a table of all-time BTC data
  cryptocmd -c BTC

  # Fetch ETH data for a date range and print as table
  cryptocmd -c ETH -f 01-01-2023 -t 31-12-2023

  # Export BTC data to a CSV file in the current directory
  cryptocmd -c BTC --all-time --output csv --save

  # Fetch BTC data in EUR and print as JSON
  cryptocmd -c BTC -f 01-01-2024 --fiat EUR --output json

  # Print the 5 most recent rows for SOL (ascending order)
  cryptocmd -c SOL --rows 5 --ascending
"""

from __future__ import print_function

import argparse
import json
import os
import sys
from datetime import datetime

from .__version__ import __version__
from .core import CmcScraper


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SUPPORTED_EXPORT_FORMATS = (
    "csv",
    "json",
    "tsv",
    "xls",
    "xlsx",
    "yaml",
    "html",
    "latex",
    "dbf",
    "ods",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _validate_date(date_str):
    # type: (str) -> str
    """Validate that a date string matches dd-mm-yyyy."""
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Invalid date '{}'. Expected format: dd-mm-yyyy (e.g. 01-01-2023)".format(
                date_str
            )
        )
    return date_str


def _print_table(headers, rows, max_rows=None):
    # type: (list, list, int | None) -> None
    """Pretty-print rows as an aligned ASCII table."""
    if max_rows is not None:
        rows = rows[:max_rows]

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    fmt = "|" + "|".join(" {:<" + str(w) + "} " for w in col_widths) + "|"

    print(sep)
    print(fmt.format(*headers))
    print(sep)
    for row in rows:
        print(fmt.format(*[str(c) for c in row]))
    print(sep)
    print("  {} row(s) displayed.".format(len(rows)))


def _print_json(headers, rows, max_rows=None):
    # type: (list, list, int | None) -> None
    """Print rows as pretty JSON."""
    if max_rows is not None:
        rows = rows[:max_rows]
    records = [dict(zip(headers, row)) for row in rows]
    print(json.dumps(records, indent=2, default=str))


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def build_parser():
    # type: () -> argparse.ArgumentParser
    parser = argparse.ArgumentParser(
        prog="cryptocmd",
        description=(
            "Fetch historical cryptocurrency price data from coinmarketcap.com "
            "and display or export it."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  cryptocmd -c BTC\n"
            "  cryptocmd -c ETH -f 01-01-2023 -t 31-12-2023\n"
            "  cryptocmd -c BTC --all-time --output csv --save\n"
            "  cryptocmd -c BTC -f 01-01-2024 --fiat EUR --output json\n"
        ),
    )

    # Required
    parser.add_argument(
        "-c",
        "--coin",
        required=True,
        metavar="COIN_CODE",
        help="Coin ticker symbol, e.g. BTC, ETH, SOL.",
    )

    # Date range
    date_group = parser.add_argument_group("Date range")
    date_group.add_argument(
        "-f",
        "--from-date",
        dest="start_date",
        metavar="DD-MM-YYYY",
        type=_validate_date,
        help="Start date (inclusive). Format: dd-mm-yyyy.",
    )
    date_group.add_argument(
        "-t",
        "--to-date",
        dest="end_date",
        metavar="DD-MM-YYYY",
        type=_validate_date,
        help="End date (inclusive). Format: dd-mm-yyyy. Defaults to today.",
    )
    date_group.add_argument(
        "--all-time",
        action="store_true",
        default=False,
        help="Fetch all available historical data (overrides -f / -t).",
    )

    # Output options
    output_group = parser.add_argument_group("Output")
    output_group.add_argument(
        "-o",
        "--output",
        default="table",
        metavar="FORMAT",
        help=(
            "Output format. Use 'table' or 'json' to print to stdout, "
            "or one of %s to save a file (requires --save). Default: table."
            % ", ".join(repr(f) for f in SUPPORTED_EXPORT_FORMATS)
        ),
    )
    output_group.add_argument(
        "--save",
        action="store_true",
        default=False,
        help=(
            "Save data to a file instead of printing. "
            "Requires a file-based --output format."
        ),
    )
    output_group.add_argument(
        "-p",
        "--path",
        dest="output_path",
        default=None,
        metavar="DIR",
        help="Directory where the output file will be saved. Defaults to current directory.",
    )
    output_group.add_argument(
        "-n",
        "--name",
        dest="output_name",
        default=None,
        metavar="FILENAME",
        help="Custom filename for the saved file (without extension).",
    )

    # Filtering & ordering
    filter_group = parser.add_argument_group("Filtering and ordering")
    filter_group.add_argument(
        "--rows",
        type=int,
        default=None,
        metavar="N",
        help="Limit output to the first N rows.",
    )
    filter_group.add_argument(
        "--ascending",
        action="store_true",
        default=False,
        help="Sort results in ascending date order (oldest first).",
    )
    filter_group.add_argument(
        "--fiat",
        default="USD",
        metavar="FIAT",
        help="Fiat currency for price data, e.g. USD, EUR, GBP. Default: USD.",
    )
    filter_group.add_argument(
        "--coin-name",
        dest="coin_name",
        default=None,
        metavar="COIN_NAME",
        help=(
            "Full coin name to disambiguate when multiple coins share the same "
            "ticker, e.g. --coin-name solana."
        ),
    )

    # Misc
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {}".format(__version__),
    )

    return parser


def main(argv=None):
    # type: (list | None) -> int
    """
    Main entry point for the ``cryptocmd`` CLI command.

    :param argv: argument list (defaults to sys.argv when None).
    :return: exit code (0 on success, non-zero on failure).
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    output_fmt = args.output.lower()

    if args.save and output_fmt in ("table", "json"):
        parser.error(
            "--save requires a file-based output format. " "Choose one of: {}".format(
                ", ".join(SUPPORTED_EXPORT_FORMATS)
            )
        )

    # Silently enable save when a file format is requested without --save flag
    if not args.save and output_fmt not in ("table", "json"):
        args.save = True

    # Build scraper
    try:
        scraper = CmcScraper(
            coin_code=args.coin.upper(),
            start_date=args.start_date,
            end_date=args.end_date,
            all_time=args.all_time,
            order_ascending=args.ascending,
            fiat=args.fiat.upper(),
            coin_name=args.coin_name,
        )
    except Exception as exc:
        print("Error initialising scraper: {}".format(exc), file=sys.stderr)
        return 1

    # Progress indicator
    if args.all_time or not (args.start_date and args.end_date):
        date_range = "all-time"
    else:
        date_range = "{} to {}".format(args.start_date, args.end_date)
    print(
        "Fetching {}/{} data ({}) ...".format(
            args.coin.upper(), args.fiat.upper(), date_range
        ),
        file=sys.stderr,
    )

    # Fetch data
    try:
        headers, rows = scraper.get_data()
    except Exception as exc:
        print("Error fetching data: {}".format(exc), file=sys.stderr)
        return 1

    if not rows:
        print("No data returned for the requested coin/date range.", file=sys.stderr)
        return 1

    # Output
    if args.save:
        try:
            scraper.export(
                format=output_fmt,
                name=args.output_name,
                path=args.output_path or os.getcwd(),
            )
            print(
                "Saved {} file to: {}".format(
                    output_fmt.upper(), args.output_path or os.getcwd()
                ),
                file=sys.stderr,
            )
        except Exception as exc:
            print("Error saving file: {}".format(exc), file=sys.stderr)
            return 1
    elif output_fmt == "json":
        _print_json(headers, rows, max_rows=args.rows)
    else:
        _print_table(headers, rows, max_rows=args.rows)

    return 0


if __name__ == "__main__":
    sys.exit(main())
