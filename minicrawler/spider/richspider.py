from .basespider import BaseSpider
from bs4 import BeautifulSoup
import re
import math

# Richest University Spider
class RichSpider(BaseSpider):
  TEMP_LAST_KEY = './minicrawler/spider/rich-lastkey.pickle'
  URL = 'https://en.wikipedia.org/wiki/List_of_colleges_and_universities_in_the_United_States_by_endowment'
  # CHECK_ID = 'search-application-results-view'
  HEADER = {
    # 'Host':'colleges.usnews.rankingsandreviews.com',
  }

  def __init__(self):
    super().__init__(RichSpider.URL, RichSpider.TEMP_LAST_KEY, False, 'rich-output')
    pass

  # override parent method
  def _getTotalKeys(self):
    itemList = ['rich']
    return itemList

  # override parent method
  def _getCurrentPage(self, index, key):
    itemList = []
    html = self._provider.getContent()
    # Test
    '''
    html = ''
    try:
      with open('./rich.html', 'rb') as f:
        html = f.read()
    except Exception as e:
      print (e)
    '''
    htmlElement = BeautifulSoup(html, 'html5lib')
    # NOTICE: 'find' only returns the first matching element
    parentElement = htmlElement.find('table', class_='wikitable')
    itemElementList = parentElement.find_all('tr')
    for itemElement in itemElementList:
      data = {}
      tdElements = itemElement.find_all('td')
      # ignore all from thead
      if(tdElements):
        data['institute'] = tdElements[0].a.string
        # 2015 billion USD
        data['2015'] = self._getBSD(tdElements[1].contents)
        data['2014'] = self._getBSD(tdElements[2].contents)
        data['2013'] = self._getBSD(tdElements[3].contents)
        data['2012'] = self._getBSD(tdElements[4].contents)
        data['2011'] = self._getBSD(tdElements[5].contents)
        data['2010'] = self._getBSD(tdElements[6].contents)
        data['2009'] = self._getBSD(tdElements[7].contents)
        data['2008'] = self._getBSD(tdElements[8].contents)
        data['2007'] = self._getBSD(tdElements[9].contents)
        data['2006'] = self._getBSD(tdElements[10].contents)
        data['2005'] = self._getBSD(tdElements[11].contents)
        itemList.append(data)
    # print(itemList)
    return itemList

  def _getBSD(self, elements):
    result = 0
    original = None
    temp = ''
    if(len(elements)):
      original = elements[0]
    if(original):
      temp = original.split('$') or []
      result = float(temp[1]) or 0
    return result
