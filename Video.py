
import requests
import json


class Video:
    

    def __init__(self, title, code, thumbnail, author, viewCount, length, publishedText, authorId, baseUrl):
        self.title = title
        self.code = code
        self.thumbnail = thumbnail
        self.author = author
        self.viewCount = viewCount
        self.length = length
        self.publishedText = publishedText
        self.authorId = authorId
        self.baseUrl = baseUrl


    #function for getting more data about a video by querying another endpoint
    def getData(self):
        videoRes = requests.get(self.baseUrl + "/api/v1/videos/" + self.code)
        videoData = json.loads(videoRes.text)
        self.vidUrl = videoData["formatStreams"][-1]["url"]
        self.size = videoData["formatStreams"][-1]["size"]
        

