# encoding: utf-8

import gvsig


from org.freixas.jcalendar import DateListener, JCalendar

from javax.swing import JPopupMenu

class DropDownCalendar(DateListener):
  def __init__(self):
    self.__onChange = None
    
  def dateChanged(self, de):
    if self.__onChange!=None:
      self.__onChange(de.getSelectedDate().getTime())

  def show(self, component, onChange):
    self.__onChange = onChange
    menu = JPopupMenu()
    jcalendar = JCalendar()
    jcalendar.addDateListener(self)
    menu.add(jcalendar)
    menu.show(component, 0, component.getY()+int(component.getSize().getHeight()))


