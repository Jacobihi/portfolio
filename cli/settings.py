import os

LOG_DIR = os.environ.get("LOG_DIR", './logs')
CLI_MODULES = 'CLI_MODULES'
APPROVED_NAMESPACES = 'approved_namespaces'

colors = {
    # This is for adding visual clarity when running in a terminal that supports color
    # Drawback: certain contexts print the escape characters and do not render the color
    'black': '\u001b[30m',
    'red': '\u001b[31m',
    'green': '\u001b[32m',
    'yellow': '\u001b[33m',
    'blue': '\u001b[34m',
    'magenta': '\u001b[35m',
    'cyan': '\u001b[36m',
    'white': '\u001b[37m',
    'reset': '\u001b[0m',
}


def get_color_text(text: str, color: str):
    """
    Wrap the input text around color formatting
    """
    if color not in colors:
        print(f'{color} not a valid option, must be one of {", ".join(colors.keys())}')
        return text
    return f"{colors[color]}{text}{colors['reset']}"
