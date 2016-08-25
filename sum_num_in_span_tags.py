# purpose:    find all the numbers in span tags
#             in given url and print their sums

from beautiful_soup import *
import urllib

# get url from user
url = raw_input('Enter url: ').strip()

# open page
page_html = urllib.urlopen(url).read()


# get span tags
soup = BeautifulSoup(page_html)
tags = soup('span')

sum = 0
for tag in tags:
    # parse out numbers
    num = int(tag.contents[0])
    # sum it up as it goes
    sum += num

print sum

