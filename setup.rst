Setting Up My Environment
==============================

I have become accustomed to using ``pyenv`` to manage python versions on my machine, and ``pyenv-virtualenv`` for virtual environment management.

.. code-block:: shell

   # Using a shell profile to store the PYENV
   SOME_SHELL_PROFILE=~/.zshrc
   git clone https://github.com/pyenv/pyenv.git ~/.pyenv
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> $SOME_SHELL_PROFILE
   echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> $SOME_SHELL_PROFILE
   PYTHON_VERSION_TO_USE=3.10.7
   pyenv install $PYTHON_VERSION_TO_USE
   echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> $SOME_SHELL_PROFILE

   git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
   echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv virtualenv-init -)"\nfi' >> $SOME_SHELL_PROFILE
   # Restart shell
   exec "$SHELL"

   pyenv virtualenv $PYTHON_VERSION_TO_USE portfolio

.. code-block:: shell

   # then if I need to find something else
   pyenv versions
   source deactivate portfolio

In each of my project sub-folders I have included some requirements that are contextually relevant, so I can install those as needed.

Java (for spark)
-------------------

Since I was running in pycharm console, I needed to edit my console environment variables to have the correct Java Home

I found this using ```java -XshowSettings:properties -version```