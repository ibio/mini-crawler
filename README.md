# Mini Crawler
This is a mini size crawler made by **Python3**. It's easy to use and extend. Good for study.
Simply crawler every item on a page and save it into local csv file. Then go to the next page.

## Used Packages
- requests
- selenium
- time
- csv
- os
- pickle
- datetime
- shutil
- numpy
- pandas
- BeautifulSoup4
- re
- math

## Main difference from Scrapy
- Easy to maintain
- Simple enough to use and extend
- Less Memory leak

## Architecture overview
![alt text](https://raw.githubusercontent.com/ibio/mini-crawler/master/mini-crawler.png "Mini Crawler")

## Main files
> webcrawler/spider/basespider.py

- crawl
- getTotalKeys (leave it to sub class)
- getCurrentPage (leave it to sub class)
- gotoNextPage (leave it to sub class)
- saveCurrentIndex
- saveContentToWorkbook

> webcrawler/provider/requestor.py
> webcrawler/provider/webbrowser.py

- load
- getContent (leave it to different kernel)
- navigate (leave it to different kernel)
- quit


### Three different examples
1. Wikipedia (static page)
2. US news (dynamic with url pagination)
3. Startclass (dynamic with button pagination)
