import pyttsx3 as ps
import speech_recognition as sr
import datetime
import os
import psycopg2 as psy
import bot_pl
class InterviewBot():
  
 def __init__(self,plObject):
  self.engine=ps.init()
  self.conn=psy.connect(database="postgres",user="postgres",password="dubey",host="localhost",port="5432")
  self.cur=self.conn.cursor()
  self.javaQuestions=dict({})
  self.cQuestions=dict({})
  self.cppQuestions=dict({})
  self.score=0
  self.highScore=dict({})
  self.responseObject=plObject

 def clear(self):
  self.responseObject.clearLabel()

 def sendResponse(self,response):
  self.responseObject.getResponse(response)
  
 def sendLabelResponse(self,response):
  self.responseObject.getLabelResponse(response)      



 def speak(self,audio):
  self.sendResponse(audio)
  self.engine.say(audio)
  self.engine.runAndWait()


 def wishMe(self):
  hour=int(datetime.datetime.now().hour)
  if(hour>=0 and hour<12):
   self.speak("Good Morning!")
  elif(hour>=12 and hour<16):
   self.speak("Good Afternoon!")
  else:
   self.speak("Good Evening!")
  self.speak("I am an interview Bot. Welcome!")

 def takeCommand(self):
  r=sr.Recognizer()
  with sr.Microphone() as source:
   r.adjust_for_ambient_noise(source,duration=0.6)
   self.sendLabelResponse("Listening....")
   #r.pause_threshold=1
   audio=r.listen(source)
   try:
    self.sendLabelResponse("Recognizing....")
    query=r.recognize_google(audio,language='en-in')
    print(f"User said: {query}\n")
   except Exception as e:
    print("Say that again please")  
    self.takeCommand()
  return query 

 def ask(self,question,correct_answer):
  self.speak(question)
  #while True:
  try:
   answer=self.takeCommand().lower()
   self.speak("Your answer is "+answer)
   if answer!=correct_answer.lower():
    self.speak("Sorry your answer is incorrect")
    self.speak("Correct answer is "+correct_answer)
   else:
    self.speak("Very good!!")
    self.speak("Your answer is correct")
    self.score+=10
    #speak("Please say yes to confirm ")
    #confirm=takeCommand().lower()
    #print(confirm)
    #if 'yes' in confirm:
     #break
    #else:
     #continue
  except Exception as e:
   print("Unable to understand ")
   self.speak("Correct answer is "+correct_answer)
  return 

 def searchNameFromDatabase(self,name):
  self.cur.execute(" SELECT S_NO,STUDENT_NAME,SCORE from STUDENT")
  rows=self.cur.fetchall()
  for row in rows:
   Name=row[1]
   if Name==name:
    self.speak("Name already exists....")
    self.speak("Do you wish to continue with that name Please say yes or no")
    while True:
     wish=self.takeCommand().lower()
     if wish=='yes':
      #delete ka code 
      return True
     elif wish=='no':
      self.speak("Please enter another name")
      return False
     else:
      self.speak("Say it again please")     
  self.conn.commit() 
  return True

 def addNameInDatabase(self,name):
  print("database opened successfully")
  self.cur.execute("INSERT INTO STUDENT(STUDENT_NAME,SCORE) VALUES('"+name+"','0')")
  print("Records are inserted")
  self.conn.commit()
  #conn.close()

 def updateScoreInDatabase(self,name):
  print("database opened successfully")
  self.cur.execute("UPDATE STUDENT set SCORE=self.score where STUDENT_NAME='"+name+"'")
  self.conn.commit()
  print("Records are updated")

 def askName(self):
  self.speak("What is your name?")
  while True:
   name=self.takeCommand().lower() 
   answer=self.searchNameFromDatabase(name)
   if answer==True:
    break 
  self.speak("Hello "+name)    
  self.askQuestionAboutLanguage()
  #self.updateScoreInDatabase(name)
 
 def populateDataStructureForCLanguage(self):
  self.cur.execute(" SELECT * from C_QUESBANK")
  rows=self.cur.fetchall()
  for row in rows:
   self.cQuestions[row[1]]=row[2]

 def populateDataStructureForCppLanguage(self):
  self.cur.execute(" SELECT * from CPP_QUESBANK")
  rows=self.cur.fetchall()
  for row in rows:
   self.cppQuestions[row[1]]=row[2]

 def populateDataStructureForJavaLanguage(self):
  self.cur.execute(" SELECT * from JAVA_QUESBANK")
  rows=self.cur.fetchall()
  for row in rows:
   self.javaQuestions[row[1]]=row[2]


 def replay(self):
  self.speak("Do you want to play again.....")
  
  while True:
   choice=self.takeCommand().lower()
   if choice=='no':
    self.speak("Good Bye!!")
    break
   elif choice=='yes':
    self.askQuestionAboutLanguage()
   else:
    self.speak("Say it again please!!")
   
 


 def setHighScore(self):
  self.cur.execute("SELECT * from STUDENT")
  rows=self.cur.fetchall()
  i="0"
  j=""
  for row in rows:
   if i<row[2]:
    j=row[1]
    i=row[2]
  self.highScore[j]=i
 

 
 def askCQuestion(self):
  self.speak("So let's start your interview in C")
  i=1
  for question in self.cQuestions:
   self.speak("Question "+str(i))
   if i>5:break
   self.ask(question,self.cQuestions[question])
   i+=1
  self.speak("Your interview is over")    
  self.speak("Your total score is ",self.score)
  self.speak("High score is ",+str(self.highScore))
  
  self.replay()
  

 def askCplusplusQuestion(self):
  self.speak("So let's start your interview in C++")
  i=1
  for question in self.cppQuestions:
   self.speak("Question "+str(i))
   if i>5:break
   self.ask(question,self.cppQuestions[question])    
   i+=1 
  self.speak("Your interview is over")    
  self.speak("Your total score is ",self.score)   
  self.speak("High score is ",+str(self.highScore))
  self.replay()



 def askJAVAQuestion(self):
  self.speak("So let's start your interview in Java")
  i=1
  for question in self.javaQuestions:
   if i>5:break
   self.speak("Question "+str(i))
   self.ask(question,self.javaQuestions[question])
   i+=1    
  self.speak("Your interview is over")    
  self.speak("Your total score is "+str(self.score)) 
  self.speak("High score is "+str(self.highScore))
  self.replay()


 def askQuestionAboutLanguage(self):
  self.speak("Let's start......")
  self.speak("What is your preferred Language C , C++ or JAVA ?")
  language=self.takeCommand().lower()
  self.populateDataStructureForCLanguage()
  self.populateDataStructureForCppLanguage() 
  self.populateDataStructureForJavaLanguage()
  self.setHighScore()
  if language=='c':
   self.askCQuestion()  
  elif language=='c plus plus':
   self.askCplusplusQuestion() 
  elif language=='java':
   self.askJAVAQuestion()
  else:
   self.speak("Language not available")
  return

 
 def startAI(self):
  self.wishMe()
  self.askName()