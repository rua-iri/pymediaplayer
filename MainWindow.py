import io
import tkinter as tk
import requests
import json
from PIL import Image, ImageTk
import urllib

from Video import Video



#function called by pushing the button
def searchButtonFunct(event):
    entryText = srchEntry.get()
    searchYT(entryText)



#function to search for relevant videos
def searchYT(searchQuery):
    searchApiUrl = "https://inv.odyssey346.dev/api/v1/search?q=" + searchQuery
    searchRes = requests.get(searchApiUrl)
    searchData = json.loads(searchRes.text)

    vidCounter = 0

    for dat in searchData:
        try:
            vidList.append(Video(dat["title"], dat["videoId"], dat["videoThumbnails"][3]["url"]))
        except:
            print("Title Not Found")
    
    if len(vidList)<10:
        for vid in vidList:
            showResult(vid, vidCounter)
            vidCounter+=1
    
    else:
        for i in range(10):
            showResult(vidList[i], vidCounter)
            vidCounter+=1
    
    window.geometry("1000x400")

            



def showResult(vdo, cntr):
    labFram = tk.LabelFrame(srchFrame, pady=2)
    labFram.pack()


    imgPage = urllib.request.urlopen(vdo.thumbnail)
    pilImg = Image.open(io.BytesIO(imgPage.read()))
    tkImg = ImageTk.PhotoImage(pilImg)

    photoList.append(tkImg)
    imgLabel = tk.Label(labFram, image=photoList[cntr])
    imgLabel.pack(side=tk.LEFT)

    
    print(vdo.thumbnail)


    #label for the video title
    vidLabel = tk.Label(labFram, text=vdo.title, padx=2);
    vidLabel.pack()

    #button to open the video
    vidButton = tk.Button(labFram, text="Watch", command= lambda: openVideo(vdo.url))
    vidButton.pack(side=tk.RIGHT)


#TODO open a new window with the videos
#function to play youtube videos
def openVideo(videoCode):
    print(videoCode)


vidList = []
photoList = []

window = tk.Tk()
# window.resizable(False, False)
window.title("PyYTPlayer")


mainFrame = tk.Frame(window)
mainFrame.pack(fill=tk.BOTH, expand=1)


#Set canvas, frame and scrollbar
srchCanvas = tk.Canvas(mainFrame)
srchCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

searchScrollbar = tk.Scrollbar(mainFrame, orient=tk.VERTICAL, command=srchCanvas.yview)
searchScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

srchCanvas.configure(yscrollcommand=searchScrollbar.set)
srchCanvas.bind("<Configure>", lambda evnt: srchCanvas.configure(scrollregion=srchCanvas.bbox("all")))


srchFrame = tk.Frame(srchCanvas)
srchCanvas.create_window((0,0), window=srchFrame, anchor="nw")


srchEntry = tk.Entry(srchFrame, width=25)
srchEntry.pack(pady=(10,10))

srchBtn = tk.Button(srchFrame, text="Search", width=5)
srchBtn.pack()

srchBtn.bind("<Button-1>", searchButtonFunct)


window.mainloop()


