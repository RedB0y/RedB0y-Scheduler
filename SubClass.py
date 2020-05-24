import json
from gspread_formatting import *
with open("config.json","r") as js:
              store=json.load(js)
              



ScheduledWeek=store["ScheduledWeek"]

NoOfTasks=store["NoOfTasks"]

TaskHours=store["TaskHours"]
DMFmt=cellFormat( backgroundColor=color(1.00,0.49,0.00),
                  textFormat=textFormat(bold=True,foregroundColor=color(0,0,0),fontSize=12),
                  horizontalAlignment='CENTER')
DFFmt=cellFormat( backgroundColor=color(1.00,0.80,0.40),
                  textFormat=textFormat(bold=True,foregroundColor=color(0,0,0),fontSize=12),
                  horizontalAlignment='CENTER')
BMFmt=cellFormat(
                            backgroundColor=color(0.70,1.00,0.80),
                              textFormat=textFormat(bold=True,foregroundColor=color(0,0,0),fontSize=12),
                              horizontalAlignment='CENTER')
 
BFFmt=cellFormat(
                            backgroundColor=color(0.80,1.00,0.87),
                              textFormat=textFormat(bold=True,foregroundColor=color(0,0,0),fontSize=12),
                              horizontalAlignment='CENTER')


class Sub:
              
              def __init__(self,SName,SPrio,ColorL,ColorFL):
                            self.SName=SName
                            self.SPrio=SPrio
                            self.Red,self.Green,self.Blue=ColorL
                            self.RedF,self.GreenF,self.BlueF=ColorFL
                            self.IsVisited=False
                            self.MFmt=cellFormat(
                              backgroundColor=color(self.Red,self.Green,self.Blue),
                              textFormat=textFormat(bold=True,foregroundColor=color(0,0,0),fontSize=12),
                              horizontalAlignment='CENTER')
                                                    
                            self.FFmt=cellFormat(
                                            backgroundColor=color(self.RedF,self.GreenF,self.BlueF),
                                            textFormat=textFormat(bold=True,foregroundColor=color(0,0,0),fontSize=12),
                                            horizontalAlignment='CENTER')                
                            self.SubHours=self.MEven(int(SPrio*ScheduledWeek*NoOfTasks*TaskHours))


              def MEven(self,number):
                            
                            if number%2==0:
                                          return number
                            else:
                                          return number-1

                            
              def SubVisit(self):
                            self.SubHours-=TaskHours
                            self.IsVisited=True
                            return self.SName

              def reset(self):
                            self.SubHours=self.MEven(int(self.SPrio*ScheduledWeek*NoOfTasks*TaskHours))
