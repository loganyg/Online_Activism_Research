import json, time
import mySQLQuerier as msq

petition_info = json.load(open("petitions.json"))
petition_ids = petitions_info["petition_ids"]
scrapetime = time.gmtime()

formattedt = time.strftime("%Y-%m-%dT%H:%M:%SZ", scrapetime)

# Add database column for this scrape
msq.add_column(formattedt, "signatures", "INT UNSIGNED")
for ID in petition_ids:
    # Get current number of signatures
    response = makerequest({'fields' : 'signature_count')}, "/v1/petitions/%s" % str(ID))
    body = json.loads(response)
    # Input number into database
    msq.update('signatures', formattedt, body['signature_count'], 'petition_id', ID)