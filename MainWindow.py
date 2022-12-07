import datetime
import io
import tkinter as tk
import requests
import json
from PIL import Image, ImageTk
import urllib

from Video import Video
from VideoWindow import VideoWindow


#function to get an instance on invidious
def getInstance():
    instanceRes = requests.get("https://api.invidious.io/instances.json?pretty=1&sort_by=type,users")
    instanceData = json.loads(instanceRes.text)
    



#clear results from list so that new results can appear
def clearResults():
    global vidList, photoList

    vidList = []
    photoList = []

    for wdgt in resultsFrame.winfo_children():
        wdgt.destroy()



#function called by pushing the button
def searchButtonFunct(event):
    entryText = srchEntry.get().strip()

    #check that the textbox isn't empty
    if entryText!="":
        genSearchLabel("Search for: " + entryText)
        searchYT(entryText)



#function to focus on searchbar if / key is pressed (just like google, youtube etc)
def focusSearchBar(evnt):
    if evnt.char=="/":
        srchEntry.focus()
        srchCanvas.yview_moveto(0.0)



#function to generate the label at the top of every search
def genSearchLabel(labelText):
    searchLabel = tk.Label(resultsFrame, text=labelText, font=("Arial", 25))
    searchLabel.pack(side=tk.TOP, padx=2, pady=(20, 10))



#function to search for relevant videos
def searchYT(searchQuery):
    clearResults()

    # TODO add function to check for active instances with an api from https://api.invidious.io/instances.json

    searchApiUrl = "https://vid.puffyan.us/api/v1/search?q=" + searchQuery
    searchRes = requests.get(searchApiUrl)
    searchData = json.loads(searchRes.text)

    vidCounter = 0

    for dat in searchData:
        try:
            vidList.append(Video(dat["title"], dat["videoId"], dat["videoThumbnails"][3]["url"], dat["author"], dat["viewCount"], dat["lengthSeconds"], dat["publishedText"], dat["authorId"]))
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



#function to search for relevant videos
def searchChannel(channelName, channelId):
    clearResults()

    searchApiUrl = "https://vid.puffyan.us/api/v1/channels/latest/" + channelId
    searchRes = requests.get(searchApiUrl)
    searchData = json.loads(searchRes.text)

    vidCounter = 0

    for dat in searchData:
        try:
            vidList.append(Video(dat["title"], dat["videoId"], dat["videoThumbnails"][3]["url"], channelName, dat["viewCount"], dat["lengthSeconds"], dat["publishedText"], dat["authorId"]))
        except:
            print("Title Not Found")


    genSearchLabel(vidList[0].author)
    
    if len(vidList)<10:
        for vid in vidList:
            showResult(vid, vidCounter)
            vidCounter+=1
    else:
        for i in range(10):
            showResult(vidList[i], vidCounter)
            vidCounter+=1
    
    window.geometry("1000x600")



#function to search trending videos (for some reason this needs an argument even if it's set to None)
def searchTrending(arg=None):
    clearResults()

    genSearchLabel("Trending")

    searchApiUrl = "https://vid.puffyan.us/api/v1/popular"
    searchRes = requests.get(searchApiUrl)
    searchData = json.loads(searchRes.text)

    vidCounter = 0

    #only add the first 10 videos to the trending page
    while len(vidList)<11:
        try:
            vidList.append(Video(searchData[vidCounter]["title"], searchData[vidCounter]["videoId"], searchData[vidCounter]["videoThumbnails"][3]["url"], searchData[vidCounter]["author"], searchData[vidCounter]["viewCount"], searchData[vidCounter]["lengthSeconds"], searchData[vidCounter]["publishedText"], searchData[vidCounter]["authorId"]))
        except:
            print("Title Not Found")
        
        vidCounter+=1

    vidCounter = 0
    
    for vid in vidList:
            showResult(vid, vidCounter)
            vidCounter+=1
    
    window.geometry("1000x600")



#function to add the results to labelframes which are attached to the srchFrame
def showResult(vdo, cntr):
    labFram = tk.LabelFrame(resultsFrame)
    labFram.pack()

    imgPage = urllib.request.urlopen(vdo.thumbnail)
    pilImg = Image.open(io.BytesIO(imgPage.read()))
    tkImg = ImageTk.PhotoImage(pilImg)

    photoList.append(tkImg)
    imgLabel = tk.Label(labFram, image=photoList[cntr])
    imgLabel.pack(side=tk.LEFT)

    #button to open the video
    vidButton = tk.Button(labFram, text=vdo.title, padx=2, width=50, height=5, wraplength=300, command= lambda: VideoWindow(vdo))
    vidButton.pack()

    #button to search the author's channel
    authorButton = tk.Button(labFram, text=vdo.author, pady=10, padx=2, width=50, height=5, command= lambda: searchChannel(vdo.author, vdo.authorId))
    authorButton.pack()
    viewsLabel = tk.Label(labFram, text=("{:,}".format(vdo.viewCount) + " views"), pady=10, padx=2, width=50);
    viewsLabel.pack()

    vidLength = str(datetime.timedelta(seconds=vdo.length))
    lengthLabel = tk.Label(labFram, text=vidLength, pady=10, padx=2, width=50);
    lengthLabel.pack()
    publishedLabel= tk.Label(labFram, text=vdo.publishedText, pady=10, padx=2, width=50);
    publishedLabel.pack()




# empty lists to hold data about currently selected videos
vidList = []
photoList = []

#main window for the application
window = tk.Tk()
window.geometry("1000x500")
window.title("PyYTPlayer")

window.tk.call("source", "assets/Azure-ttk-theme-main/azure.tcl")
window.tk.call("set_theme", "light")

mainFrame = tk.Frame(window)
mainFrame.pack(fill=tk.BOTH, expand=1)

#Set canvas, frame and scrollbar
srchCanvas = tk.Canvas(mainFrame)
srchCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

srchScrollbar = tk.Scrollbar(mainFrame, orient=tk.VERTICAL, command=srchCanvas.yview)
srchScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

#bindings for scrolling page
srchCanvas.bind("<1>", lambda evnt: srchCanvas.focus_set())
srchCanvas.configure(yscrollcommand=srchScrollbar.set)
srchCanvas.bind("<Configure>", lambda evnt: srchCanvas.configure(scrollregion=srchCanvas.bbox("all")))
srchCanvas.bind("<Up>", lambda evnt: srchCanvas.yview_scroll(-1, "units"))
srchCanvas.bind("<Down>", lambda evnt: srchCanvas.yview_scroll(1, "units"))

srchCanvas.focus_set()


srchFrame = tk.Frame(srchCanvas, width=1000)
srchCanvas.create_window((0,0), window=srchFrame, anchor="nw")


# LabelFrame for the search bar
srchLabFrame = tk.LabelFrame(srchFrame, pady=4)
srchLabFrame.pack()

# search bar widgets
logoImg = tk.PhotoImage(file="./assets/youtube-icon-blue.png")
homeBtn = tk.Button(srchLabFrame, image=logoImg)
homeBtn.pack(side=tk.LEFT, pady=(10,10), padx=(15, 15))
srchBtn = tk.Button(srchLabFrame, text="Search", width=25, height=2)
srchBtn.pack(side=tk.RIGHT, pady=(10,10), padx=(15, 15))
srchEntry = tk.Entry(srchLabFrame,font=("Arial", 16), width=30)
srchEntry.pack(side=tk.RIGHT, pady=(10,10), padx=(15, 15))



resultsFrame = tk.Frame(srchFrame, width=1000)
resultsFrame.pack()

searchTrending()


# TODO maybe add vim keybindings to control the application


#bind search button and text entry box to search function
srchBtn.bind("<Button-1>", searchButtonFunct)
srchBtn.bind("<space>", searchButtonFunct)
srchEntry.bind("<Return>", searchButtonFunct)

homeBtn.bind("<Button-1>", searchTrending)

window.bind("<Key>", focusSearchBar)

window.mainloop()

