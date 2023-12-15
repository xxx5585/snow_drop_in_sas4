#pip install pywin32 wxpython 

import win32gui
import win32con
import win32api
import wx
import random
import math
import time

def get_client_position():

  sas4_title = 'SAS: Zombie Assault 4'
  #sas4_title = 'Untitled - Notepad'
  while True:
    sas4_handle = win32gui.FindWindow(None, sas4_title)
    if sas4_handle:
      break
    else:
      time.sleep(5)
      continue

  window_rect = win32gui.GetWindowRect(sas4_handle)
  client_rect = win32gui.GetClientRect(sas4_handle)

  flame_width = ((window_rect[2] - window_rect[0]) - (client_rect[2] - client_rect[0]))/2
  titlebar_hieght = window_rect[3] - window_rect[1] - (client_rect[3] - client_rect[1]) - flame_width


  x0 = window_rect[0] + flame_width
  y0 = window_rect[1] + titlebar_hieght
  x1 = window_rect[2] - flame_width
  y1 = window_rect[3] - flame_width

  w = x1 - x0
  h = y1 - y0

  if h > w /4 * 3:
    h = w /4 * 3
    y0 = (y1+y0)/2 - h/2
    y1 = y0 + h
  elif w > h /9 * 16:
    w = h /9 * 16
    x0 = (x1+x0)/2 - w/2
    x1 = x0 + w

  return x0, y0, x1, y1

class Snow:
  def __init__(self,x,y):
    self.beforex=self.x=x
    self.beforey=self.y=y
    self.baseX=x
    self.size=random.randint(1*3,3*3)

  def update(self):
    self.beforex=self.x
    self.beforey=self.y
    self.x=self.baseX+2*math.sin(self.y*0.1)
    self.y+=1


class AppFrame( wx.Frame ):
  def __init__(self):
    wx.Frame.__init__(self,parent=None, title="HP Layer",style= wx.STAY_ON_TOP)


    hwnd = self.GetHandle()
    extendedStyleSettings = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, extendedStyleSettings | win32con.WS_EX_LAYERED | win32con.WS_DISABLED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0,0,0), 0, win32con.LWA_COLORKEY)

    x0, y0, x1, y1 = get_client_position()

    win32gui.MoveWindow(hwnd, int(x0), int(y0), int(x1), int(y1), True)

    #self.Maximize()
    self.snows=[]
    self.Bind(wx.EVT_PAINT,self.OnPaint)
    self.timer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.onTimer)
    self.timer.Start(10)


  def OnPaint(self, evt):
    dc=wx.PaintDC(self)
    dc=wx.BufferedDC(dc)
    if not random.randint(0,3):
      self.snows.append(Snow(random.randint(0, self.GetSize()[0]),0))

    #dc.SetBackground(wx.Brush('black'))
    #dc.Clear()

    for snow in self.snows:
      dc.SetPen(wx.BLACK_PEN)
      dc.SetBrush(wx.BLACK_BRUSH)
      dc.DrawCircle(int(snow.beforex),int(snow.beforey),snow.size)
      dc.SetTextForeground((0,0,0))
      dc.DrawText(str(snow.size), int(snow.beforex),int(snow.beforey))
      snow.update()
      dc.SetPen(wx.WHITE_PEN)
      dc.SetBrush(wx.WHITE_BRUSH)
      dc.DrawCircle(int(snow.x),int(snow.y),snow.size)
      #dc.SetTextForeground((255,0,0))
      #dc.DrawText(str(snow.size), int(snow.x),int(snow.y))
      if snow.y>self.GetSize()[1]:
        self.snows.remove(snow)

  def onTimer(self,event):
    self.Refresh(False)

if __name__ == '__main__':
  app = wx.App(False)
  AppFrame().Show()
  app.MainLoop()


