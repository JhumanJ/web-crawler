from time import time

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

    # Create a queue to save job and a lock to guarantee a safe access to data between threads
    dataLock = Lock()
    linksQueue = Queue()

    logger.info('Starting to crawl ' + DOMAIN + ' with ' + str(THREADS_COUNT) + ' threads')

    # Create thread workers
    for x in range(THREADS_COUNT):
        worker = CrawlerWorker(linksQueue,x,dataLock, DOMAIN)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    linksQueue.put(DOMAIN)
    # Wait for queue to be empty
    linksQueue.join()

    logger.info('Done crawling ' + DOMAIN + ' - ' + str(len(websiteIndex))+" pages were parsed in "+str(time()-startingTime))

    print("Done! "+ str(len(websiteIndex))+" pages were parsed!")
    print(str(time()-startingTime))
    output_result(websiteIndex)

def output_result(websiteIndex):
    """
       Simple function to output result of parsing in the console
    """
    for page,result in websiteIndex.items():
        print("\n"+str(page.path))
        print("|\n| Static assets:")
        for asset in result[1]:
            print("|-----"+asset)
        print("|\n| Links:")
        for link in result[0]:
            print("|-----"+link)


if __name__== "__main__":
  main()
