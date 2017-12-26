# encoding: utf-8

import gvsig

from gvsig.commonsdialog import msgbox
from gvsig import currentLayer
from gvsig import getResource
from gvsig.libs.formpanel import FormPanel

from org.gvsig.tools.swing.api import ToolsSwingLocator

from org.gvsig.tools.swing.api.windowmanager import WindowManager_v2
from java.awt.event import ActionListener
from javax.swing import JPopupMenu

from org.gvsig.app import ApplicationLocator
from org.gvsig.fmap.dal import DataTypes

import dropDownCalendar
reload(dropDownCalendar)
from dropDownCalendar import DropDownCalendar

import simpleTimeSupport
reload(simpleTimeSupport)
from simpleTimeSupport import SimpleTimeSupport

from java.text import SimpleDateFormat

from org.gvsig.tools import ToolsLocator

class AddTimeSupport(FormPanel, ActionListener):
  def __init__(self, layer):
    FormPanel.__init__(self, getResource(__file__, "addTimeSupport.xml"))
    self.__starTime = None
    self.__endTime = None
    self.__layer = layer
    toolsSwingManager = ToolsSwingLocator.getToolsSwingManager()
    toolsSwingManager.translate(self.lblLayer)
    toolsSwingManager.translate(self.lblTimeAttribute)
    toolsSwingManager.translate(self.lblTimeAttributeName)
    toolsSwingManager.translate(self.lblRangeOfValues)
    toolsSwingManager.translate(self.lblStarTime)
    toolsSwingManager.translate(self.lblEndTime)
    toolsSwingManager.translate(self.lblParsePattern)
    self.txtLayer.setText(layer.getName())
    self.txtTimeSupportName.setText("TimeSupport")
    featureType = self.__layer.getFeatureStore().getDefaultFeatureType()
    self.fillCombo(self.cboTimeAttribute,featureType)
    self.setPreferredSize(450,200)

  def fillCombo(self, combo, featureType):
    combo.removeAllItems()
    combo.addItem(" ")
    for attr in featureType:
      combo.addItem(attr.getName())
    combo.setSelectedIndex(0)

  def btnStarTime_click(self,event):
    DropDownCalendar().show(self.txtStarTime, self.__starTime_change)

  def __starTime_change(self, time):
    self.__starTime = time
    self.txtStarTime.setText(time.toString())
    
  def btnEndTime_click(self,event):
    DropDownCalendar().show(self.txtEndTime, self.__endTime_change)

  def __endTime_change(self, time):
    self.__endTime = time
    self.txtEndTime.setText(time.toString())
    
  def apply(self):
    pattern = self.cboParsePatern.getSelectedItem()
    if pattern != None:
      pattern = pattern.toString()
    timeSupport = SimpleTimeSupport(
      self.txtTimeSupportName.getText(), 
      self.cboTimeAttribute.getSelectedItem(), 
      DataTypes.DATE, 
      (self.__starTime, self.__endTime),
      simpleDateFormat=SimpleDateFormat(pattern)
    )
    self.__layer.getDataStore().setTimeSupport(timeSupport)
    ApplicationLocator.getManager().refreshMenusAndToolBars()
    
  def actionPerformed(self, event):
    if event.getSource().getAction()==WindowManager_v2.BUTTON_OK:
      self.apply()
    
def main(*args):
  i18n = ToolsLocator.getI18nManager()
  layer = currentLayer()
  if layer == None:
    msgbox(i18n.getTranslation("_Need_a_vector_layer_selected_in_the_ToC"))
    return 
  panel = AddTimeSupport(currentLayer())

  winmgr = ToolsSwingLocator.getWindowManager()
  dialog = winmgr.createDialog(
    panel.asJComponent(),
    i18n.getTranslation("_Add_basic_time_support"),
    i18n.getTranslation("_Add_basic_time_support_to_vectorial_layer"),
    winmgr.BUTTONS_OK_CANCEL
  )
  dialog.addActionListener(panel)
  dialog.show(winmgr.MODE.WINDOW)
