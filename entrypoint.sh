#!/bin/sh

# Define default values for options
WORKDIR="/data"
TMPDIR="/tmp"
OUTPUT_FILE_JSON_O="${WORKDIR}/report.horusec.original.json"
OUTPUT_FILE_JSON="${WORKDIR}/report.horusec.json"

# Run the insider tool
horusec start "$@" -o json -O $OUTPUT_FILE_JSON_O --disable-docker

# Format the final json report
python /report.py -i $OUTPUT_FILE_JSON_O -o $OUTPUT_FILE_JSON

# Cleanup
rm -rf ${WORKDIR}horusec-config.json
