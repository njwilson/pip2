import argparse
import commands

parser = argparse.ArgumentParser(prog='pip2')
subparsers = parser.add_subparsers()

parser_install = subparsers.add_parser('install')
parser_install.add_argument('package_name')
parser_install.set_defaults(func=commands.install)

parser_uninstall = subparsers.add_parser('uninstall')
parser_uninstall.add_argument('package_name')
parser_uninstall.set_defaults(func=commands.uninstall)

parser_search = subparsers.add_parser('search')
parser_search.add_argument('package_name')
parser_search.set_defaults(func=commands.search)

parser_freeze = subparsers.add_parser('freeze')
parser_freeze.set_defaults(func=commands.freeze)

args = parser.parse_args()
args.func(args)
