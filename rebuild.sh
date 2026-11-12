#!/bin/sh
# Re-read the official Excel (data/source/...xlsx) and rebuild every page.
cd "$(dirname "$0")" && python3 extract_sales.py && python3 build.py
