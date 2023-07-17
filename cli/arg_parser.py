import json
from optparse import Option, OptionParser

from cli import parser_options

JSON_DATA = parser_options.JSON_DATA
BOOL = parser_options.BOOL
EXTEND = parser_options.EXTEND

COMMA_SEPARATED_LISTS = ['table', 'concept', 'source', 'field', 'export']


class CLIOptions(Option):
    # See : https://docs.python.org/3.8/library/optparse.html#adding-new-actions
    ACTIONS = Option.ACTIONS + (EXTEND, BOOL, JSON_DATA)
    STORE_ACTIONS = Option.STORE_ACTIONS + (EXTEND, BOOL, JSON_DATA)
    TYPED_ACTIONS = Option.TYPED_ACTIONS + (EXTEND, BOOL, JSON_DATA)
    ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + (EXTEND, BOOL, JSON_DATA)

    def take_action(self, action, dest, opt, value, values, parser):
        if action == EXTEND:
            lvalue = value.split(",")
            values.ensure_value(dest, []).extend(lvalue)
        elif action == BOOL:
            if str(value).lower() in ['t', 'true', 'y', 'yes', '']:
                setattr(values, dest, True)
            else:
                setattr(values, dest, False)
        elif action == JSON_DATA:
            setattr(values, dest, process_data(**{opt.replace('--', ''): value}))
        else:
            Option.take_action(self, action, dest, opt, value, values, parser)


def process_data(
    data_file: str = None, data: str = None, params: str = None, param_file: str = None
):
    """Utility for parsing JSON data as an argument"""
    data_file = data_file or param_file
    data = data or params
    if data_file:
        with open(data_file, 'r') as json_file_obj:
            return json.load(json_file_obj)
    if data:
        return json.loads(data)
    return None


def get_cli_parser() -> OptionParser:
    """
    Return the artisanal CLI option parser pre-loaded with all the parser options.

    Options have to be maintained in :py:mod:`parser_options`
    """
    parser = OptionParser(option_class=CLIOptions)
    for item in COMMA_SEPARATED_LISTS:
        """Certain arguments were helpful to allow users to pass a single or a plural and resolve both to lists"""
        parser.add_option(f"--{item}s", action=EXTEND, help=f"A comma-separated list of {item}.")
        parser.add_option(
            f"--{item}",
            action=EXTEND,
            dest=f"{item}s",
            help=f"A {item} to add to a list of {item}s",
        )
    for opt, params in parser_options.PARSER_OPTIONS.items():
        opt = opt.replace('--', '')
        opt = f'--{opt}'
        if opt not in [x.get_opt_string() for x in parser.option_list]:
            parser.add_option(opt, **params)
    return parser
