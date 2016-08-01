import json
import urllib
import ssl
import sqlite3
import time

serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'

scontext = None

conn = sqlite3.connect('geodata.sqlite3')
cur = conn.cursor()

cur.execute('''
            CREATE TABLE IF NOT EXISTS Locations ( address TEXT, geodata TEXT )''')

fh = open('hiking.data')
count = 0
for line in fh:
    if count>200: break
    address = line.strip()
    print ''
    cur.execute('SELECT geodata FROM Locations WHERE address = ?',(buffer(address),))
    
    try:
        data = cur.fetchone()[0]
        print 'Found in Database'
        continue
    except:
        pass

    print "Resolving",address
    url = serviceurl + urllib.urlencode({"sensor":"false","address":address})
    print 'Retrieving url:',url
    uh = urllib.urlopen(url, context = scontext)
    data = uh.read()
    print 'Retrieved',len(data),'characters',data[:20].replace('\n',' ')
    count += 1
    try:
        js = json.loads(str(data))
    except:
        continue

    if 'status' not in js or js['status']!='OK':
        print "====== Failure to retrieve ======"
        print data
        continue
    
    cur.execute('''INSERT INTO Locations VALUES(?,?)''',(buffer(address),buffer(data)))
    conn.commit()
    time.sleep(1)
    
        





    
