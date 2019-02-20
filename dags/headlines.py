from time import time

# Apache Airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Newspaper
import newspaper
from newspaper import Article

# Quilt
import t4


one_day_ago = datetime.combine(
    datetime.today() - timedelta(1),
    datetime.min.time()
)

default_args = {
    'owner': 'rnewman',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email': ['robertlnewman@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'provide_context':True
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    'headlines',
    default_args=default_args,
    schedule_interval=timedelta(days=1))

def get_headlines(**kwargs):

    keywords_list = list()

    print(f"Grabbing political headlines from {kwargs['source_url']}")
    print("Build newspaper...")
    paper = newspaper.build(
        kwargs['source_url'],
        memoize_articles=False
    )
    print("Collect today's articles")
    for article in paper.articles:
        if 'politics' in article.url:
            print(article.url)
            single_article = Article(article.url)
            # Must call download and parse before NLP analysis
            single_article.download()
            count = 0
            while single_article.download_state != 2:
                #ArticleDownloadState.SUCCESS is 2 
                count = count+1
                time.sleep(count)
            single_article.parse()
            single_article.nlp()
            keywords_list.extend(single_article.keywords)
    print("Completed parsing articles")
    print("Push to Xcom\n\n")
    return keywords_list
    # kwargs['ti'].xcom_push(key='keywords_list', value=keywords_list)

def add_to_package(**kwargs):
    ti = kwargs['ti']

    print("\n\nAdd to package")

    # Get values
    keywords_list = ti.xcom_pull(task_ids='get_headlines')
    print("Return unique values")
    keyword_set = set(keywords_list)
    print(keyword_set)

t1 = PythonOperator(
    task_id='get_headlines',
    python_callable=get_headlines,
    op_kwargs={'source_url': 'https://theguardian.com'},
    dag=dag
)

t2 = PythonOperator(
    task_id='add_to_package',
    python_callable=add_to_package,
    dag=dag
)

# Set dependencies
t1 >> t2