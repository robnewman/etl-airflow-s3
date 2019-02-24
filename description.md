# Sentiment analysis of online newspaper articles

## Overview

Using Apache Airflow as our ETL tool, we have an end-to-end online newspaper article scraping pipeline. We extract article keyword data using NLP, transform it, save locally to JSON files, then add to a quilt data package and upload to AWS S3.

## Online sources

We scrape article content from the following three sources:

* The Guardian
* The New York Times
* CNN

## Visualization

Our dashboard displays Vega [Word Cloud](https://vega.github.io/vega/examples/word-cloud/) visualizations of keywords scraped from our three online news sources.

