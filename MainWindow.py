import tkinter as tk
import requests
import json



def printEntryText(event):
    entryText = srchEntry.get()
    searchYT(entryText)


def searchYT(searchQuery):
    searchApiUrl = "https://inv.odyssey346.dev/api/v1/search?q=" + searchQuery
    searchRes = requests.get(searchApiUrl)
    searchData = json.loads(searchRes.text)

    for dat in searchData:
        try:
            print(dat["title"])
        except:
            print("Title Not Found")



window = tk.Tk()
greeting = tk.Label(text="blah")
greeting.pack()


srchEntry = tk.Entry(text="bleh")
srchBtn = tk.Button(text="Search")

srchEntry.pack()
srchBtn.pack()

srchBtn.bind("<Button-1>", printEntryText)


window.mainloop()


