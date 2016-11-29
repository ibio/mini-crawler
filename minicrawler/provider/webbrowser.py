from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException
import time

class WebBrowser():
  TIME_DELAY = 0.05
  # static variables
  DEFAULT_HEADER = {
    'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
  }

  # member variables
  _browser = None
  _browserRest = None

  def __init__(self, url, browserRest = {}):
    self._browserRest = browserRest
    # http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
    # *param: all function parameters as a tuple
    # **param: all keyword arguments except for those corresponding to a formal parameter as a dictionary
    self.load(url)

  def load(self, url):
    self._browser = self._getBroswer(url, **self._browserRest)
  
  # this is a MUST-HAVE signature
  def getContent(self):
    # https://docs.python.org/3/reference/simple_stmts.html#assert
    # make sure the handler is here
    assert self._browser is not None, 'self._browser is None, please check.'
    return self._browser.page_source

  # selector: tag.className
  def navigate(self, checkId, selector):
    if(self._browser):
      result = self._checkElement(self._browser, checkId, 1)
      # element.send_keys(Keys.RETURN)
      if(result):
        element = self._browser.find_element_by_css_selector(selector)
        # how to fix StaleElementReferenceException
        # http://stackoverflow.com/questions/17174515/how-to-resolve-stale-element-exception-if-element-is-no-longer-attached-to-the
        try:
          element.click()
        except StaleElementReferenceException as e:
          print(type(e))    # the exception instance
          time.sleep(WebBroswer.TIME_DELAY)
          self.navigate(checkId, selector)
      else:
        print('found out checkId of navigate [{!s}]: {!s}'.format(checkId, result))
        time.sleep(WebBroswer.TIME_DELAY)
        self.navigate(checkId, selector)
  
  def quit(self):
    if(self._browser):
      self._browser.close()
      # 'NoneType' object has no attribute 'path'
      self._browser.quit()
      self._browser = None

  # private member methods
  def _getBroswer(self, url, driver = None, checkId = None, header = None, timeout = 5, width = 0, height = 0, screenshot = None):
    header = header or {}
    # the latest header will rewrite default header
    combinedHeader = {**WebBroswer.DEFAULT_HEADER, **header}
    # http://stackoverflow.com/questions/35666067/selenium-phantomjs-custom-header-in-python
    for key, value in combinedHeader.items():
      webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{!s}'.format(key)] = value
      pass
    # http://selenium-python.readthedocs.io/getting-started.html
    if(driver is 'phantomjs'):
      print('header', __name__, combinedHeader)
      # TODO: PhantomJS has some problems for dynamic loading some pages ...
      browser = webdriver.PhantomJS()
    else:
      # selenium.common.exceptions.WebDriverException: Message: 'geckodriver' executable needs to be in PATH.
      # It needs to download firefoxdriver first and put it in to '/usr/local/bin'
      browser = webdriver.Firefox()
    if(width and height):
      browser.set_window_size(width, height) # optional
    browser.get(url)
    # assert "Python" in browser.title
    # element = browser.find_element_by_id('search-application-results-view')
    # print('===script===', script)
    # agent = browser.execute_script(script)
    # print('===agent===', agent)
    if(screenshot):
      browser.save_screenshot(screenshot) # save a screenshot to disk
    #
    if(checkId):
      result = None
      while(not result):
        result = self._checkElement(browser, checkId, timeout)
        print('found out checkId [{!s}]: {!s}'.format(checkId, result))
        time.sleep(WebBroswer.TIME_DELAY)
    # browser.page_source
    return browser

  def _checkElement(self, browser, id, timeout):
    element = None
    try:
      # timeout
      # checkId is for waiting for this id ready
      element = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.ID, id)))
      # html_source = browser.page_source
      pass
    except Exception as e:
      print(type(e))    # the exception instance
      # print(e.args)     # arguments stored in .args
      # print(e)
    return element is not None
  



