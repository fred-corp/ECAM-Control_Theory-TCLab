# import kivy module
import kivy

kivy.require("1.9.1")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.properties  import NumericProperty
from kivy.config import Config

import threading

import tclab

Ts = 1.0

class app(App):
  def build(self):
    self.lab = tclab.TCLab()
    self.title = 'TCLab GUI'
    self.valMVset = 0
    self.valDVset = 0
    mainBox = BoxLayout(orientation='vertical')

    ## MV control 
    MVBox = BoxLayout(orientation='horizontal')

    MVsliderBox = BoxLayout(orientation = 'vertical')
    MVsliderBox.add_widget(Label(text ='MV level'))
    self.MV = Slider(min = 0, max = 100)
    MVsliderBox.add_widget(self.MV)
    self.MV.bind(value = self.mv_value)
    MVBox.add_widget(MVsliderBox)

    MVlabelBox = BoxLayout(orientation='vertical')
    MVlabelBox.add_widget(Label(text ='Current'))
    self.oldMVLevel = Label(text = '0')
    MVlabelBox.add_widget(self.oldMVLevel)
    MVlabelBox.add_widget(Label(text ='New'))
    self.newMVLevel = Label(text ='0')
    MVlabelBox.add_widget(self.newMVLevel)

    MVBox.add_widget(MVlabelBox)
    

    MVSetButton = Button(background_color = (2, 2, 2, 1), text = 'Set MV', padding = (12, 12))
    MVSetButton.bind(on_press=self.setMV)
    MVBox.add_widget(MVSetButton)

    mainBox.add_widget(MVBox)

    ## DV control

    DVBox = BoxLayout(orientation='horizontal')

    DVsliderBox = BoxLayout(orientation = 'vertical')
    DVsliderBox.add_widget(Label(text ='DV level'))
    self.DV = Slider(min = 0, max = 100)
    DVsliderBox.add_widget(self.DV)
    self.DV.bind(value = self.dv_value)
    DVBox.add_widget(DVsliderBox)

    DVlabelBox = BoxLayout(orientation='vertical')
    DVlabelBox.add_widget(Label(text ='Current'))
    self.oldDVLevel = Label(text = '0')
    DVlabelBox.add_widget(self.oldDVLevel)
    DVlabelBox.add_widget(Label(text ='New'))
    self.newDVLevel = Label(text ='0')
    DVlabelBox.add_widget(self.newDVLevel)

    DVBox.add_widget(DVlabelBox)

    DVSetButton = Button(background_color = (2, 2, 2, 1), text = 'Set DV', padding = (12, 12))
    DVSetButton.bind(on_press=self.setDV)
    DVBox.add_widget(DVSetButton)

    mainBox.add_widget(DVBox)

    # Temp sensor
    tempSensorBox = BoxLayout(orientation = 'horizontal')
    self.tempSensorLabel = Label(text = 'Temperature')
    tempSensorBox.add_widget(self.tempSensorLabel)
    self.tempSensorReadout = Label(text = '0')
    tempSensorBox.add_widget(self.tempSensorReadout)
    mainBox.add_widget(tempSensorBox)

    self.updateTemp()

    return mainBox

  def mv_value(self, instance, MV):
    self.valMVset = MV
    self.newMVLevel.text = "% d"% MV

  def dv_value(self, instance, DV):
    self.valDVset = DV
    self.newDVLevel.text = "% d"% DV

  def setMV(self, instance):
    self.lab.Q1(self.valMVset)
    self.oldMVLevel.text = "% d"% self.valMVset

  def setDV(self, instance):
    self.lab.Q2(self.valDVset)
    self.oldDVLevel.text = "% d"% self.valDVset

  def updateTemp(self):
    threading.Timer(Ts, self.updateTemp).start()
    self.tempSensorReadout.text = "% d °C"% self.lab.T1


root = app()
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '500')
root.run()