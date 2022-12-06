import json
import vlc
import requests

class VideoPlayer:

    def __init__(self, vidCode):        
        self.vidCode = vidCode
        self.url = ""
        self.mediaPlayer = vlc.MediaPlayer()


    def getVideoUrl(self):
        videoRes = requests.get("https://inv.odyssey346.dev/api/v1/videos/" + self.vidCode)
        videoData = json.loads(videoRes.text)
        self.url = videoData["formatStreams"][-1]["url"]
        print(self.url)


    def initialiseMedia(self):
        if self.url!="":
            self.media = vlc.Media(self.url)
            self.mediaPlayer = vlc.MediaPlayer(self.media)
        else:
            print("Error: video url not initialised")


    def playVideo(self):
        self.mediaPlayer.play()


    def stopVideo(self):
        self.mediaPlayer.stop()