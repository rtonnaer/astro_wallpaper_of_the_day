import os
import requests
import sys
import wget
import ctypes
import glob
from PIL import Image, ImageFont, ImageDraw 
import textwrap


# get some of the users paths
userPicPath = os.path.join(os.environ["USERPROFILE"],'Pictures')

# Check if the folder nasa_apod exists in the users picturs folder if it doesn`t, create it
dirsInPictures = [folder[0].split("\\")[-1] for folder in os.walk(userPicPath)]
if not ("nasa_apod" in dirsInPictures):
    os.mkdir(os.path.join(userPicPath,'nasa_apod'))

userAPODPicPath = os.path.join(userPicPath,'nasa_apod')

filesInAPODPicPath = glob.glob(os.path.join(userAPODPicPath,"*"))
for file in filesInAPODPicPath:
    os.remove(file)

# get nasa-api-key from env variable
nasaAPIKey = os.getenv('nasa_api_key')

# connect to nasa webapi for todays astronomy picture of the day + some of the metadata
nasaAPIUrl = 'https://api.nasa.gov/planetary/apod?api_key=' + str(nasaAPIKey)
nasaResponse = requests.get(url = nasaAPIUrl)
nasaAPODFull = nasaResponse.json()
nasaAPODExpl = nasaAPODFull.get('explanation')
nasaAPODHDUrl = nasaAPODFull.get('hdurl')

nasaAPODExplLines = nasaAPODExpl.split(".")
nasaAPODExplShort = ""

for i in range(0,3):
    cleanLine = nasaAPODExplLines[i].strip()
    if i == 0:
        nasaAPODExplShort = cleanLine
    elif i == 2:
        nasaAPODExplShort = nasaAPODExplShort + ". " + cleanLine + "."
    else:
        nasaAPODExplShort = nasaAPODExplShort + ". " + cleanLine

# Store the hd image into apod
response = wget.download(nasaAPODHDUrl,userAPODPicPath,)

# Get the Image name in apod folder
apodName = os.listdir(userAPODPicPath)[0]
apodPath = os.path.join(userAPODPicPath,apodName)

# Add the description of the image to the image itself (as an overlay)
image = Image.open(apodPath) # open the image
image = image.resize((1920,1080)) # resize the image so it is native to the screen resolution
imgW, imgH = image.size # get the size of the image as variables
descriptionFont = ImageFont.truetype('Helvetica-Oblique.ttf', 35) # set the font and font size
imageEditable = ImageDraw.Draw(image) # create a editable version of the image we loaded
nasaAPODExplWrapped = textwrap.wrap(nasaAPODExplShort,100) # take the short description, and cut it up into 100 char long strings
nStrings = len(nasaAPODExplWrapped) # get the number of strings we need to place at the bottom of the page

# iterate over the textwrapped strings, and place them on the image
yShift = -50 # manual shift of y position to prevent text to dissappear behind the taskbar
for line in nasaAPODExplWrapped:
    lineW, lineH = descriptionFont.getsize(line) # get the dimensions of the string that needs to be placed
    # calculate the x and y positions of the current line
    xPos = imgW/2 - lineW/2 # the center of the line should be centered in the image
    yPos = imgH - (nStrings*lineH) + yShift # the first string needs to be placed nString times above the bottom of the image
    imageEditable.text((xPos, yPos), line, (254, 203, 117), font=descriptionFont)
    nStrings -= 1

annotatedApodPath = os.path.join(userAPODPicPath,'annotatedWallpaper.jpg')
image.save(annotatedApodPath)

# set the image as windows background using ctypes
ctypes.windll.user32.SystemParametersInfoW(20, 0, annotatedApodPath , 0)







