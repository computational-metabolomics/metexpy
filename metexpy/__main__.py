# -*- coding: utf-8 -*-

import argparse
import os
from metexpy import __version__


def main(): # pragma: no cover

    print("Executing MetExPy version %s." % __version__)

    parser = argparse.ArgumentParser(description='Python package to search, extract and rename '
                                                 'metabolite and lipid names using regular expression',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(dest='step')

    parser_r = subparsers.add_parser('rename', help='Rename metabolite and/or lipid names')

    parser_r.add_argument('-i', '--input',
                          type=str, required=True,
                          help="Path to a text file that contains a line-separated list "
                               "of metabolite and/or lipid names")

    parser_r.add_argument('-o', '--output',
                          type=str, required=True,
                          help="Path to a text file to write the new metabolite and/or lipid names")


if __name__ == "__main__":
    main()
