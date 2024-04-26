import argparse

_parser = argparse.ArgumentParser()
_parser.add_argument('-d', '--debug', action='store_true')
command_args = _parser.parse_args()