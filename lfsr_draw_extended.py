# All of the paremeters used for drawing
# Note that the paremeters are not dependend of each other so that this gives flexibility
# For example: youu are free to make thicker lines or smaller boxes
import matplotlib.pyplot as plt
import io
from PIL import Image, ImageChops
import time
import string    
import random
import os
from contextlib import redirect_stdout
import mdtex2html
import sympy
from pylatex import (Document, TikZ, TikZNode,
                     TikZDraw, TikZCoordinate,
                     TikZUserPath, TikZOptions,NoEscape)
from pdf2image import convert_from_path
import argparse
#The background color
backgorundcolor = "white"

#The Border Size around the figure in mm
borderSize = 15

#All lines, including the boxes
lineWidth = "0.1"
#Circles tend to seem smaller, you may want to increase it
cirleLineWidth = "0.12"
#Some likes bigger arrowHead
arrowHead = "0.5"

#Size of the LFSR box cm
boxSize = 4
#box Color use Tikz format
boxColor = "{{rgb:black,0;white,5}}"

#used for the distance of the box variable names 
boxBelowTextDistance = 6

#size of the x-or drawing cm
xorSize = 1

# How for the Xor's must be printed
xorDistance = boxSize/2

#For the box values.
BoxValuesFontSize = "30pt"

#For the box indexes.
BoxIndexFontSize = "20pt"

#For the box values.
FeedBackPolyFontSize = "30pt"

#Set True if you want the LFSR is filled with initial values.
drawInitValues = True

#Set True if you want the LFSR's box names are written under.
printBoxNames = True

#strating position of the first box.
x = 25
y = 20

#Determines how far left does the feedback line go
lefFeedbackDestance = 2 * boxSize

#Latex preample for standalone Tikz
def printPreample():

     print('\\documentclass[convert={density=300,size=1080x800,outext=.png},tikz]{standalone}')


     print("\\usepackage{xcolor}")
     print("\\usepackage{scalerel}")
     print("\\usepackage{amsmath}")
     print("\\usetikzlibrary{arrows.meta,backgrounds}")
     print("\\tikzset{{white background/.style={{show background rectangle,tight background,background rectangle/.style={{fill={0} }} }} }}".format(backgorundcolor))
     print("")
     print("\\begin{document}")
     print("\\begin{tikzpicture}[white background]\n\n")

#Latex end
def printPrologue():
     #https://tex.stackexchange.com/a/596158/62865
     print("\\path (current bounding box.north east) +({0}mm,{0}mm) (current bounding box.south west) +(-{0}mm,-{0}mm);".format(borderSize) )
     print("\n\\end{tikzpicture}")
     print("\\end{document}")
     
#Prints the LFSr Boxes if printBoxNames==True then the values are printed,too
def printSquare(x1,y1,value, index):
    
    print('%node {0}'.format(index))
    
    if drawInitValues == True:
        if printBoxNames == True:
            print('\t\draw node[draw, fill={8}, minimum size={3}cm,line width={4}cm, label={{ [yshift=-{9}cm] {{ $\scaleto{{x_{{ {7} }} }}{{ {6} }}$ }} }} ] at ({0}, {1}) {{ $\scaleto{{ {2} }}{{ {5} }}$ }};'.format(x1,y1,value,boxSize,lineWidth,BoxValuesFontSize, BoxIndexFontSize,index,boxColor,boxBelowTextDistance))
        else:
            print('\t\draw node[draw, fill={7}, minimum size={3}cm,line width={4}cm] at ({0}, {1}) {{ $\scaleto{{ {2} }}{{ {5} }}$ }};'.format(x1,y1,value,boxSize,lineWidth,BoxValuesFontSize, BoxIndexFontSize,boxColor))
    else:
        if printBoxNames == True:
            print('\t\draw node[draw, fill={8}, minimum size={3}cm,line width={4}cm, label={{ [yshift=-{9}cm] {{ $\scaleto{{x_{{ {7} }} }}{{ {6} }}$ }} }} ] at ({0}, {1}) {{ }} ;'.format(x1,y1,value,boxSize,lineWidth,BoxValuesFontSize, BoxIndexFontSize,index,boxColor,boxBelowTextDistance))
        else:
            print('\t\draw node[draw, fill={7}, minimum size={3}cm,line width={4}cm] at ({0}, {1}) {{ }};'.format(x1,y1,value,boxSize,lineWidth,BoxValuesFontSize, BoxIndexFontSize,boxColor))
 
#The arrow from a box to x-or if it is a tap point. 
def printTapLine(x1,y1,length, arrow=False):
    if arrow:
        print('\t\draw [arrows={{-Triangle[angle=90:{5}cm,black,fill=black,line width={4}cm]}},line width={4}cm]({0},{1}) -- ({2},{3});'.format(x1,y1,x1,y1+length,lineWidth,arrowHead))
    else:
        print('\t\draw [line width={4}cm]({0},{1}) -- ({2},{3});'.format(x1,y1,x1,y1+length,lineWidth))
        
def printArrow(x1,y1):
    print('\t\draw [arrows={{-Triangle[angle=90:{5}cm,black,fill=black,line width={4}cm]}}]({0},{1}) -- ({2},{3});'.format(x1,y1,x1-0.0001,y1,lineWidth,arrowHead))
    
def printXor(x1,y1):
    print('\t\\draw [line width={3}cm] ({0},{1}) circle ({2});'.format(x1,y1,xorSize,cirleLineWidth))
    
    lx1 = x1
    lx2 = x1
    ly1 = y1-xorSize
    ly2 = y1+xorSize
    
    print('\t\draw [line width={4}cm]({0},{1}) -- ({2},{3});'.format(lx1,ly1,lx2,ly2,cirleLineWidth))
    
    lx1 = x1 - xorSize
    lx2 = x1 + xorSize
    ly1 = y1
    ly2 = y1
    
    print('\t\draw [line width={4}cm]({0},{1}) -- ({2},{3});'.format(lx1,ly1,lx2,ly2,cirleLineWidth))

def printToplineAndFeedbackArrow(x1, x2, x3, y1, y2, feedback, boxsizehalf):
    if drawInitValues:
        print('\draw[->,line width=0.1cm,arrows={{-Triangle[angle=90:{6}cm,black,fill=black,line width={5}cm]}}] ({0},{3}) -- ({1},{3}) -- ({1},{4}) -- node[above,yshift={9}cm] {{ $\scaleto{{ {8} }}{{ {7} }}$ }}  ({2},{4});'.format(x1, x2, x3, y1, y2,lineWidth,arrowHead,BoxValuesFontSize,feedback,boxsizehalf))
    else:
        print('\draw[->,line width=0.1cm,arrows={{-Triangle[angle=90:{6}cm,black,fill=black,line width={5}cm]}}] ({0},{3}) -- ({1},{3}) -- ({1},{4}) -- ({2},{4});'.format(x1, x2, x3, y1, y2,lineWidth,arrowHead,BoxValuesFontSize,feedback,boxsizehalf))
        
def printOutputArrow(x1, x2, y1,value,boxsizehalf):
    
    if drawInitValues:
        print('\draw[->,line width=0.1cm,arrows={{-Triangle[angle=90:{4}cm,black,fill=black,line width={3}cm]}}] ({0},{2}) -- ({1},{2}) node[midway,above,yshift={7}cm]{{  $\scaleto{{  {6}  }}{{ {5} }}$  }};'.format(x1, x2, y1, lineWidth,arrowHead, BoxValuesFontSize, value,boxsizehalf))
    else:
        print('\draw[->,line width=0.1cm,arrows={{-Triangle[angle=90:{4}cm,black,fill=black,line width={3}cm]}}] ({0},{2}) -- ({1},{2}) node[midway,above]{{}};'.format(x1, x2, y1, lineWidth,arrowHead, BoxValuesFontSize))

def printFeedBackPolynomial(lfsr):
    count = lfsr.count(1)
    feedBackPolynomail ="$\scaleto{\\text{The Feedback Polynomial is } (x) = x^{" + str(len(lfsr)) + "}+" 

    for i, val in enumerate(lfsr):
        if val == 1:
            if len(lfsr) - i -1 == 0:
                feedBackPolynomail += "1"
            else:
                feedBackPolynomail += "x^" + str(len(lfsr) - i -1)
            if count > 1:
                feedBackPolynomail += "+"
            count = count -1
            
    feedBackPolynomail += "}{"+ FeedBackPolyFontSize+ "}$"    

    feedBackPolynomailX = x+ (boxSize* (len(lfsr))) / 2
    feedBackPolynomailY = y - boxSize * 1.5

    print('\draw node[minimum size={3}cm,line width={4}cm] at ({0}, {1}) {{{6}}};'.format(feedBackPolynomailX,feedBackPolynomailY,feedBackPolynomail,boxSize,lineWidth,FeedBackPolyFontSize,feedBackPolynomail))

###############################
#  Now definition of the LFSR
###############################

###############################
#  Feedback calculator for the LFSR
###############################
def calculateFeedBack(taps,values):
    feedback = 0
    for i, tap in enumerate(lfsrTaps):
        if tap == 1:
            feedback = feedback ^ values[i]
    return feedback


###############################
#  Just one function to call to print the LFSR
###############################
def printLFSR(taps, values, printvalues, showBoxNames, printEquation):
    
    global drawInitValues
    global printBoxNames
    
    drawInitValues = printvalues
    printBoxNames = showBoxNames
    
    #We need this inorder to draw the feedback properly
    lastTapPos = 0

    #Latex starts
    printPreample()

    count = taps.count(1)

    for i, val in enumerate(taps):
        
        printSquare(x + i * boxSize, y , values[i] ,len(taps) - i -1)
                
            
        if val == 1:
            if i == len(taps)-1:
                
                printTapLine(x + i * boxSize,y + boxSize/2, xorDistance + xorSize )
            else:
                printTapLine(x + i * boxSize,y + boxSize/2, xorDistance)
                printXor    (x + i * boxSize, y + boxSize/2 + xorDistance + xorSize )
                if count > 1:
                    printArrow(x + i * boxSize + xorSize, y + boxSize/2 + xorDistance + xorSize)

            count = count -1            
            
            lastTapPos = i

    feedbackValue = calculateFeedBack(taps,values)

    printToplineAndFeedbackArrow(x + (lastTapPos )* boxSize ,          #x1
                                x - lefFeedbackDestance,                       #x2
                                x - boxSize /2,                                #x3
                                y + boxSize/2 + xorDistance + xorSize,         #y1
                                y,                                             #y2
                                feedbackValue,                                 # Feedback value
                                boxSize/4                                      #Box size for position of the feedback value
                                )

    printOutputArrow(x + (len(taps) -1) * boxSize + boxSize/2, x + (len(taps) -1) * boxSize + 2 * boxSize, y, values[-1], boxSize/4) 

    if printEquation == True:
        printFeedBackPolynomial(taps)

    #Latex Ends
    printPrologue()
###############################
#  Print n images to output that can be turned into GIF/Videos
###############################
def printLFSRAnimation(taps, values, n, printvalues, showBoxNames, printEquation):
    print("!!! Not Implemented Yet!")




white = (255, 255, 255, 255)

def latex_to_img(tex):
    buf = io.BytesIO()
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.axis('off')
    plt.text(0.05, 0.5, f'${tex}$', size=40)
    plt.savefig(buf, format='png')
    plt.close()

    im = Image.open(buf)
    bg = Image.new(im.mode, im.size, white)
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    return im.crop(bbox)


###############################
#  Now define your LFSR
###############################

#The taps. right most is the x_0 
#lfsrTaps = [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1]

#The inits. left most is the value of x_0 
#initVals = [1,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0]
#sudo apt install texlive texlive-latex-extra texlive-fonts-recommended dvipng
#apt install cm-super
#sudo pip3 install pylatex
#         ( taps,    initial values, print values, box names, print equation )
RANDOM_FOLDER_NAME_LENGHT = 30
def current_milli_time():
    return round(time.time() * 1000)
def current_random_str():
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = RANDOM_FOLDER_NAME_LENGHT))
    return str(ran)  
def create_folder():
    try:
        PATH=str(current_milli_time())+"_"+current_random_str()
        os.mkdir(PATH)
        return PATH
    except OSError as error: 
        return create_folder()
def run(cmd):
    
    
    os.system(cmd)
def latex2png(FOLDER,infile , dpi):
    dvifile =  FOLDER+ '/out.dvi'
    
        
        
    
    
    os.chdir(FOLDER)
    #pdflatex -shell-escape lfsr.tex
    run("sudo pdflatex -shell-escape out.tex")
    pages = convert_from_path('out.pdf', 500)
    i=0
    for page in pages:
        namex="out"+str(++i)+".png"
        page.save(namex, 'PNG')
    
        
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--initvals',  
                    help='INIT VALS [1,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0]')
parser.add_argument('--lfsrtaps',  
                    help='LFSR TAPS [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1]')
args = parser.parse_args()

initVals = list(map(int, args.initvals.split(",")))
lfsrTaps =list(map(int, args.lfsrtaps.split(",")))
FOLDER_NAME=create_folder()
FILE_NAME=str(FOLDER_NAME)+"/out.tex"
with open(FILE_NAME, 'w') as f:
    with redirect_stdout(f):
         printLFSR(lfsrTaps, initVals,        True,          True,          False)
   
text_file = open(FILE_NAME, "r")
 
#read whole file to a string
data = text_file.read()
print(data)
    

#latex_to_img(data).save(PNG_FILE_PATH)
#latex_to_img(data).save(FOLDER_NAME+'/img.png')
htmlfoo = mdtex2html.convert(data)
HTML_FILE_NAME=str(FOLDER_NAME)+"/out.html"
fxx = open(HTML_FILE_NAME, "a")
fxx.write(htmlfoo)
fxx.close()



PNG_FILE_PATH=str(FOLDER_NAME)+"/out.png"
latex2png(FOLDER_NAME,text_file,  72)

#preview(data, viewer='file', filename='test.png', euler=False)