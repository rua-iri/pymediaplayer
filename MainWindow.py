import tkinter as tk
import requests
import json

from Video import Video



def searchButtonFunct(event):
    entryText = srchEntry.get()
    searchYT(entryText)



def searchYT(searchQuery):
    searchApiUrl = "https://inv.odyssey346.dev/api/v1/search?q=" + searchQuery
    searchRes = requests.get(searchApiUrl)
    searchData = json.loads(searchRes.text)

    for dat in searchData:
        try:
            vidList.append(Video(dat["title"], dat["videoId"], dat["videoThumbnails"][0]["url"]))
        except:
            print("Title Not Found")
    
    if len(vidList)<10:
        for vid in vidList:
            showResult(vid)
    
    else:
        for i in range(10):
            showResult(vidList[i])
            



def showResult(vdo):
    labFram = tk.LabelFrame(window, pady=2)
    labFram.pack()

    #label for the video title
    vidLabel = tk.Label(labFram, text=vdo.title, padx=2);
    vidLabel.pack(side=tk.LEFT)

    #button to open the video
    vidButton = tk.Button(labFram, text="Watch", command= lambda: openVideo(vdo.url))
    vidButton.pack(side=tk.RIGHT)


def openVideo(videoCode):
    print(videoCode)


vidList = []
window = tk.Tk()
window.attributes('-zoomed', True)

greeting = tk.Label(text="blah")
greeting.pack()


srchEntry = tk.Entry(width=25)
srchBtn = tk.Button(text="Search", width=5)

srchEntry.pack()
srchBtn.pack()

srchBtn.bind("<Button-1>", searchButtonFunct)


window.mainloop()


