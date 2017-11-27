# Web-Crawler
By Julien Nahum for a Monzo Interview

A python web crawler returning links and assets on each page of a website.
To be used with Python 3.6.3.

To use, in `data.py`, change the value of DOMAIN and then simply run `$ python crawler.py`

A log file will be created, and result will be output in a txt file in the "results" folder.

## Limitations

This web crawler is pretty basic and doesn't work on every website.
The very simple user agent used by the crawler is probably the reason why it doesn't work for some websites.

There is also an issue with SSL. Websites using https seems not work, but again that may be the case because of user agents.

## Testing

To run the tests, execute `$  python3 -m tests.name_of_the_test`
