import logging
import re
from time import time

"""
Data shared between files
"""

# Url to crawl
DOMAIN = "https://docs.python.org"

# Size of pool thread
THREADS_COUNT = 20

LOG_LEVEL = logging.DEBUG

# Set of link already visited
linksVisited = set()

# Dictionary with a path as a key, and a list of link and assets as value
websiteIndex = dict()

# Create a file logger that will stores actions in web_crawler
logger = logging.getLogger('web_crawler ')
logger.setLevel(LOG_LEVEL)
fh = logging.FileHandler('log/web_crawler_'+re.sub('[^A-Za-z0-9]+', '', DOMAIN)+'_'+str(time())+'.log')
fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(fh)
