
import json
import vlc
import tkinter as tk
import requests

class VideoWindow:


    def __init__(self, vid):
        print(vid.title)
        self.vid = vid

        self.vidMediaPlayer = vlc.MediaPlayer()


        self.vidWindow = tk.Tk()
        self.vidWindow.bind("<Key>", self.closeVideo)
        self.vidWindow.title(vid.title)
        
        self.openVideo()




    def openVideo(self):
        self.vid.getData()

        self.vidWindow.geometry(self.vid.size)

        self.vidMediaPlayer.set_xwindow(self.vidWindow.winfo_id())
        vidMedia = vlc.Media(self.vid.vidUrl)
        self.vidMediaPlayer.set_media(vidMedia)
        self.vidMediaPlayer.play()





    #function to stop a video from playing
    def closeVideo(self, event):
        if event.char=="q":
            self.vidMediaPlayer.stop()
            self.vidWindow.destroy()