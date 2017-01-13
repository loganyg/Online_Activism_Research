import json, time, os, sys
from selenium import webdriver
from lxml import html
from bs4 import BeautifulSoup
import makeQueries as mq

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
    driver.quit()
    parser = BeautifulSoup(response, "html.parser")
    for petition in parser.find_all("li", class_="petition"):
        url = petition["data-url"]
        petition_id = json.loads(mq.makerequest({'petition_url':url}, "/v1/petitions/get_id"))['petition_id']
        response_data = json.loads(mq.makerequest({'fields' : ','.join(mq.fields)}, "/v1/petitions/" + str(petition_id)))
        petition_created = time.strptime(response_data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        if petition_created > lastscrape:
            petition_info["petition_ids"].append(petition_id)
        else:
            foundend = True
    page += 1
petition_info["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", scrapetime)
with open("petitions.json", 'w') as out:
    json.dump(petition_info, out, indent=4)


print(time.time()-start)