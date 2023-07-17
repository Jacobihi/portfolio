from inspect import getmembers, isfunction
from cli.settings import colors


class ApprovedNamespace:
    """
    An approved namespace is an allow-listed namespace (i.e., directory/folder) that semantically groups modules containing functions .

    It simplifies the execution of  commands from the command line by grouping commands into semantic arguments.
    Then, each function can be retrieved without knowing the specific details of the command's location.

    """

    def __init__(self, name: str):
        """
        :param name: The relative namespace (directory) of the namespace.
        """
        self.name = name
        self.namespace_package = __import__(self.name, globals(), locals(), ["approved_modules"])
        self.approved_modules = getattr(self.namespace_package, "approved_modules")
        self.modules = getattr(self.approved_modules, "CLI_MODULES")
        self.namespace_package = __import__(self.name, globals(), locals(), self.modules)

    def get_functions(self, a_function: str = None):
        """
        :param a_function: an optional filter of a function name to retrieve. If not specified, all functions returned
        :return: either a function or a dict {"mod": [functions]}
        """
        attrs = {}
        for mod in self.modules:
            attrs[mod] = []
            my_module = getattr(self.namespace_package, mod)
            functions = getmembers(my_module, isfunction)
            for name, method in functions:
                if name not in FORBIDDEN_MEMBERS and not name.startswith('_'):
                    if a_function and name == a_function:
                        return method
                    attrs[mod].append(name)
        return attrs


def get_function_from_module(a_namespace: str, a_function: str) -> callable:
    """
    Given the namespace from the CLI and the function as arguments, find the namespace and then find the function within it.
    """
    try:
        namespace_package = __import__(a_namespace, globals(), locals(), ["approved_modules"])
        approved_modules = getattr(namespace_package, "approved_modules")
        modules = getattr(approved_modules, "CLI_MODULES")
        attrs = {}
        namespace_package = __import__(a_namespace, globals(), locals(), modules)
    except ModuleNotFoundError as e:
        raise e

    for mod in modules:
        attrs[mod] = []
        my_module = getattr(namespace_package, mod)
        functions = getmembers(my_module, isfunction)
        for name, method in functions:
            if name not in FORBIDDEN_MEMBERS and not name.startswith('_'):
                if name == a_function:
                    # Return the callable if found in the list of members in the approved namespace
                    return method
                attrs[mod].append(name)
    # If no argument was passed, print the callable options!
    print(
        f"{colors['yellow']}{a_namespace}{colors['reset']} has the following {colors['green']}module{colors['reset']} {colors['blue']}[commands]{colors['reset']}:"
    )

    for mod in sorted(attrs.keys()):
        print(f"\n\t{colors['green']}{mod}{colors['reset']}")
        for func in sorted(attrs[mod]):
            print(f"\t  * {colors['blue']}{func}{colors['reset']}")
    exit()


FORBIDDEN_MEMBERS = ['os', 'shutil', 'sys', 'remove', 'rmtree']

