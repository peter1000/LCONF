""" Validator for LCONF specification
"""
import argparse
from argparse import RawDescriptionHelpFormatter
import sys

from LCONF.MainCode import lconf_validate_file


def parse_commandline():
   """ Return the parsed commandline arguments

   Returns:
      obj: argparse.Namespace
   """
   main_parser = argparse.ArgumentParser(
      description='Validate `LCONF files`',
      formatter_class=RawDescriptionHelpFormatter,
      epilog='''EXAMPLES:
   lconf-validate path-to-first.lconf path-to-second.lconf
   '''
   )

   main_parser.add_argument(
      'in_files',
      nargs='*',
      default=[],
      help='List of files to be validates',
   )

   args = main_parser.parse_args()
   if not args.in_files:
      main_parser.print_help()
      sys.exit()

   return args


def main():
   """ main Validator entry point
   """
   args = parse_commandline()

   for path_to_lconf_file in args.in_files:
      lconf_validate_file(path_to_lconf_file)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
if __name__ == '__main__':
   main()
