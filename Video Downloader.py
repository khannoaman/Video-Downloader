import requests
import re
import os
from tqdm import tqdm
import sys
import subprocess




url=input("Please Provide the url of video source.\n->")

if re.findall(r'^blob',url):

    url = input("\nSince this is a blob Url, Please Provide the Url of master.m3u8 file.\n->")

    try:
        r = requests.get(url)
    except Exception as e:
        print("Invalid Url.\n", e)
        sys.exit()

    res = re.findall(r'BANDWIDTH=\d+?,RESOLUTION=\d{3,4}x\d{3}', r.text)
    res_links = [i.strip() for i in re.findall(r'https://.*?\n', r.text)]
    print()

    if res==[] or res_links==[]:
        print("\nThis is not a Url of master.m3u8 file.\nPlease Provide Correct Url.\n")
        sys.exit()

    for i,j in enumerate(res):
        print("{}- {}".format(i+1,j))

    inp=int(input("\nWhich RESOLUTION you want to download?(1-{})\n->".format(len(res))))

    try:
        r = requests.get(res_links[inp-1])
    except Exception as e:
        print("\nCan't reach this resolution's video links.\n",e)

    videots_links = [i.strip() for i in re.findall(r'https://.*?\n', r.text)]

    if videots_links==[]:
        print("\nCan't find video links.\n")
        sys.exit()

    Downloads = os.path.normpath(os.path.expanduser("~/Downloads"))
    if not os.path.exists(Downloads + "/video.ts" ):
        path=Downloads + "/video.ts"
    else:
        a = 1
        while True:
            path = Downloads + "/video " + str(a)+".ts"
            if not os.path.exists(path):
                break
            a += 1


    print("\nDownloading Video\n")

    try:
        file = open(path, "wb")
        for i in tqdm(videots_links):
            if ".ts" in i:
                r = requests.get(i)
                if b'\0' not in r.content:
                    print("\nInvalid Content.\nPlease Provide video Source Url.")
                    sys.exit()
                file.write(r.content)
        file.close()
    except Exception as e:
        print(e)
    print("\nDownloading Complete")
    x=input("\nDo you want to Convert your video into mp4?(yes/no)\n->")
    if x.lower()=="yes":
        print("\nConverting to mp4.\n")
        tqdm(subprocess.run(['ffmpeg', '-i',path,path[:len(path)-3]+".mp4"]))
        print("\nDone")


else:
    try:
        r=requests.get(url,stream=True)
    except Exception as e:
        print("Invalid Url.\n",e)
        sys.exit()

    if b'\0' not in r.content:
        print("\nInvalid Content.\nPlease Provide video Source Url.")
        sys.exit()



    Downloads = os.path.normpath(os.path.expanduser("~/Downloads"))
    if not os.path.exists(Downloads + "/video.mp4" ):
        path=Downloads + "/video.mp4"
    else:
        a = 1
        while True:
            path = Downloads + "/video " + str(a)+".mp4"
            if not os.path.exists(path):
                break
            a += 1


    print("\nDownloading Video\n")
    chunk = 256
    try:
        file=open(path,"wb")
        for content in tqdm(r.iter_content(chunk_size=chunk)):
            file.write(content)
        file.close()
    except Exception as e:
        print(e)
        sys.exit()

    print("\nDownloading Complete")