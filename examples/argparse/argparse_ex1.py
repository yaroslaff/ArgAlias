#!/usr/bin/env python

import argparse
from argalias import ArgAlias
import sys

def get_args():
    parser = argparse.ArgumentParser(description='argalias example')

    parser.add_argument('-v','--verbose', default=False, action='store_true', help='verbose mode')
    parser.add_argument('--level', type=int, default=0, help='debug level')
    parser.add_argument('--xy', type=int, nargs=2, default=None, help='X and Y coordinates')

    subparsers = parser.add_subparsers(dest="entity", help="Choose between 'employee' or 'project'")

    employee_parser = subparsers.add_parser("employee", help="Manage employees")
    employee_parser.add_argument('COMMAND', help='show/create/delete or short alias')
    employee_parser.add_argument('NAME', help='Employee name')

    project_parser = subparsers.add_parser("project", help="Manage employees")
    project_parser.add_argument('COMMAND', help='show/create/delete or short alias')
    project_parser.add_argument('NAME', help='Project name')

    return parser.parse_args()


def resolve_aliases():
    aa = ArgAlias()
    aa.skip_flags()
    aa.nargs('--level')
    aa.nargs('--xy', nargs=2)
    aa.alias("show", "get", "sh", "s")
    aa.alias(["employee"], "emp", "e")
    aa.alias(["project"], "proj", "p", "pr")

    aa.alias(["employee|project", "create"], "cr", "c")
    aa.alias(["*", "delete"], "del", "d")

    aa.parse()

def main():

    resolve_aliases()
    print(sys.argv)
    args = get_args()
    print(args)

if __name__ == '__main__':
    main()