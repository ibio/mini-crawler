'''
TEST:
from webcrawler.provider.requestor import Requestor
_r = Requestor('https://www.yelp.com/search?find_loc={!s}&start={:d}&cflt={!s}'.format('New+York,+NY', 0, 'chinese'))
print(_r.getContent())
'''
import requests

class Requestor():
  _html = None

  def __init__(self, url):
    self.load(url)

  def load(self, url):
    data = requests.get(url)
    self._html = data.text

  # this is a MUST-HAVE signature
  def getContent(self):
    return self._html

  # this is a MUST-HAVE signature
  def quit(self):
    pass
    
