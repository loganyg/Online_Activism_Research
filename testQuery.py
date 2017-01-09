import json, time, os, sys
from makeQueries import *

start = time.time();
with open('out.json', 'w') as out:
    updates = False
    reasons = False
    if '-u' in sys.argv[2:]:
        updates = True
    if '-r' in sys.argv[2:]:
        reasons = True
    if os.path.isfile(sys.argv[1]):
        urls = open(sys.argv[1], 'r')
        for url in urls:
            scrapeurl(url, out, updates=updates, reasons=reasons)
    else: 
        scrapeurl(sys.argv[1], out, updates=updates, reasons=reasons)
print(time.time() - start)