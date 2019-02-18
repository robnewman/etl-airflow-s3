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

6. Install Apache Airflow (with support for S3-specific features):

`pip install apache-airflow[s3]`

7. Install Quilt T4:

`pip install t4`

8. Change the default location of of `AIRFLOW_HOME` to your project directory

`$ export AIRFLOW_HOME="$(pwd)"`

9. Initialize Airflow's database (default to SQLite):

`$ airflow initdb`

## Data Retrieval: Open Weather Map

We are going to get weather data from [OpenWeatherMap](https://openweathermap.org) using their [API](https://api.openweathermap.org). We'll get the current weather for the all Californian cities using the Current Weather API by specifying a bounding box (`bbox`) in the API call:

`http://api.openweathermap.org/data/2.5/box/city?bbox=-125,32,-114,42,10&appid=[APIKEY]`

where `APIKEY` is your personal API key.
