from time import time

# Apache Airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Newspaper
import newspaper
from newspaper import Config, Article, Source

# Quilt
import t4

default_args = {
    'owner': 'rnewman',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email': ['robertlnewman@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    'headlines',
    default_args=default_args,
    schedule_interval=timedelta(days=1))

def get_headlines(source_url):

    keywords_list = list()

    print(f"Grabbing headlines from {source_url}")

    config = Config()
    config.memoize_articles = False
    config.fetch_images = False
    config.browser_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    config.headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        'referer': "https://google.com",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Pragma': 'no-cache'
    }

    print("Build newspaper...")
    paper = newspaper.build(source_url)
    print("Collect today's articles")
    for article in paper.articles:
        print(article.url)
        single_article = Article(article.url)
        if single_article.publish_date > datetime.now() - timedelta(days=1):
            # Must call download and parse before NLP analysis
            single_article.download()
            count = 0
            while single_article.download_state != 2:
                #ArticleDownloadState.SUCCESS is 2 
                count = count+1
                time.sleep(count)
            single_article.parse()
            single_article.nlp()
            keywords_list.append(single_article.keywords)
    print("Completed parsing articles")


def add_to_package():
    print("Add to package")

t1 = PythonOperator(
    task_id='get_headlines',
    provide_context=False,
    python_callable=get_headlines,
    op_kwargs={'source_url': 'https://theguardian.com'},
    dag=dag
)

t2 = PythonOperator(
    task_id='add_to_package',
    provide_context=False,
    python_callable=add_to_package,
    dag=dag
)

# Set dependencies
t1 >> t2