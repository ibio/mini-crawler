from .basespider import BaseSpider
from bs4 import BeautifulSoup
import re
import math

# National University Spider
class NUSpider(BaseSpider):
  TEMP_LAST_KEY = './minicrawler/spider/nu-lastkey.pickle'
  URL = 'http://colleges.usnews.rankingsandreviews.com/best-colleges/rankings/national-universities?_page={:d}'
  CHECK_ID = 'search-application-results-view'
  HEADER = {
    'Host':'colleges.usnews.rankingsandreviews.com',
  }

  def __init__(self):
    super().__init__(NUSpider.URL.format(1), NUSpider.TEMP_LAST_KEY, True, 'nu-output', {'header':NUSpider.HEADER, 'driver':'phantomjs', 'screenshot':'nu.png', 'checkId':NUSpider.CHECK_ID, 'width':1280, 'height':800})
    pass

  # override parent method
  def _getTotalKeys(self):
    itemList = []
    html = self._provider.getContent()
    htmlElement = BeautifulSoup(html, 'html5lib')
    # print(html)
    pageElement = htmlElement.find('div', class_='search-count-view')
    page = int(pageElement.span.strong.string) or 0
    # 25 item per page
    page = math.ceil(page / 25)
    for i in range(page):
      # keep in the same page
      itemList.append('nu')
    return itemList

  # override parent method
  def _getCurrentPage(self, index, key):
    itemList = []
    # page number starts from 1
    number = index + 1
    self._provider.load(NUSpider.URL.format(number))
    html = self._provider.getContent()
    # Test
    '''
    html = ''
    try:
      with open('./nu.html', 'rb') as f:
        html = f.read()
    except Exception as e:
      print (e)
    '''
    htmlElement = BeautifulSoup(html, 'html5lib')
    parentElement = htmlElement.find('div', id='search-application-results-view')
    itemElementList = parentElement.find_all('div', class_='block-loose-for-large-up')
    # print('itemElementList', len(itemElementList))
    for itemElement in itemElementList:
      data = {}
      # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attributes
      # WHY: weired that 'is' doesn't go through but '==' does?
      # ANSWER: http://stackoverflow.com/questions/1504717/why-does-comparing-strings-in-python-using-either-or-is-sometimes-produce
      if(itemElement and (itemElement.attrs.get('data-view') == 'colleges-search-results-card')):
        instituteElement = itemElement.find('h3', class_='heading-large')
        data['institute'] = instituteElement.a.string
        addressElement = itemElement.find('div', class_='text-small')
        data['address'] = addressElement.string
        rankElements = itemElement.find('div', class_='text-strong')
        # https://docs.python.org/3/library/re.html#re.search
        # it needs 'strings' here because sometimes there are multiple children
        # NOTICE: special case, Rank Not Published
        if(rankElements.div is not None):
          nums = re.search(r"\d+", rankElements.div.contents[0].string)
          rank = nums.group(0) or 0
        else:
          rank = 0
        data['rank'] = rank
        divElementList = itemElement.find_all('div', class_='inline-right-tight-for-medium-up')
        # tuition
        # NOTICE: special case, $39,518 (out-of-state), $12,836 (in-state)
        data['tuition'] = self._getNumber(divElementList[0].strong.string.split('(out-of-state),')[0])
        # undergradEnrollment
        data['undergradEnrollment'] = self._getNumber(divElementList[1].strong.string)
        # print(data)
        itemList.append(data)
    return itemList

  def _getNumber(self, original):
    nums = re.compile(r"\d+")
    string = ''
    for key in nums.findall(original):
      string += key
    string = string or 0
    return int(string)

