import json, time
import mySQLQuerier as msq

petition_info = json.load(open("petitions.json"))
petition_ids = petitions_info["petition_ids"]
scrapetime = time.gmtime()

# Add database column for this scrape
msq.add_column(time.strftime("%Y-%m-%dT%H:%M:%SZ", scrapetime), "signatures", "INT UNSIGNED")
for ID in petition_ids:
    # Get current number of likes
    # Input number into database