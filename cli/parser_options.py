from optparse import OptionParser

"""
Lightweight dictionary of argument parsing options
for the CLI
"""
ACTION = 'action'
HELP = 'help'
DEST = 'dest'
BOOL = 'bool'
EXTEND = 'extend'
DATA = 'data'
JSON_DATA = 'json_data'
STORE = 'store'

PARSER_OPTIONS = {
    'conn_string': {
        HELP: 'For some tasks where a connection string is viable, the string itself pre-compiled.'
    },
    'cron': {HELP: 'A cron expression (Minutes Hours Days_of_Month Months Days_of_Week'},
    'data': {ACTION: 'json_data', HELP: 'A Dict or JSON object passed directly from command line.'},
    'data_file': {
        ACTION: 'json_data',
        HELP: 'If there is a file with data (e.g., data for posting in JSON requests), the absolute filepath',
        DEST: 'data',
    },
    'dataset_name': {HELP: 'The name of a dataset in a data model.'},
    'db_name': {HELP: 'The DB name of a DB connection'},
    'delimiter': {HELP: 'Delimiter character for csv or psql copy tasks'},
    'description': {HELP: 'if pertinent, the description of something.'},
    'destination_directory': {
        HELP: 'In a copy or bilateral repo/directory operation, the destination.'
    },
    'dialect': {HELP: 'The dialect of a CSV to open in, for instance'},
    'encoding': {HELP: 'The encoding of a file'},
    'extension': {HELP: 'File extension'},
    'file_path': {HELP: 'A file path to interact with.'},
    'file_path_pattern': {HELP: 'The path pattern of a file for searching'},
    'host': {HELP: 'If passing DB connect args, the Host'},
    'mode': {HELP: 'where relevant, toggles modes for certain methods'},
    'n': {HELP: 'the number variable'},
    'name': {HELP: "name of object or file you're making"},
    'null_char': {HELP: 'Null character override for psql copy tasks.'},
    'output_directory': {HELP: 'An output directory to write files out to.'},
    'output_file': {HELP: 'the file to write out to'},
    'params': {
        ACTION: 'json_data',
        HELP: 'A Dict or JSON object passed directly from command line for parameters.',
    },
    'params_file': {
        ACTION: 'json_data',
        HELP: 'If there is a file with data (e.g., parameters for posting in JSON requests), the absolute filepath',
        DEST: 'params',
    },
    'password': {HELP: 'In local testing cases when a username:password is required, a password.'},
    'pattern': {HELP: 'A regex pattern for searching'},
    'port': {HELP: 'Port number for certain connection or forwarding tasks'},
    'query': {HELP: 'The query you want to run'},
    'quote_char': {HELP: 'Quote character used in csv and psql copy tasks'},
    'regex_flags': {
        HELP: "When passing a pattern to compile, the flags you need to compile it. Common examples are 'i' for ignore case, 's' for dotall, 'm' for multiline; to pass multiple just concat (e.g., im) "
    },
    's3_uri': {HELP: 'The S3 URI if known for an S3 migration task'},
    'schema': {HELP: 'For single-schema DB tasks, the schema'},
    'source_conn_string': {
        HELP: 'For migration tasks, the source sqlalchemy connection string'
    },
    'target_conn_string': {
        HELP: 'For migration tasks, the target sqlalchemy connection string'
    },
    'target_schema': {HELP: 'For migration tasks, the target schema'},
    'truncate': {HELP: 'For DB operations, whether or not to truncate', ACTION: BOOL},
    'url': {HELP: 'A URL'},
    'username': {HELP: 'A username for a connection.'},
    'xl_file': {HELP: 'File path to a .xlsx'},
}


def get_dict_from_parser(parser: OptionParser):
    """
    This is the method I used to simplify the dict representation
    of the client opt parsing.
    """
    options = {
        option.get_opt_string().replace('--', ''): {
            ACTION: option.action,
            HELP: option.help,
            DEST: option.dest,
        }
        for option in parser.option_list
    }
    return {
        opt: {
            key: value
            for key, value in opt_dict.items()
            if value and (key, value) != (ACTION, STORE) and value != opt
        }
        for opt, opt_dict in sorted(options.items())
    }
