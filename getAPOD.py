import os
import requests
import sys
import wget
import ctypes
import glob

# get some of the users paths
userPicPath = os.path.join(os.environ["USERPROFILE"],'Pictures')

# Check if the folder nasa_apod exists in the users picturs folder if it doesn`t, create it
dirsInPictures = [folder[0].split("\\")[-1] for folder in os.walk(userPicPath)]
if not ("nasa_apod" in dirsInPictures):
    os.mkdir(os.path.join(userPicPath,'nasa_apod'))

userAPODPicPath = os.path.join(userPicPath,'nasa_apod')

# if the folder exists, check if there already is a file in it. If so, delete it (can be refined later)
if len(os.listdir(userAPODPicPath)) != 0:
     fName = os.listdir(userAPODPicPath)[0]
     os.remove(os.path.join(userAPODPicPath,fName))

# get nasa-api-key from env variable
nasaAPIKey = os.getenv('nasa_api_key')

# connect to nasa webapi for todays astronomy picture of the day + some of the metadata
nasaAPIUrl = 'https://api.nasa.gov/planetary/apod?api_key=' + str(nasaAPIKey)
nasaResponse = requests.get(url = nasaAPIUrl)
nasaAPODFull = nasaResponse.json()
nasaAPODExpl = nasaAPODFull.get('explanation')
nasaAPODHDUrl = nasaAPODFull.get('hdurl')

# Store the hd image into apod
response = wget.download(nasaAPODHDUrl,userAPODPicPath,)

# Get the Image name in apod folder
apodName = os.listdir(userAPODPicPath)[0]
apodPath = os.path.join(userAPODPicPath,apodName)

# set the image as windows background using ctypes
ctypes.windll.user32.SystemParametersInfoW(20, 0, apodPath , 0)
print(apodName)






