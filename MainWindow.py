import io
import tkinter as tk
import requests
import json
from PIL import Image, ImageTk
import urllib

from Video import Video
from VideoWindow import VideoWindow


#clear results from list so that new results can appear
def clearResults():
    global vidList, photoList

    vidList = []
    photoList = []

    for wdgt in blahFrame.winfo_children():
        wdgt.destroy()


#function called by pushing the button
def searchButtonFunct(event):
    clearResults()

    entryText = srchEntry.get()

    searchLabel = tk.Label(srchFrame, text="Search for: " + entryText, padx=2, width=50, height=5)
    searchLabel.pack(side=tk.TOP)

    searchYT(entryText)



#function to search for relevant videos
def searchYT(searchQuery):
    
    searchApiUrl = "https://inv.odyssey346.dev/api/v1/search?q=" + searchQuery
    searchRes = requests.get(searchApiUrl)
    searchData = json.loads(searchRes.text)

    vidCounter = 0

    for dat in searchData:
        try:
            vidList.append(Video(dat["title"], dat["videoId"], dat["videoThumbnails"][3]["url"], dat["author"], dat["viewCount"], dat["lengthSeconds"], dat["publishedText"]))
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
    
    window.geometry("1000x600")



#function to add the results to labelframes which are attached to the srchFrame
def showResult(vdo, cntr):
    labFram = tk.LabelFrame(blahFrame, pady=4)
    labFram.pack()

    imgPage = urllib.request.urlopen(vdo.thumbnail)
    pilImg = Image.open(io.BytesIO(imgPage.read()))
    tkImg = ImageTk.PhotoImage(pilImg)

    photoList.append(tkImg)
    imgLabel = tk.Label(labFram, image=photoList[cntr])
    imgLabel.pack(side=tk.LEFT)

    #button to open the video
    vidButton = tk.Button(labFram, text=vdo.title, padx=2, width=50, height=5, command= lambda: VideoWindow(vdo))
    vidButton.pack()

    authorLabel = tk.Label(labFram, text=vdo.author, pady=10, padx=2, width=50);
    authorLabel.pack()
    viewsLabel = tk.Label(labFram, text=vdo.viewCount + " views", pady=10, padx=2, width=50);
    viewsLabel.pack()
    lengthLabel = tk.Label(labFram, text=vdo.length + " seconds", pady=10, padx=2, width=50);
    lengthLabel.pack()
    publishedLabel= tk.Label(labFram, text=vdo.publishedText, pady=10, padx=2, width=50);
    publishedLabel.pack()



    # TODO add function to click on channel name and search

    
    


vidList = []
photoList = []


window = tk.Tk()
window.geometry("1000x500")
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


srchFrame = tk.Frame(srchCanvas, width=1000)
srchCanvas.create_window((0,0), window=srchFrame, anchor="nw")


srchEntry = tk.Entry(srchFrame, width=50)
srchEntry.pack(pady=(10,10), padx=(300, 300))

srchBtn = tk.Button(srchFrame, text="Search", width=25, height=2)
srchBtn.pack(pady=(10,10), padx=(300, 300))


blahFrame = tk.Frame(srchFrame, width=1000)
blahFrame.pack()


srchBtn.bind("<Button-1>", searchButtonFunct)



window.mainloop()


