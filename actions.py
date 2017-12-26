# encoding: utf-8

import gvsig


from gvsig import currentView
from gvsig import getResource
from java.io import File
from javax.swing import JScrollPane
from org.gvsig.andami import PluginsLocator
from org.gvsig.app import ApplicationLocator
from org.gvsig.app.project.documents.view import ViewManager
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools import ToolsLocator
from org.gvsig.tools.swing.api import ToolsSwingLocator

from addTimeSupport import AddTimeSupport
from gvsig import currentLayer
from gvsig.commonsdialog import msgbox

class AddBasicTimeSupportToDatasourceExtension(ScriptingExtension):
  def __init__(self):
    pass

  def canQueryByAction(self):
    return True

  def isEnabled(self,action):
    if action == "view-time-add-basic-support-to-datasource":
      view = currentView()
      if view == None:
        return False
      mapContext = view.getMapContext()
      if not mapContext.hasLayers():
        return False
      return mapContext.hasActiveVectorLayers()

  def isVisible(self,action):
    if action == "view-time-add-basic-support-to-datasource":
      view = currentView()
      if view == None:
        return False
      mapContext = view.getMapContext()
      return mapContext.hasLayers()
    
  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "view-time-add-basic-support-to-datasource":
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


def selfRegister():
  application = ApplicationLocator.getManager()

  #
  # Registramos las traducciones
  i18n = ToolsLocator.getI18nManager()
  i18n.addResourceFamily("text",File(getResource(__file__,"i18n")))

  #
  # Registramos los iconos en el tema de iconos
  icon = File(getResource(__file__,"images","view-time-add-basic-support-to-datasource.png")).toURI().toURL()
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
  iconTheme.registerDefault("scripting.addBasicTimeSupportToDatasource", "action", "view-time-add-basic-support-to-datasource", None, icon)

  #
  # Creamos la accion 
  extension = AddBasicTimeSupportToDatasourceExtension()
  actionManager = PluginsLocator.getActionInfoManager()
  action = actionManager.createAction(
    extension, 
    "view-time-add-basic-support-to-datasource", # Action name
    "Add basic support", # Text
    "view-time-add-basic-support-to-datasource", # Action command
    "view-time-add-basic-support-to-datasource", # Icon name
    None, # Accelerator
    650151000, # Position 
    "_Add_basic_time_support_to_vectorial_layer" # Tooltip
  )
  action = actionManager.registerAction(action)
  application.addMenu(action, "View/Time/_Add_basic_time_support")
  
def test():
  pass
      
def main(*args):
  #selfRegister()
  test()    
  