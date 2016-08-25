# This application will read the mailbox data (mbox.txt)
# count up the number of email messages per organization
# (i.e. domain name of the email address) using a database
# with the following schema to maintain the counts.
# CREATE TABLE Counts (org TEXT, count INTEGER)


import sqlite3

# create table
connection = sqlite3.connect('emails.sqlite')
cur = connection.cursor()

cur.execute('''DROP TABLE IF EXISTS Counts''')
cur.execute('''CREATE TABLE Counts (org TEXT, count INTEGER)''')
cur.execute('''DELETE FROM Counts;''')

# open file
fname_w_space = raw_input('enter file name: ')
fname = fname_w_space.strip()

try:
    fhandler = open(fname)
except:
    print 'bad input, please relaunch program'
    quit

# extract org name and count
for line in fhandler:
    line = line.strip()
    if line.startswith('From: '):
	
        low = line.split()
        email = low[1]
        email_org_w_space = email.split('@')[1]
        email_org = email_org_w_space.strip()
		
    
        #email_org = line.split("@")[1].replace('\n','')
        cur.execute('SELECT count FROM Counts WHERE org = ?', (email_org, ))
        try:
            email_count = cur.fetchone()[0]
            cur.execute('UPDATE Counts SET count = count+1 WHERE org = ?', (email_org, ))
        except:
            cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1)', (email_org, ))
        
connection.commit()        

    
# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

print "Counts:"
for row in cur.execute(sqlstr) :
    print str(row[0]), row[1]

cur.close()
