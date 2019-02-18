from time import time
import newspaper
from newspaper import Config, Article, Source

from newsplease import NewsPlease

print("Configure")
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

paper_url = "https://theguardian.com"
paper = newspaper.build(paper_url)

print("Categories...")
for category in paper.category_urls():
    print(category)
    if 'technology' in category:
        tech_category = category
# print(f"Technology category: {tech_category}")

print("Articles...")
for article in paper.articles:
    url = article.url
    print(url)
    article = Article(url)
    article.download()
    count = 0
    while article.download_state != 2:
        #ArticleDownloadState.SUCCESS is 2 article.download() 
        count = count+1
        time.sleep(count)
    # this_article = Article(article.url, config)
    # if tech_category in article.url: 
    # this_article.download()
    # this_article.parse()
    # print(this_article.nlp())

# article = NewsPlease.from_url(bbc_rss)
# print(article.title)
# print(article.description)
# print(article.text)