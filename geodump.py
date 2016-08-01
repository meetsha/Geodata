import sqlite3
import json
import codecs

conn = sqlite3.connect('geodata.sqlite3')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
fhand = codecs.open('where.js','w',"utf-8")
fhand.write("myData = [\n")
count = 0
for row in cur:
    data = str(row[1])
    try:
        js = json.loads(data)
    except:
        continue
    
    if not('status' in js and js['status']=='OK'): continue

    lat = js['results'][0]['geometry']['location']['lat']
    lon = js['results'][0]['geometry']['location']['lng']
    
    where = js['results'][0]['formatted_address']
    where = where.replace("'"," ")

    try:
        print where,lat,lon
        count += 1
        if count > 1: fhand.write(",\n")
        output = "["+str(lat)+","+str(lon)+", '"+where+"']"
        fhand.write(output)
    except:
        continue        
    
fhand.write("\n];\n")
cur.close()
fhand.close()    
    
