from minicrawler.spider.nuspider import NUSpider
from minicrawler.spider.salaryspider import SalarySpider
from minicrawler.spider.richspider import RichSpider

# _nuSpider = NUSpider()
# _nuSpider.crawl(True)
# _nuSpider.crawl()
# Test
# _nuSpider._getCurrentPage(0, 0)

_salarySpider = SalarySpider()
# 1: start index adjustment
_salarySpider.crawl(True, 1)
# _salarySpider.crawl()

# _richSpider = RichSpider()
# _richSpider.crawl(True)


