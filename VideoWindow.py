
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

        self.vidWindow.bind("<Destroy>", self.closeVideoCloseWindow)

        
        self.openVideo()




    def openVideo(self):
        self.vid.getData()

        self.vidMediaPlayer.set_xwindow(self.vidWindow.winfo_id())
        vidMedia = vlc.Media(self.vid.vidUrl)
        self.vidMediaPlayer.set_media(vidMedia)
        self.vidMediaPlayer.play()

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

    

    #function to increase or decrease current time location by five seconds
    def skipAhead(self, event):

        currentTime = self.vidMediaPlayer.get_time()
        self.vidMediaPlayer.set_time(currentTime + 5000)



    #function to increase or decrease current time location by five seconds
    def skipBack(self, event):

        currentTime = self.vidMediaPlayer.get_time()
        self.vidMediaPlayer.set_time(currentTime - 5000)

