from time import time
import json

# Threading imports
from queue import Queue
from threading import Thread, Lock

# Custom Class import
from data import *
from crawlerWorker import CrawlerWorker

# Retrieve variable from data.py
global websiteIndex
global logger

def main():
    startingTime = time()
    print("Starting to crawl "+DOMAIN+" ...")

    # Create a queue to save job and a lock to guarantee a safe access to data between threads
    dataLock = Lock()
    linksQueue = Queue()

    logger.info('Starting to crawl ' + DOMAIN + ' with ' + str(THREADS_COUNT) + ' threads')

    # Create thread workers
    for x in range(THREADS_COUNT):
        worker = CrawlerWorker(linksQueue,x,dataLock, DOMAIN)
        # We allow main thread to exit program even though threads are blocking
        worker.daemon = True
        worker.start()
    linksQueue.put(DOMAIN)
    # Wait for queue to be empty
    linksQueue.join()

    logger.info('Done crawling ' + DOMAIN + ' - ' + str(len(websiteIndex))+" pages were parsed in "+str(time()-startingTime))

    print("Done! "+ str(len(websiteIndex))+" pages were parsed!")
    print(str(time()-startingTime)+" s. spent crawling.")

    fileName = 'results/'+re.sub('[^A-Za-z0-9]+', '', DOMAIN)+'_'+str(time())+'.txt'
    output_result(websiteIndex,fileName)

    print("Result available in file "+fileName)

def output_result(websiteIndex,fileName):
    """
       Simple function to output result of parsing in a unique txt file
    """
    file = open(fileName,'w')
    for page,result in websiteIndex.items():
        file.write(str(page)+"\n")
        file.write("\n|\n| Static assets:")
        for asset in result[1]:
            file.write("\n|-----"+asset)
        file.write("\n|\n| Links:")
        for link in result[0]:
            file.write("\n|-----"+link)
        file.write("\n\n")

if __name__== "__main__":
  main()
