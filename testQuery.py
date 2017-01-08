import httplib, urllib, base64, json, sys, os

api_key = 'c8771f32ce9ff32fe469d90327e9d5ee86832021f9491e2afc1dd3c7688ce60c'
PAGE_SIZE = 500
#request_url = '/v1/petitions/get_id'

# Makes a request using the first param as the parameters other than
# the API key in the form of a dictionary.
# The second parameter is the endpoint that the request is made to.
def makerequest(additional_params, request_url):
    base_url = 'api.change.org'
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
    response_data = makerequest(additional_parameters, "/v1/petitions/" + str(petition_id))
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

fields = ['title','signature_count','goal','creator_name','organization_name','targets','overview','creator_url'
]
additional_parameters = {
    #'petition_url' : petition_url
    #'petition_id' : petition_id,
    'fields' : ','.join(fields)
}
with open('out.txt', 'w') as out:
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

#print makerequest(additional_parameters, "/v1/petitions/get_id")
#petition_id()
#response_data = json.load(makerequest(additional_parameters, "/v1/petitions/" + petition_id))
#for item in response_data:
#    print item
#    print response_data[item]# 