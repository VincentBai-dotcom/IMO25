#!/usr/bin/env python3
"""
Batch JSON to HTML Converter for IMO25 Solution Files

This script converts all JSON solution files in the run_logs directory to HTML format.
"""

import os
import glob
from pathlib import Path
from json_to_html_converter import convert_json_to_html


def main():
    """Convert all JSON files in the run_logs directory."""
    # Find all JSON files in run_logs
    json_files = glob.glob("../run_logs/*.json")

    if not json_files:
        print("No JSON files found in run_logs directory")
        return

    print(f"Found {len(json_files)} JSON files to convert:")
    for file in json_files:
        print(f"  - {file}")

    print("\nStarting conversion...")

    # Convert each file
    successful = 0
    failed = 0

    for json_file in json_files:
        print(f"\nConverting {json_file}...")
        if convert_json_to_html(json_file):
            successful += 1
        else:
            failed += 1

    print(f"\nConversion completed!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    if successful > 0:
        print(f"\nHTML files have been created in the run_logs directory.")
        print("You can open them in any web browser to view the formatted solutions.")


if __name__ == "__main__":
    main()
