import json, time
import mySQLQuerier as msq
import makeQueries as mq

petitions_info = json.load(open("petitions.json"))
petition_ids = petitions_info["petition_ids"]
scrapetime = time.gmtime()

formattedt = time.strftime("%Y-%m-%dT%H:%M:%SZ", scrapetime)

# Add database column for this scrape
msq.add_column("`" + formattedt + "`", "signatures", "INT UNSIGNED")
for ID in petition_ids:
    try:
        # Get current number of signatures
        response = mq.makerequest({'fields' : 'signature_count'}, "/v1/petitions/%s" % str(ID))
        body = json.loads(response)
        # Input number into database
        if "messages" in body.keys() and "petition not found" in body['messages']:
            petitions_info["petition_ids"].remove(ID)
            print "Petition ID #" + str(ID) + " appears to be deleted, it has been removed from the petitions list."
        else:
            msq.update('signatures', '`' + formattedt + '`', str(body['signature_count']), 'petition_id', str(ID))
    except Exception as e:
        print ID
        print str(e)

with open("petitions.json", 'w') as out:
    json.dump(petitions_info, out, indent=4)