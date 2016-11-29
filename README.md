# Mini Crawler
This is a mini size crawler made by **Python3**. It's easy to use and extend. Good for study.
Simply crawler every item on a page and save it into local csv file. Then go to the next page.

## Main Features
- Save every item on the page into cvs and then go to the next page
- Pause and rerun
- Suppoer almost all kernels (PhantomJS, Firefox etc.)
- Also can use Requests for those static pages, speed up

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
> minicrawler/spider/basespider.py

- crawl
- **_getTotalKeys_** (leave it to sub class)
- **_getCurrentPage_** (leave it to sub class)
- **_gotoNextPage_** (leave it to sub class, optional)
- saveCurrentIndex
- saveContentToWorkbook

> minicrawler/provider/requestor.py

> minicrawler/provider/webbrowser.py

- load
- getContent (leave it to different kernel)
- navigate (leave it to different kernel)
- quit

### Three different examples
1. Wikipedia (static page)
⋅⋅* https://en.wikipedia.org/wiki/List_of_colleges_and_universities_in_the_United_States_by_endowment
⋅⋅* Static page
⋅⋅* Only one page
> minicrawler/spider/richspider.py

2. US news (dynamic with url pagination)
⋅⋅* http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities
⋅⋅* Dynamic page
⋅⋅* Change url to next page
> minicrawler/spider/nuspider.py

3. Startclass (dynamic with button pagination)
⋅⋅* http://faculty-salaries.startclass.com/
⋅⋅* Dynamic page
⋅⋅* Click the pagenition button for the next page
> minicrawler/spider/salaryspider.py

