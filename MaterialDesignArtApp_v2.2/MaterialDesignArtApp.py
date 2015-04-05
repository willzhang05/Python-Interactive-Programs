#By William Zhang
#Version 2.2
from Tkinter import *
from PIL import Image, ImageTk
from random import randint

#Create a window      
root = Tk()
root.wm_title("Material Design Art App")

w,h=1280,720
canvas = Canvas(root, width=w, height=h, bg="#EEEEEE")
tool=1
firstClick=True
linePoints=[]
points=[]
rectFirstClick=True
rectPoints=[]
rectCount=0
#Number of paint points
paint=100
paintPoints=[]
#Radius of spray paint
radius=15
vortexPoints=[]
winOpen=False
#RGB values for color
r=0
g=0
b=0

#Associate images to icons
material=Image.open('material.png').resize((100,100))
scribble=Image.open('freeHand_icon.png').resize((75,75))
can=Image.open('sprayPaint_icon.png').resize((75,75))
vortex=Image.open('vortex.png').resize((75,75))
icon=ImageTk.PhotoImage(material)
icon2=ImageTk.PhotoImage(scribble)
icon3=ImageTk.PhotoImage(can)
icon4=ImageTk.PhotoImage(vortex)

#Create base menu
menuY=0
while menuY<=500: 
   canvas.create_image(47.5,55+menuY, image=icon)
   menuY+=100

#Create menu icons   
canvas.create_line(25,25,75,75)
canvas.create_image(47.5,155,image=icon2)
canvas.create_rectangle(25,225,75,275, fill="black")
canvas.create_image(47.5,355,image=icon3)
canvas.create_image(47.5,455,image=icon4)
canvas.create_oval(13, 517, 83, 587, fill='#'+ ("%02x" % r) + ("%02x" % g) + ("%02x" % b))

def click(event):
   global firstClick, linePoints, points, paint, paintPoints, tool, winOpen
   #Tool 1 is drawLine
   if 0<event.x<95 and 5<event.y<100:
      tool=1
      #Custom cursor   
      canvas.configure(cursor="crosshair")
      firstClick=True
      linePoints=[]
   #Tool 2 is freeHand
   elif 0<event.x<95 and 105<event.y<200:
      tool=2
      canvas.configure(cursor="pencil")
      freeHand(event)
   #Tool 3 is drawRectangle
   elif 0<event.x<95 and 205<event.y<300:
      tool=3   
      canvas.configure(cursor="crosshair")
   #Tool 4 is sprayPaint
   elif 0<event.x<95 and 305<event.y<400:
      tool=4 
      canvas.configure(cursor="spraycan")
      #Store number of paint points
      sprayPaint(event)
   #Tool 5 is vortex
   elif 0<event.x<95 and 405<event.y<500:
      tool=5
      canvas.configure(cursor="trek")
   #Color picker
   elif 0<event.x<95 and 505<event.y:
      if winOpen:
         colorPicker.destroy()
         winOpen=False
      colorSelect(event)
   #Start drawing
   else:
      toolSelect(event)
      
def buttonRelease(event):
   if event.x>95 and tool==3:
      drawRectangle(event)
      
def drag(event):
   global points, tool, paint, paintPoints, radius
   if event.x>95 and tool==2:
      #Store coordinates in array
      points.append(event.x)
      points.append(event.y)
      #Use coordinates in array to draw line
      canvas.create_line(points, event.x,event.y, fill='#'+ ("%02x" % r) + ("%02x" % g) + ("%02x" % b), tag="userDrawn")
      return points
   elif event.x>95 and tool==4:
      sprayPaint(event)
   elif event.x>95 and tool==5:
      canvas.create_line(vortexPoints, event.x, event.y, fill='#'+ ("%02x" % r) + ("%02x" % g) + ("%02x" % b), tag="userDrawn")
      
def toolSelect(event):
   global tool
   if tool==1:
      drawLine(event)
   elif tool==2:
      freeHand(event)
   elif tool==3:
      drawRectangle(event)
   elif tool==4:
      sprayPaint(event)
   elif tool==5:
      vortex(event)
      
def colorSelect(event):
   global r,g,b,redSlider,greenSlider,blueSlider, colorPicker, winOpen
   if event.x<95 and event.y>505:
      #New, separate window for color sliders
      colorPicker = Toplevel()
      colorPicker.wm_title("Color Picker")
      redSlider = Scale(colorPicker, bd=0, activebackground="#9E9E9E", from_=0, to=255, resolution=1, relief="flat", sliderrelief="flat", orient=HORIZONTAL)
      redSlider.set(r)
      redSlider.pack()
      greenSlider = Scale(colorPicker, bd=0, activebackground="#9E9E9E", from_=0, to=255, resolution=1, relief="flat", sliderrelief="flat", orient=HORIZONTAL)
      greenSlider.set(g)
      greenSlider.pack()
      blueSlider = Scale(colorPicker, bd=0, activebackground="#9E9E9E", from_=0, to=255, resolution=1, relief="flat", sliderrelief="flat", orient=HORIZONTAL)
      blueSlider.set(b)
      blueSlider.pack()
      winOpen=True
      colorPicker.bind("<B1-Motion>",colorUpdate)

#Update r,g,b to the slider values     
def colorUpdate(event):
   global r,g,b,redSlider,greenSlider,blueSlider
   r=redSlider.get()
   g=greenSlider.get()
   b=blueSlider.get()
   canvas.create_oval(13, 517, 83, 587, fill='#'+ ("%02x" % r) + ("%02x" % g) + ("%02x" % b))
   #print current hexadecimal color
   print '#'+ ("%02x" % r) + ("%02x" % g) + ("%02x" % b)
   
def drawLine(event):
   global color, tool, linePoints, firstClick
   if event.x>95 and tool==1:
      if firstClick:
         linePoints=[event.x,event.y]
         firstClick=False
      else:
         canvas.create_line(linePoints, event.x, event.y, fill='#'+ ("%02x" % r) + ("%02x" % g) + ("%02x" % b), tag="userDrawn")
         firstClick=True
   
def freeHand(event):
   if event.x>95 and tool==2: 
      global count
      count=0
      #Array to store coordinates
      global points
      points=[]
      if count%2==0:
         points.append(event.x)
         points.append(event.y)
      else:
         canvas.create_line(points, event.x, event.y, fill='#'+ ("%02x" % r) + ("%02x" % g) + ("%02x" % b), tag="userDrawn")
      count+=1
 
def drawRectangle(event):
   global rectCount, rectPoints, color, tool, rectFirstClick
   if event.x>95 and tool==3:
      if rectCount%2==0:
         rectPoints=[event.x,event.y]
         rectFirstClick=False
      else:
         x0,y0 = rectPoints
         x1,y1 = (event.x, event.y)
         canvas.create_rectangle(x0, y0, x1, y1, fill='#'+ ("%02x" % r) + ("%02x" % g) + ("%02x" % b), tag="userDrawn")
      rectCount+=1
         
def sprayPaint(event):
   global radius
   if event.x>95 and tool==4:
      for x in xrange(paint):
         px,py=(event.x + randint(-radius,radius)),(event.y + randint(-radius,radius))
         #Circle formula
         if (px-event.x)**2+(py-event.y)**2<=radius**2:
            canvas.create_line(px, py, px+1, py+1, fill='#'+ ("%02x" % r) + ("%02x" % g) + ("%02x" % b), tag="userDrawn")
         
def vortex(event):
   if event.x>155 and tool==5: 
      #Array to store coordinates
      global vortexPoints
      vortexPoints=[]
      vortexPoints.append(event.x)
      vortexPoints.append(event.y)
      
#Reset all arrays, clear any user drawn elements         
def clear(event):
   canvas.delete("userDrawn")
   firstClick=True
   rectFirstClick=True
   rectPoints=[]
   linePoints=[]
   vortexPoints=[]
   points=[]
   tool=1
  
#Show window
canvas.pack()
root.bind("<Button-1>", click)
#Bind left button drag to function
root.bind("<B1-Motion>", drag)
root.bind("<ButtonRelease-1>", buttonRelease)
root.bind('c', clear)
root.mainloop()
