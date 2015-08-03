#Name: William Zhang
#Date: 2/19/15
#Lab18: Bowling
import xml.etree.cElementTree as e
throw1,throw2=0,0
lastThrow=None
reset, strike, spare=True, False, False
score1,score2,score3=[],[],[]
b=1


def finalFrame(list):
   global lastThrow, reset, strike, spare
   while True:
      throw=raw_input("Enter score: ")
      if int(throw)==10: #If a strike is thrown
         if reset:
            list.append(10)
            lastThrow=0
            reset=True
            strike=True
            break
         else:
            print "Invalid input(s), try again"
      else:
         try:
             if int(lastThrow)+int(throw)==10: #If a spare is thrown
                list.append(10-lastThrow)
                lastThrow=10-lastThrow
                reset=True
                spare=True
                break
             else: #Normal condition
                throw=int(throw)
                if int(lastThrow)+throw>10:
                    raise ValueError()
                list.append(throw)
                lastThrow=throw
                reset=not reset
                break
         except: #If invalid input type
            print "Invalid input(s), try again"

#Start input section
while b<=9: #First 9 frames
   print "Frame " + str(b)
   throw1=raw_input("Enter first score: ")
   if int(throw1)==10: #If a strike is thrown
      score1.append(10)
      score2.append(0)
      score3.append(0)
   else:
      throw2=raw_input("Enter next score: ") #Ask for a second score
      try:
         if int(throw1)+int(throw2)==10: #If a spare is thrown
            if int(throw1)>10:
               raise ValueError()
            else:
               score1.append(int(throw1))
               score2.append(int(throw2))
               score3.append(0)
         else: #Normal condition
            if int(throw1)+int(throw2)>10:
               raise ValueError()
            else:
               score1.append(int(throw1))
               score2.append(int(throw2))
               score3.append(0)
      except: #If invalid input type
         print "Invalid input(s), try again"
         continue
   b+=1
b+=1
print "Final Frame"
lastThrow=0
finalFrame(score1)
finalFrame(score2)
if strike or spare:
   finalFrame(score3)

#Start calculation section
strike, spare=False, False
framescore=0
ovscore=[None]*10

for i in xrange(9):
   if spare: #If last frame was a spare
      framescore+=score1[i] #Add next ball to old framescore
      ovscore[i-1]=framescore
   elif strike: #If last frame was a strike
      if score1[i]==10: #If current frame is a strike
         framescore+=score1[i]+score1[i+1]
      else: 
         framescore+=score1[i]+score2[i] #Add next 2 balls to old framescore
      ovscore[i-1]=framescore
   else: #Normal condition
      pass
   
   if score1[i]==10:
      spare=False
      strike=True
   else:
      if score1[i]+score2[i]==10:
         spare=True
      else:
         spare=False
      strike=False
   framescore+=score1[i]+score2[i] #Add current frame's balls
   ovscore[i]=framescore
if spare: #If last frame was a spare
   framescore+=score1[-1] #Add next ball to old framescore
elif strike: #If last frame was a strike
   framescore+=score1[-1]+score2[-1] #Add next 2 balls to old framescore
ovscore[i]=framescore
framescore+=score1[-1]+score2[-1]+score3[-1]
ovscore[-1]=framescore
print "Please view bowlingScores.html for an overview of your bowling game."

#Start HTML output section
html = e.Element("html")
head = e.SubElement(html,"head")
title = e.SubElement(head,"title")
title.text = "Scores"
body = e.SubElement(html,"body")
frame = e.SubElement(body,'div style="font-family:Arial"')  
for a in xrange(len(score1)):
   frame_n = e.SubElement(frame,'span style="font-weight:bold"')
   frame_n.text = "Frame " + str(a+1) + ":"
   break_ = e.SubElement(frame,"br")
   score_1 = e.SubElement(frame,"span")
   score_1.text = "1: " + str(score1[a])
   break_ = e.SubElement(frame,"br")
   score_2 = e.SubElement(frame,"span")
   score_2.text = "2: " + str(score2[a])
   break_ = e.SubElement(frame,"br")
   if a==9 and score3[-1]!=0:
      score_3 = e.SubElement(frame,"span")
      score_3.text = "3: " + str(score3[-1])
      break_ = e.SubElement(frame,"br")
   ovscore_ = e.SubElement(frame,"span")
   ovscore_.text = "Overall: " + str(ovscore[a])
   for s in xrange(2):
      break_ = e.SubElement(frame,"br")
  
out = e.ElementTree(html)
out.write('bowlingScores.html')
