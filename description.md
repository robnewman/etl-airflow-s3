# Repeatable NLP of online newspaper articles

## Overview

Generate text corpus for calculating sentiment for multiple online news sources. ETL performed by Apache Airflow DAG; article keywords extracted using [newspaper3k](https://newspaper.readthedocs.io/en/latest/); data saved locally to JSON; added to a Quilt data package and upload to AWS S3 bucket using Quilt T4.

## Online sources

* [The Guardian](https://theguardian.com)
* [The New York Times](https://nytimes.com)
* [CNN](https://cnn.com)

## Exploratory data analysis over time

Our dashboard displays Vega [Word Cloud](https://vega.github.io/vega/examples/word-cloud/) visualizations of keywords scraped from our news sources and updated daily.

## Source code
[Github repository](https://github.com/robnewman/etl-airflow-s3)