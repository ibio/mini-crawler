from ..provider.webbrowser import WebBrowser
from ..provider.requestor import Requestor
import csv
import os
import pickle
import datetime
import shutil
import numpy as np
import pandas as pd

class BaseSpider():

  # member variables
  _provider = None
  _outputFolder = 'output'
  _keyList = []
  _lastKeyPath = None
  _isRunning = False

  # constructor
  def __init__(self, url, lastKeyPath, asyncPage = False, outputFolder = None, broswerRest = None):
    self._lastKeyPath = lastKeyPath
    # if it's a async page
    if(asyncPage):
      self._provider = WebBrowser(url, broswerRest)
    else:
      self._provider = Requestor(url)
    if(outputFolder):
      self._outputFolder = outputFolder
    self._keyList = self._getTotalKeys()
    # print (self._keyList)

  def crawl(self, forceRestart = False, startIndex = 0):
    if(forceRestart):
      self._setKeyIndex(startIndex)
      #
      if(os.path.exists(self._outputFolder)):
        shutil.rmtree(self._outputFolder)
    # start
    # test finish # self._setKeyIndex(25230)
    if(self._isRunning):
      print('It was already running...')
    else:
      self._isRunning = True
      # go though all crawled pages
      self._ignoreCrawledPages()
      self._getTotalPages()
      self._provider.quit()
      self._isRunning = False
  
  # NOTICE: needs to be implemented in subclass  
  def _getTotalKeys(self):
    # html = self.provider.getContent()
    return []

  # NOTICE: needs to be implemented in subclass
  def _getCurrentPage(self, index, key):
    return None

  # NOTICE: needs to be implemented in subclass for async pages
  def _gotoNextPage(self, index, key):
    pass

  def _ignoreCrawledPages(self):
    index = self._getKeyIndex()
    for i in range(index):
      print('go to page {:d}'.format(i + 1))
      self._gotoNextPage(i, self._keyList[i])

  def _getTotalPages(self):
    index = self._getKeyIndex()
    totalLeft = len(self._keyList) - index
    date = datetime.datetime.today().strftime("%m/%d/%Y %H:%S")
    print ('[{!s}] total left items: [{:d}/{:d}]'.format(date, totalLeft, len(self._keyList)))
    for i in range(totalLeft):
      self._getAndSave()

  def _getKeyIndex(self):
    index = 0
    # get current index
    try:
      with open(self._lastKeyPath, 'rb') as f:
        index = pickle.load(f)
    except Exception as e:
      print (e)
    return index

  def _setKeyIndex(self, index):
    # save current index
    with open(self._lastKeyPath, 'wb') as f:
      pickle.dump(index, f)

  def _getAndSave(self):
    keyIndex = self._getKeyIndex()
    # just for test # keyIndex = 6
    # https://pyformat.info/
    print('trying to get the page {:d}...'.format(keyIndex + 1))
    if(self._keyList and self._keyList[keyIndex]):
      key = self._keyList[keyIndex]
      result = self._getCurrentPage(keyIndex, key)
      if(result):
        # print (result)
        # save to .csv
        # use keyIndex because current key may be invalid path
        self._saveWorkbook(result, keyIndex)
        print('getting {!s} done!'.format(key))
      # save current index as an existing one
      keyIndex += 1
      # save current index
      self._setKeyIndex(keyIndex)
      # go to the next page
      self._gotoNextPage(keyIndex, key)
    date = datetime.datetime.today().strftime("%m/%d/%Y %H:%S")
    string = '[{!s}] next [{:d}/{:d}]'.format(date, keyIndex + 1, len(self._keyList))
    # last items
    if(keyIndex >= len(self._keyList)):
      string = '[{!s}] all finished!'.format(date)
    print(string)

  def _saveWorkbook(self, items, key):
    path = '/'.join([self._outputFolder, 'key' + str(key) + '.csv'])
    # check the folder
    if not os.path.exists(self._outputFolder):
      os.makedirs(self._outputFolder)
      print('"./{!s}/" does not exist, making a new one...'.format(self._outputFolder))
    #
    df = pd.DataFrame(items)
    # df = df.set_index('institute')
    if(os.path.isfile(path)):
      # append model
      with open(path, 'a') as f:
        df.to_csv(f, header=False, index=False)
    else:
      df.to_csv(path, index=False)
    #

