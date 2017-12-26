# encoding: utf-8

import gvsig

import sys

from org.gvsig.fmap.dal.feature import FeatureStoreTimeSupport
from java.lang import String
from org.gvsig.timesupport import TimeSupportLocator
from java.text import SimpleDateFormat

from jarray import array

from java.util import Date

class SimpleTimeSupport(FeatureStoreTimeSupport):
  def __init__(self, attrName, timeAttrName, dataType, interval, simpleDateFormat=None):
    FeatureStoreTimeSupport.__init__(self)
    self.__attrName = attrName
    self.__timeAttrName = timeAttrName
    self.__dataType = dataType
    self.__times = list()
    self.__simpleDateFormat = simpleDateFormat
    self.__timeManager = TimeSupportLocator.getManager()
    t1 = self.__timeManager.createRelativeInstant(interval[0])
    t2 = self.__timeManager.createRelativeInstant(interval[1])
    self.__interval = self.__timeManager.createRelativeInterval(t1,t2)
    
  def getAttributeName(self):
    return self.__attrName

  def getDataType(self):
    return self.__dataType

  def getInterval(self):
    return self.__interval

  def getTimes(self, interval=None):
    return self.__times

  def get(self, feature):
    value = feature.get(self.__timeAttrName)
    if not isinstance(value, Date):
      try:
        value = self.__simpleDateFormat.parse(value)
      except:
        value = None
    if value != None:
      value = self.__timeManager.createRelativeInstant(value)
    return value
    
  def set(self, feature, value):
    pass

  def allowSetting(self):
    return False

  def getRequiredFieldNames(self):
    return array((self.__timeAttrName,),String)


def main(*args):
  pass
