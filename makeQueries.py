import httplib, urllib, base64, json, sys, os, time

# Load various values from a config file so values are not
# hard coded into this script.
config = json.load(open("config.json"))
api_key = config["api_key"]
PAGE_SIZE = config["PAGE_SIZE"]
petition_fields = config["petition_fields"]
user_fields = config["user_fields"]
#request_url = '/v1/petitions/get_id'

# Makes a request using the first param as the parameters other than
# the API key in the form of a dictionary.
# The second parameter is the endpoint that the request is made to.
def makerequest(additional_params, request_url):
    base_url = config["base_url"]
    headers = {
        # Request headers
    }
    parameters = additional_params
    parameters['api_key'] = api_key
    params = urllib.urlencode(parameters)

    conn = httplib.HTTPSConnection(base_url)
    conn.request("GET", request_url + "?" + params)
    #conn.request("GET", "/v1/petitions/get_id?%s" % params)
    response = conn.getresponse()
    return response.read()

# Specific to query for the information of a user based on their
# user url. This is used since unlike other change URLs user IDs
# are contained within the actual URL.
def scrapeuser(url):
    spliturl = url.split("/")
    ID = spliturl[len(spliturl)-1]
    response_data = makerequest({}, "/v1/users/" + str(ID))
    body = json.loads(response_data)
    body['user_id'] = ID
    body['user_url'] = url
    return body

# A more general form to scrape information from the change.org API based on a change.org URL.
# Requires that you also specify the endpoint to query for whatever url type inputted.
# For users it is preferred to use scrapeuser because the structure of the user URL allows the
# get_id step to be omitted.
def scrapeurl(url, epname):
    url_key = epname + '_url'
    response_data = makerequest({url_key:url}, "/v1/%ss/get_id" % epname)
    ID = json.loads(response_data)[epname + '_id']
    response_data = makerequest({'fields' : ','.join(config[epname + "_fields"])}, "/v1/%ss/%s" % (epname, str(ID)))
    body = json.loads(response_data)
    body[epname + '_id'] = ID
    body[epname + '_url'] = url
    body['scraped_at'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return body

# DEPRECATED -- Used to scrape a URL and put the results into a text file in JSON form.
# Additionally, has an option to include both updates and reasons, only obtaining the first page of each.
# As we are now using a database to store the information, the text dump format is no longer useful.
# Additionally, neither reasons nor updates are scraped until the end of the project, so this is
# even further unnecessary.
# One should use the more versatile scrapeurl() to scrape petition data.
def scrapepetition(url, out, updates=False, reasons=False):
    petition_id = json.loads(makerequest({'petition_url':url}, "/v1/petitions/get_id"))['petition_id']
    response_data = makerequest({'fields' : ','.join(petition_fields)}, "/v1/petitions/" + str(petition_id))
    json.dump(json.loads(response_data), out, sort_keys=True, indent=4)
    out.write('\n')
    if updates:
        response_data = makerequest({'page_size' : PAGE_SIZE}, "/v1/petitions/%s/updates" % str(petition_id))
        json.dump(json.loads(response_data), out, indent=4)
        out.write('\n')
    if reasons:
        response_data = makerequest({'page_size' : PAGE_SIZE}, "/v1/petitions/%s/reasons" % str(petition_id))
        json.dump(json.loads(response_data), out, indent=4)
        out.write('\n')

#print makerequest(additional_parameters, "/v1/petitions/get_id")
#petition_id()
#response_data = json.load(makerequest(additional_parameters, "/v1/petitions/" + petition_id))
#for item in response_data:
#    print item
#    print response_data[item]# 