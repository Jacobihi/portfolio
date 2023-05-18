Command Line Interface
======================

The command line interface is a simple wrapper around the library optparse.

In one deployment a similar tool was used for data team members to run ad-hoc jobs interacting with our warehouse and orchestration tools.

I use sphinx as docs and gitlab pages for hosting internally, so I had pretty robust documentation for team members to use.

I have re-written my own version of this tool for my portfolio.

Usage
-----

.. code-block:: shell

   # make sure you are in portfolio
   export PYTHONPATH=$(pwd)
   source cli/aliases.sh
   cli --help


.. code-block:: shell

   # illustrative successful execution.
   file_path=some/path.csv
   table=something
   schema=some_schema

.. code-block:: console

   (portfolio) user portfolio % cli db load_a_file_to_postgres --file_path "${file_path}" --table $table --schema $schema
   [2023-05-17 23:18:22] - INFO: - creating postgres connector
   [2023-05-17 23:18:22] - INFO: - Loading from some/path.csv into some_schema.table
   [2023-05-17 23:18:22] - INFO: - 20 rows affected
   (portfolio) user portfolio %

.. automodule:: cli.run_cli
   :members:

.. automodule:: cli.arg_parser
   :members:

.. automodule:: cli.parser_options
   :members:

.. automodule:: cli.approved_namespaces
   :members:
