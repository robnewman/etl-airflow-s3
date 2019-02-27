# etl-airflow-s3

ETL of newspaper article keywords using Apache Airflow, Newspaper3k, Quilt T4
and AWS S3

## Setup

As of writing, Apache Airflow does not support Python 3.7 (my default install), so we need to install a local version of Python 3.6. We do this using [pyenv](https://github.com/pyenv/pyenv).

1. Install Homebrew version of pyenv (on OSX):

`$ brew install pyenv`

2. Install the latest Python 3.6 (as of writing, 3.6.8)

`$ pyenv install 3.6.8`

3. Use Python 3.6.8 for this project

`$ pyenv local 3.6.8`

4. Create a new virtual environment (using `venv` for the project using our installed Python 3.6.8):

`$ python -m venv /path/to/virtual-environment`

5. Activate the virtual environment:

`$ source /path/to/virtual-environment/bin/activate`

6. Install Apache Airflow:

`$ pip install apache-airflow`

7. Install Quilt T4:

`$ pip install t4`

8. Install Newspaper3k:

```
$ brew install libxml2 libxslt
$ brew install libtiff libjpeg webp little-cms2
$ pip install newspaper3k
$ curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python
```

9. Change the default location of of `AIRFLOW_HOME` to your project directory

`$ export AIRFLOW_HOME=~/airflow`

10. Initialize Airflow's database (defaults to SQLite):

`$ airflow initdb`

11. Start the scheduler:

`$ airflow scheduler`

12. Start the webserver (DAG interface):

`$ airflow webserver`

## <a name="customdagfolder"></a>Define a custom DAG folder

If you are storing you DAGs in a local repository (as part of a
larger version-controlled data engineering infrastructure) rather
than globally in `AIRFLOW_HOME/dags`, you’ll need to update the entry
in `airflow.cfg` to reflect this new DAG folder location:

```
[core]
# The home folder for airflow, default is ~/airflow
airflow_home = /Users/<username>/airflow

# The folder where your airflow pipelines live, most likely a
# subfolder in a code repository
# This path must be absolute
dags_folder = /Users/<username>/<path-to-repo>/dags
```

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

## Check your DAGs

List current DAGs:

`$ airflow list_dags`

Check each task in your DAG:

`$ airflow list_tasks <dag_id>`

Test DAG tasks end-to-end:

`$ airflow test <dag_id> <task_id> <execution_date>`
