# etl-airflow-s3

ETL using Apache Airflow and S3

## Setup

As of writing, Apache Airflow does not support Python 3.7 (my default install), so we need to install a local version of Python 3.6. We do this using [pyenv](https://github.com/pyenv/pyenv).

1. Install Homebrew version of pyenv (on OSX):

`brew install pyenv`

2. Install the latest Python 3.6 (as of writing, 3.6.8)

`pyenv install 3.6.8`

3. Use Python 3.6.8 for this project

`pyenv local 3.6.8`

4. Create a new virtual environment (using `venv` for the project using our installed Python 3.6.8):

`python -m venv /path/to/virtual-environment`

5. Activate the virtual environment:

`source /path/to/virtual-environment/bin/activate`

6. Install Apache Airflow:

`pip install apache-airflow`

7. Install Quilt T4:

`pip install t4`

8. Change the default location of of `AIRFLOW_HOME` to your project directory

`$ export AIRFLOW_HOME=~/airflow`

9. Initialize Airflow's database (defaults to SQLite):

`$ airflow initdb`

10. Start the scheduler:

`$ airflow scheduler`

11. Start the webserver (DAG interface):

`$ airflow webserver`

## <a name="simplifydaginterface"></a>Simplify the DAG web interface

By default, Airflow helpfully loads ~15 example DAGs: great for
learning but which clutter the UI. You can remove these (which you
will definitely want to do before moving to a production environment)
by setting the `load_examples` flag to `False` in the `[core]` section
of `AIRFLOW_HOME/airflow.cfg`:

```
# Whether to load the examples that ship with Airflow. It's good to
# get started, but you probably want to set this to False in 
# a production environment
load_examples = False
```

Note: If you started the Airflow scheduler and webserver _before_
updating this setting, you'll still see the example DAGs in the web
UI. To reset the view, run the following command (warning - this
will destroy all current DAG information!):

`$ airflow resetdb`
