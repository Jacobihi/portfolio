from optparse import OptionError
import os

from cli.settings import colors
from cli.logger import cleanup_old_logs
import cli.approved_namespaces
import cli.arg_parser

ROOT_DIR = os.environ.get("ROOT_DIR")
APPROVED_NAMESPACES = [
    "db"  # simply for illustrative purposes
]
pretty_names = '\n\t* '.join(
    [f"{colors['yellow']}{n}{colors['reset']}" for n in APPROVED_NAMESPACES]
)
usage = f"""To run the command line interface (cli), invoke with {colors['red']}python cli.py{colors['reset']} 

    {colors['yellow']}[namespace]{colors['reset']} {colors['blue']}[command]{colors['reset']} {colors['magenta']}[arguments]{colors['reset']}

Namespace must be one of:
    
    * {pretty_names}
    See that folder's README for more guidance.
    
    You can also pass {colors['yellow']}[namespace]{colors['reset']}  {colors['blue']}options{colors['reset']} to list available commands.
"""


parser = cli.arg_parser.get_cli_parser()
parser.usage = usage


def run_cli():
    """
    This is the main event for the Command Line Interface (CLI) module.

    Every command is structured ``python cli.py [namespace_directory] [function]``
    This CLI parser uses the optparse library to find the function within the namespace directory.

    If everyone follows setup correctly, they will have sourced cli/aliases.sh ``alias cli="python
    cli/run_cli.py"``

    ``cli`` is thus an alias for this function to run the command line interface.

    .. note:: You will have to add options to :py:mod:`cli.parser_options`

    Use ``help`` or ``options`` after any command to learn about it!

    """
    cleanup_old_logs()
    try:
        options, args = parser.parse_args()

        if len(args) > 1:
            the_module, the_function, *other_args = args

            f = cli.approved_namespaces.get_function_from_module(
                the_module, the_function
            )

            if not f:
                print(usage)
                exit()
            if 'help' in other_args or 'options' in other_args:
                if f.__doc__:
                    print(f.__doc__)
                else:
                    type_hints = {var: c.__name__ for var, c in f.__annotations__.items()}
                    arg_list = [
                        var + (f" ({type_hints.get(var, '')})" if var in type_hints else '')
                        for var in f.__code__.co_varnames[: f.__code__.co_argcount]
                    ]
                    arg_list = '\n'.join(arg_list)
                    print(f"acceptable arguments:\n{arg_list}")
                exit()
            options = options.__dict__
            options = {k: v for k, v in options.items() if v is not None}
            f(**options)
        else:
            print(usage)

    except OptionError:
        print("Unrecognized options")
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    run_cli()
