from threading import Thread, Lock
from urllib.parse import urlparse
import urllib.request

from parser import Parser
from data import linksVisited,websiteIndex,logger

class CrawlerWorker(Thread):
   """
      Thread worker Class
      Query and parse url from a given queue
   """

   def __init__(self, queue, id, dataLock, domain):
       """
          Creates the thread

          Args:
              queue (queue): the queue containing the list of url to Query
              id (int): id of the thread (for debugging and logging)
              dataLock (Lock): lock shared by al threads to insure safe access to global var linksVisited and websiteIndex
              domain (string): domain of interest (so that we don't follow external links)
       """
       Thread.__init__(self)
       self.queue = queue
       self.domain = domain
       self.dataLock = dataLock
       self.id = id

   def run(self):
       """
          Take jobs in the queue (url to query), parse it and save results
       """
       global linksVisited
       global websiteIndex
       global logger

       dataLock = self.dataLock

       while True:

           # Get the job(link) from the queue and parse link
           queueItem = self.queue.get()
           currentLink = urlparse(queueItem)

           # Make sure link wasn't already visited and add it to the list of visited links
           with dataLock:
               if currentLink.path in linksVisited:
                   self.queue.task_done()
                   continue
               linksVisited.add(currentLink.path)

           logger.info("Thread with id " + str(self.id) + " starts crawling " + currentLink.path)

           # Query page - Add some headers so that websites such as Monzo.com aren't afraid and answer ;)
           try:
                req = urllib.request.Request(urllib.parse.urljoin(self.domain, currentLink.path), headers={'User-Agent': 'Mozilla/5.0'})
                webPage = urllib.request.urlopen( req )
           except urllib.error.HTTPError as e:
                # Whoops it wasn't a 200
                logger.error("Error - Thread with id " + str(self.id) + " while crawling " + urllib.parse.urljoin(self.domain, currentLink.path) + ": " + str(e))
                self.queue.task_done()
                continue

           # Create instance of HTML parser
           try:
               htmlParser = Parser(self.domain)
               htmlParser.feed(str(webPage.read()))
               htmlParser.close()
           except UnboundLocalError:
                logger.error("Error - Thread with id " + str(self.id) + " while parsing " + urllib.parse.urljoin(self.domain, currentLink.path))
                self.queue.task_done()
                continue

           # Find remaining links to visit (again syncrhonised so that link aren't handled twice)
           with self.dataLock:
               # Save links and assets as a tuple
               websiteIndex[currentLink.path] = (htmlParser.links,htmlParser.staticAssets)
               linksNotVisitedYet = htmlParser.links.difference(linksVisited)

           # Add links to visit
           for link in linksNotVisitedYet:
               self.queue.put(link)

           self.queue.task_done()
