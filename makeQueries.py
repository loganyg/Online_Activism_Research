import httplib, urllib, base64, json, sys, os, time

config = json.load(open("config.json"))
api_key = config["api_key"]
PAGE_SIZE = config["PAGE_SIZE"]
fields = config["fields"]
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

def scrapeurl(url, out, updates=False, reasons=False):
    petition_id = json.loads(makerequest({'petition_url':url}, "/v1/petitions/get_id"))['petition_id']
    response_data = makerequest({'fields' : ','.join(fields)}, "/v1/petitions/" + str(petition_id))
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