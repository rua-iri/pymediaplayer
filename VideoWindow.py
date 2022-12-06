
import datetime
import math
import time
import vlc
import tkinter as tk

class VideoWindow:


    def __init__(self, vid):
        print(vid.title)
        self.vid = vid

        self.vidMediaPlayer = vlc.MediaPlayer()

        self.vidWindow = tk.Tk()
        self.vidWindow.title(vid.title)

        #bind the keys to control the player
        self.vidWindow.bind("<Key>", self.closeVideo)
        self.vidWindow.bind("<space>", self.playPauseVideo)
        self.vidWindow.bind("<Left>", self.skipBack)
        self.vidWindow.bind("<Right>", self.skipAhead)
        self.vidWindow.bind("<Up>", self.volumeUp)
        self.vidWindow.bind("<Down>", self.volumeDown)

        self.vidWindow.bind("<Destroy>", self.closeVideoCloseWindow)
        
        self.openVideo()



    #function to open a new mediaplayer and play the selected video
    def openVideo(self):
        self.vid.getData()

        self.dataFrame = tk.Frame(self.vidWindow)
        self.dataFrame.pack()

        self.vidMediaPlayer.set_xwindow(self.vidWindow.winfo_id())
        vidMedia = vlc.Media(self.vid.vidUrl)
        self.vidMediaPlayer.set_media(vidMedia)
        self.vidMediaPlayer.play()
        self.vidMediaPlayer.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, True)

        #resize the window to match the video size
        self.vidWindow.geometry(self.vid.size)

    

    #functions to stop a video from playing
    def closeVideo(self, event):
        if event.char=="q":
            self.vidMediaPlayer.stop()
            self.vidWindow.destroy()

    def closeVideoCloseWindow(self, event):
        self.vidMediaPlayer.stop()



    #function to toggle the play/pause state of the video    
    def playPauseVideo(self, event):

        if self.vidMediaPlayer.is_playing():
            self.vidMediaPlayer.pause()
        else:
            self.vidMediaPlayer.play()

        self.showTimeSymbol()

    

    #function to increase or decrease current time location by five seconds
    def skipAhead(self, event):
        currentTime = self.vidMediaPlayer.get_time()
        self.vidMediaPlayer.set_time(currentTime + 5000)
        self.showTimeSymbol()



    #function to increase or decrease current time location by five seconds
    def skipBack(self, event):
        currentTime = self.vidMediaPlayer.get_time()
        self.vidMediaPlayer.set_time(currentTime - 5000)
        self.showTimeSymbol()


    #function to increase volume
    def volumeUp(self, event):
        currentVol = self.vidMediaPlayer.audio_get_volume()

        if currentVol<150:
            self.vidMediaPlayer.audio_set_volume(currentVol + 10)

            self.showVolumeSymbol()



    #function to decrease volume
    def volumeDown(self, event):
        currentVol = self.vidMediaPlayer.audio_get_volume()

        if currentVol>0:
            self.vidMediaPlayer.audio_set_volume(currentVol - 10)

            self.showVolumeSymbol()



    #function to show volume bar over the video
    def showVolumeSymbol(self):
        #add time delay so that updated volume level is read instead of old
        time.sleep(0.01)
        
        currentVol = self.vidMediaPlayer.audio_get_volume()
        volSymbol = ""

        #generate volume symbol based on what percentage the volume is at (0%-150%)
        for i in range(math.ceil(currentVol / 10)):
                volSymbol+="|"
            
        for x in range(math.ceil(15 - (currentVol / 10))):
            volSymbol+="."


        self.vidMediaPlayer.video_set_marquee_string(vlc.VideoMarqueeOption.Text, volSymbol)
        self.vidMediaPlayer.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, 2000)


    
    #function to show the current time against the total length of the video
    def showTimeSymbol(self):
        #current time and full time
        cTime = str(datetime.timedelta(seconds=math.floor(self.vidMediaPlayer.get_time()/1000)))
        fTime = str(datetime.timedelta(seconds=math.floor(self.vidMediaPlayer.get_length()/1000)))
        timeSymbol = cTime + " / " + fTime

        self.vidMediaPlayer.video_set_marquee_string(vlc.VideoMarqueeOption.Text, timeSymbol)
        self.vidMediaPlayer.video_set_marquee_int(vlc.VideoMarqueeOption.Timeout, 2000)
