# _*_ coding:utf-8 _*_

from link_crawler import link_crawler
from mongo_cache import MongoCache
from alexa_cb import AlexaCallback

def main():
    scrape_callback=AlexaCallback()
    cache=MongoCache()
    crawler(scrape_callback.seed_url,scrape_callback=scrape_callback,cache=cache,timeout=100,ignore_robots=True)

if __name__=='__main__':
    main()
