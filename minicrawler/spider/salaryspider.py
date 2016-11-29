from .basespider import BaseSpider
from bs4 import BeautifulSoup
import re
import math

class SalarySpider(BaseSpider):
  TEMP_LAST_KEY = './minicrawler/spider/salary-lastkey.pickle'
  URL = 'http://faculty-salaries.startclass.com/'
  
  def __init__(self):
    # superclass' constructor
    # NOTICE: it needs with > 1280 to get 5 'th' columns in the result
    super().__init__(SalarySpider.URL, SalarySpider.TEMP_LAST_KEY, True, 'salary-output', {'timeout':0, 'screenshot':'salary.png', 'checkId':'srp-results', 'width':1280, 'height':800})
    pass

  # override parent method
  def _getTotalKeys(self):
    itemList = []
    html = self._provider.getContent()
    htmlElement = BeautifulSoup(html, 'html5lib')
    # print(htmlElement)
    # pageElement = htmlElement.find('div', id='srp-footer-stats')
    pageElement = htmlElement.find('span', class_='fs-total')
    # http://stackoverflow.com/questions/21104476/what-does-the-r-in-pythons-re-compiler-pattern-flags-mean
    nums = re.compile(r"\d+")
    string = ''
    for key in nums.findall(pageElement.string):
      string += key
    string = string or 0
    page = int(string)
    # 20 item per page
    page = math.ceil(page / 20)
    for i in range(page):
      # keep in the same page
      itemList.append('salary')
    return itemList

  # override parent method
  def _gotoNextPage(self, index, key):
    self._provider.navigate('pager', 'div.next')
    pass

  # override parent method
  def _getCurrentPage(self, index, key):
    itemList = []
    html = self._provider.getContent()
    # Test
    '''
    html = ''
    try:
      with open('./salary.html', 'rb') as f:
        html = f.read()
    except Exception as e:
      print (e)
    '''
    htmlElement = BeautifulSoup(html, 'html5lib')
    tableElement = htmlElement.find('table', class_='srp-list-results')
    # print(len(tableElement.thead.tr.contents))
    # srp-list-results stnd-table
    trElementList = tableElement.find_all('tr', class_='srp-row')
    for itemElement in trElementList:
      data = {}
      instituteElement = itemElement.find('h3', class_='srp-listing-name')
      data['institute'] = instituteElement.a.string
      titleElement = itemElement.find('div', class_='srp-val')
      data['title'] = titleElement.div.string
      #
      tdElementList = itemElement.contents or []
      if(len(tdElementList) > 0):
        salary9Element = tdElementList[2].find('div', class_='val')
        if(salary9Element):
          data['salary9'] = self._getSalary(salary9Element.contents[1])
        #
        salaryAnnualElement = tdElementList[3].find('div', class_='val')
        if(salaryAnnualElement):
          data['salaryAnnual'] = self._getSalary(salaryAnnualElement.contents[1])
        #NOTICE: this column has something to do with viewport's width (with > 1280)
        totalFacultyElement = tdElementList[4].find('div', class_='val')
        if(totalFacultyElement):
          data['totalFaculty'] = totalFacultyElement.string
        # print(data)
      itemList.append(data)
    #
    return itemList

  def _getSalary(self, string):
    string = string or ''
    string = string.replace(',', '')
    return float(string)
  