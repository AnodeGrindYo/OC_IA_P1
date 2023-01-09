import requests
import os
import zipfile

'''use this script if you want to download the data and unzip them in ./data/'''

zipPath = "./data.zip"

print("downloading the zip file...")
url = 'https://s3-eu-west-1.amazonaws.com/static.oc-static.com/prod/courses/files/AI+Engineer/Project+1+Discover+the+AI%C2%A0Engineer+Job/Dataset+project+1+AI%C2%A0Engineer.zip'
r = requests.get(url, allow_redirects=True)

print("writing the zip file")
open(zipPath, "wb").write(r.content)

path = "./data"
print("checking if data folder already exists...")
if(not os.path.exists(path)):
    print("creating data folder")
    os.makedirs(path)

print("unziping the data...")
with zipfile.ZipFile(zipPath, 'r') as zip_ref:
    zip_ref.extractall(path)
    
print("deleting the zip file...")
os.remove(zipPath)

print("Done !")