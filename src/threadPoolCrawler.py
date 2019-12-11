from threading import Thread
from job import Job
from state import State
import logging


class threadPoolCrawler:
    def __init__(self, maxThreads):
        self.state = State.WAITING
        self.contador = 0
        self.pool = set([]) 
        self.maxThreads = maxThreads
        self.currentQtdWorkers = 0
        self.thredsAtivas = set([])
        self.thread_safe = True
    
    def run(self):
        self.state = State.RUNNING
        while(self.state is not State.DONE):
            self.startNewJob()
            self.verifyThreadsState()
        

    def startNewJob(self):
        if(self.currentQtdWorkers < self.maxThreads):
            if self.pool:
                job = self.pool.pop()
                
                try:
                    th = Thread(target=job.function, args=(job.args,))
                    th.start()
                    
                    self.thredsAtivas.add(th)
                    self.currentQtdWorkers+=1 
    
    def submit(self, func, args):
        newExec = Job(func, args)
        self.pool.add(newExec)
        logging.info("Enviado")
        self.contador +=1
        
        
    def verifyThreadsState(self):
        toRemove = set([])
        for th in self.thredsAtivas:
            if not th.isAlive():
                toRemove.add(th)
        for td in toRemove:
            self.contador -=1
            self.thredsAtivas.remove(td)
            self.currentQtdWorkers-=1
        if(self.contador == 0 and not self.pool and not self.thredsAtivas):
            self.state = State.DONE
            