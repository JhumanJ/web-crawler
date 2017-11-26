from html.parser import HTMLParser
from urllib.parse import urlparse

class Parser(HTMLParser):
    """
        Define an HTML Parser that only saves link on a specified domain

        Attributes:
            staticAssets (set): Set of assets on the currently parsed page
            links (int): Set of links (same domaine name as specified) on the currently parsed page
            url (ParseResult): domain of interest
    """

    def __init__(self,url):
        """
            Init the default htmlParser and add custom properties

            Args:
                url (string): the domain of interest
        """

        # Call parent constructor (HTMLParser)
        HTMLParser.__init__(self)

        # Create empty sets to store assets and links
        self.staticAssets = set()
        self.links = set()

        # We also save the url, so that Parser only parse link belonging to the same domain
        self.url = urlparse(url)

    def handle_starttag(self, tag, attrs):
        """
            Parsing behaviour here by overriding the HTMLParser method
        """

        # First we collect all links on the same domain
        if tag == 'a':
            # If the link points to another page on the same domain we save it
            for (key,value) in attrs:
                if key =='href' and self.linkOnSameDomain(value):
                    self.links.add( urlparse(value).path )

        # Then we start collecting assets (both scrips and links)
        if tag == 'link' or tag == 'script':
            # If the link points to another page on the same domain we save it
            for (key,value) in attrs:
                if (key =='href' or key =='src') and self.linkOnSameDomain(value):
                    self.staticAssets.add( urlparse(value).path )


    def linkOnSameDomain(self,value):
        """
            Return true if the link isn't an external link (ie: same domain)
        """
        if (urlparse(value).netloc == self.url.netloc or urlparse(value).netloc == ''):
            return True
        return False
