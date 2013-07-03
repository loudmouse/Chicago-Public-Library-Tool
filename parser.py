"""Functions to renew books on the CPL website.
"""

import HTMLParser
import login
import urllib2

ROOT_URL = 'http://www.chipublib.org'
SUMMARY_URL = 'http://www.chipublib.org/mycpl/summary'

class RenewLinkParser(HTMLParser.HTMLParser, object):
    """Gather a list of links that renew books."""

    def __init__(self):
        super(self.__class__, self).__init__()
        self.renew_links = []

    def handle_starttag(self, tag, attrs):
        """Append each renewal link we find to renew_links."""
        if tag == 'a':
            for name, value in attrs:
                if name == 'href' and 'renew' in value:
                    self.renew_links.append(value)

def get_summary_page(opener):
    """Get the summary page for the account."""
    request = urllib2.Request(SUMMARY_URL, None, login.HEADERS)
    response = opener.open(request)
    return response.read()

def get_renew_links(page):
    """Get the book renewal links."""
    parser = RenewLinkParser()
    parser.feed(page)
    return parser.renew_links

def renew_books():
    """Open each book renewal link."""
    opener = login.login()
    page = get_summary_page(opener)
    renew_links = get_renew_links(page)
    if renew_links:
        for renew_link in renew_links:
            item_number = renew_link.split('/')[-2]
            print('renewing item %s' % item_number)
            renew_link = ROOT_URL + renew_link
            request = urllib2.Request(renew_link, None, login.HEADERS)
            opener.open(request)
    else:
        print('nothing to renew')
