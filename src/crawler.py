from threading import Thread
import urllib.request
import re
from bs4 import BeautifulSoup
import requests
import time
from threadPoolCrawler import threadPoolCrawler
from state import State
from Queue import Queue

class ImageDownloader:
    
    def __init__(self, param1):
        self.urls = param1
        self.threadList=[]
        self.threadPool = threadPoolCrawler(20) 
        self.readUrls = set([])
        self.to_crawl = Queue()
        self.prepared = State.WAITING
        self.startFutures = set([])


    def prepareExecution(self):
        if self.prepared == State.WAITING:
            self.prepared = State.RUNNING
            with open (self.urls, 'r') as urls:
                line = urls.readline()
                while line:
                    self.prepared = State.RUNNING
                    self.threadPool.submit(self.getImageUrls, line)
                    print(line)
                    line =  urls.readline()
    
    
    def download(self, url):
        try:
            if(not("http" in url)):
                url = "http:" + url
            r = requests.get(url)
            
            namePath="./downloaded photos/"+str(url).split('/').pop()
            with open (namePath, 'wb') as f:
                f.write(r.content)

    def getImageUrls(self, urls):
        srcImage = ''
        with urllib.request.urlopen(urls) as url:
            htmltext = url.read()
            soup = BeautifulSoup(htmltext, "html.parser")
            images = []
            images = soup('img')

            for image in images:
                if(image.get('src') != None):
                    srcImage = image.get('src')
                self.to_crawl.put(srcImage)  

    def start(self):
        self.prepareExecution()

        execThread = Thread(target = self.threadPool.run, args=())
        execThread.start()
        
        while self.threadPool.state is not State.DONE:
            try:
                current_url=self.to_crawl.get(timeout=60)
                if current_url not in self.readUrls:
                    self.readUrls.add(current_url)
                    self.threadPool.submit(self.download, current_url)

if __name__ == "__main__":
    archive = 'links.txt'
    imgDownloader = ImageDownloader(archive[0])
    imgDownloader.start()
