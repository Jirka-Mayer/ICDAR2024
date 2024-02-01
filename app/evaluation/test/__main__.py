import argparse
import unittest
import os
import sys
import glob
import json
from .scan_corpus import scan_corpus


##########
# Parser #
##########

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(
    title="available commands",
    dest="command_name"
)

build_parser = subparsers.add_parser(
    "convert-corpus",
    aliases=[],
    help="Converts MuseScore files to MXL files in the OS Lieder corpus"
)

build_parser = subparsers.add_parser(
    "scan-corpus",
    aliases=[],
    help="Executes the evaluation function on the entire OpenScore Lieder corpus"
)


########
# Main #
########

args = parser.parse_args()

if args.command_name == "convert-corpus":
    os.chdir("datasets/OpenScore-Lieder/data")
    assert os.system(
        f"../../../musescore/musescore.AppImage -j corpus_conversion.json"
    ) == 0
elif args.command_name == "scan-corpus":
    scan_corpus()
else:
    parser.print_help()
    exit(2)