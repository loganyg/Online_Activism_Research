import json, time, os, sys
from selenium import webdriver
from lxml import html
from bs4 import BeautifulSoup
import makeQueries as mq
import mySQLQuerier as msq

#time.strptime("2015-07-12T16:44:24Z", "%Y-%m-%dT%H:%M:%SZ")
petition_info = json.load(open("petitions.json"))
lastscrape = time.strptime(petition_info["last_updated"], "%Y-%m-%dT%H:%M:%SZ")

scrapetime = time.gmtime()
start = time.time()
page = 1
foundend = False
while foundend is False:
    driver = webdriver.Firefox()
    driver.get("https://www.change.org/petitions#most-recent/%s" % page)
    time.sleep(5)
    response = driver.page_source
    parser = BeautifulSoup(response, "html.parser")
    for petition in parser.find_all("li", class_="petition"):
        url = petition["data-url"]
        #petition_id = json.loads(mq.makerequest({'petition_url':url}, "/v1/petitions/get_id"))['petition_id']
        #response_data = json.loads(mq.makerequest({'fields' : ','.join(mq.petition_fields)}, "/v1/petitions/" + str(petition_id)))
        petition_body = mq.scrapeurl(url, 'petition')
        petition_id = petition_body['petition_id']
        print petition_body.keys()
        petition_created = time.strptime(petition_body['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        if petition_created > lastscrape:
            # ---+--- This is up in the air in terms of where to make the mySQL queries. Doing them with the scraping ---+----
            # ---+--- of the petitions makes the program the most streamlined, but could increase the amount of time  ---+----
            # ---+--- between the scraping of each petitionself.                                                      ---+----
            # ---+--- Storing the petition data and then scraping all the necessary data before adding anything to the---+----
            # ---+--- database would minimize the time between the scraping of petition data but would be less space  ---+----
            # ---+--- efficientself.                                                                                  ---+----
            try:
                petition_info["petition_ids"].append(petition_id)
                # Add petition to the database.
                msq.add_petition(petition_body)
                # Add targets and the link between targets and petition to the database.
                for target in petition_body['targets']:
                    msq.add_target(target)
                    target_id = msq.cursor.lastrowid
                    msq.insert({'petition_id': petition_id, 'target_id': target_id}, 
                            'petition_targets', ['petition_id', 'target_id'])
                # Add user as well as link between petition and use to the database.
                user_body = mq.scrapeuser(petition_body['creator_url'])
                msq.add_user(user_body)
                msq.insert({'petition_id': petition_id, 'user_id': user_body['user_id']}, 
                            'petition_users', ['petition_id', 'user_id'])
            except:
                with open('error.json', 'a') as out:
                    json.dump(petition_body, out, indent=4)
                raise
        else:
            foundend = True
    page += 1
driver.quit()
msq.close()
petition_info["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", scrapetime)
with open("petitions.json", 'w') as out:
    json.dump(petition_info, out, indent=4)


print(time.time()-start)