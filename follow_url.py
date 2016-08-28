# purpose: follow url at the n-th position on
# linked webpages m times to get to the final name,
# like a scavenger hunt!

# user inputs: m, n, starting url; n > 0, m>= 0
# effect: print out final name

from beautiful_soup import *
import urllib

# prompt for url
url= raw_input('Enter url: ').strip()

# prompt for and check times
times_str = raw_input('Enter times: ')
try:
    times = int(times_str)
except:
    print 'bad times, start over'
    quit

# prompt for and check position
position_str = raw_input('Enter position:').strip()
try:
    position = int(position_str)
except:
    print 'bad position, start over'
    quit

    
# start looping    
while times > 0:
        
    # url: check if valid
    try:
        page_html = urllib.urlopen(url).read()
    except:
        print 'bad url, start over'
        quit

    # change to soup and get next url
    soup = BeautifulSoup(page_html)
    tags = soup('a')

    link = tags[position-1].get('href')
    
	# print name and extract url
    name = tags[position-1].contents[0]
    
	# update m, update url and iterate
    times-=1
    url = link
    
# print final name
print name