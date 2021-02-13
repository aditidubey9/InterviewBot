import bot_dl
from tkinter import *
import tkinter.scrolledtext as ScrolledText
from PIL import ImageTk,Image
import time
import os

class InterviewBotPl(object):

    def __init__(self):
     
      self.text=None
      self.window=None
   
   

    def welcomeWindow(self):

       self.window=Tk()
       x_cordinate=(self.window.winfo_screenwidth()/2)-(600/2)
       y_cordinate=(self.window.winfo_screenheight()/2)-(600/2)
       self.window.geometry("%dx%d+%d+%d" %(600,600,x_cordinate,y_cordinate))
       self.window.title("Interview Bot")
       self.frame=Frame(master=self.window,bg='white')
       self.frame.pack(fill=BOTH,expand=1)
       self.frame.pack_propagate(0)
       imgO=Image.open(os.getcwd()+"/images/interviewbot.jpg")
       img= ImageTk.PhotoImage(imgO)
       self.Imagelabel=Label(self.frame,image=img,bg='white')
       self.Imagelabel.pack(side="bottom",fill="both",expand="yes")

       self.welcomeLabel=Label(self.frame,text='Welcome',font='Verdana 30 bold',bg='white')
       self.welcomeLabel.pack(side=TOP)
       self.window.after(5000,lambda:self.window.destroy())
       self.window.mainloop()


class MainWindow(object):
   
       
    def __init__(self):
      self.window=Tk()
      x_cordinate=(self.window.winfo_screenwidth()/2)-(550/2)
      y_cordinate=(self.window.winfo_screenheight()/2)-(600/2)
      self.window.geometry("%dx%d+%d+%d" %(550,600,x_cordinate,y_cordinate))
      self.window.title("Interview Bot")
      self.text=ScrolledText.ScrolledText(self.window, state='disabled',width=49,height=23,bg="white",font='Verdana 12')
      self.userLabel=Frame(self.window,height=50,width=300,bg="white")
      self.userLabel.pack_propagate(0)
      self.display_variable=StringVar()
      self.display_variable.set("")
      self.label=Label(self.userLabel,textvariable=self.display_variable,bg="white",font='Verdana 12')
      self.label.pack(fill=BOTH,expand=1)      
      print("PL Object created")

    def setAppearance(self):

      img=Image.open(os.getcwd()+"/images/logo.jpg")
      imgLogo=ImageTk.PhotoImage(img)


      self.text.config(state=DISABLED)
      self.text.place(x=30,y=80)
      img=Image.open(os.getcwd()+"/images/logo.jpg")
      imgLogo=ImageTk.PhotoImage(img)
      self.imageLabel=Label(self.window,image=imgLogo,width=50,height=50)
      self.imageLabel.place(x=2,y=2)
      self.TitleLabel=Label(self.window,text=" Interview Bot ",bg='white',borderwidth=2,relief="groove",font='Verdana 25 bold')
      self.TitleLabel.place(x=110,y=2)
     
      self.interviewBot=bot_dl.InterviewBot(self)
      self.img=Image.open(os.getcwd()+"/images/mike.png")
      self.imgMike=ImageTk.PhotoImage(self.img)
      self.listenButton=Button(self.window,image=self.imgMike,width=50,height=50,command=self.interviewBot.takeCommand)
      self.listenButton.place(x=10+40+10+30+250+20,y=400+110+2)
      self.img=Image.open(os.getcwd()+"/images/cancel.png")
      self.imgQuit=ImageTk.PhotoImage(self.img)
      self.QuitButton=Button(self.window,image=self.imgQuit,width=50,height=50,command=quit)
      self.QuitButton.place(x=64+40+30+20+250+20,y=400+110+2)

      self.userLabel.place(x=20+30,y=402+112+2)
      self.window.after(2000,lambda:self.interviewBot.startAI())
      self.window.mainloop()
       
    def getResponse(self,response):
        self.text['state']="normal"
        self.text.insert(END,response+"\n")
        self.text['state']="disabled"
        self.window.update()
       
    def getLabelResponse(self,response):
       self.display_variable.set(response)
       self.window.update()
 
    def clearLabel(self):
      self.display_variable.set("")
      self.window.update()
 
         

if __name__ =="__main__":
  a=InterviewBotPl()
  a.welcomeWindow()
  b=MainWindow()
  b.setAppearance()
