from django.core.management import setup_environ
import pmap.settings
setup_environ(pmap.settings)
from pmap.models import ItemLocation


#item_code = '2202'
#2128
#item_code = '2128'
#item_code = '190203000'
import csv

addrs = {}
postcodes = {}

s = csv.reader(open('../T201208ADDR BNFT.CSV'))
for row in s:
    addrs[row[1]] = row[7].strip()
del s
s = csv.reader(open('../postcodes.csv'))
for row in s:
    postcodes[row[0].strip()] = row[1], row[2]
del s

s = csv.reader(open('..//T201208PDP IEXT.CSV'))
header = s.next()
items = {}
ItemLocation.objects.all().delete()
q = []
for i, row in enumerate(s):
    if True:#row[3].strip() == item_code:
        pc = addrs[row[2]]
        try:
            lat,lon = postcodes[pc]
        except KeyError:
            continue
        #print ','.join([ row[3].strip(), row[4].strip(), pc, lat, lon, str(int(row[5])), str(float(row[6])), str(float(row[7])) ])
        il = ItemLocation()
        il.item_id = row[3].strip()
        il.item_name = row[4].strip()
        il.lat = lat
        il.lon = lon
        il.quantity = int(row[5])
        q.append(il)
    if i  % 1000 == 0:
        print i
        ItemLocation.objects.bulk_create(q)
        q = []
