import requests, urllib

DISCOVERY_EP = 'https://api.us.socrata.com/api/catalog/v1'
DEFAULT_DOMAIN = 'data.act.gov.au'
APP_TOKEN = 'dvYaQOtps4HPZUfxFrC7B4tu2'
ASSET_TYPES = ['datasets', 'charts', 'maps', 'datalenses', 'stories', 'files', 'hrefs']
MIME_TYPE_CSV = 'text/csv'
MIME_TYPE_JSON = 'application/json'
MIME_TYPE_GEOJSON = 'application/vnd.geo+json'

def connect(url, payload, headers, return_type=MIME_TYPE_JSON):
    r = requests.get(url, headers=headers)
    print('attempting connection to {}...'.format(url))
    print('response was [{} {}]'.format(r.status_code, r.reason))
    if 'Accept' in headers.keys():
        if headers['Accept'] == MIME_TYPE_CSV:
            return r.text
        elif headers['Accept'] == MIME_TYPE_JSON or headers['Content-Type'] == MIME_TYPE_GEOJSON:
            return r.json()
    return r

def discover(context=DEFAULT_DOMAIN, categories=[], tags=[], text=None, asset_type=None):
    '''
    Search for open datasets by context (defaults to the ACT open data domain), 
    categories, tags, text and asset type. All search fields are optional, and if 
    none are given, then all possible results will be returned.
    
    The result will be stored in a dictionary of the form:
    {
        results: [
            {
                resource {
                    name
                    id
                    description
                    attribution
                    type
                    updatedAt
                    createdAt
                    page_views
                    columns_name
                    columns_field_name
                    columns_description
                    parent_fxf (optional)
                    provenance (optional)
                    download_count
                }
                classification {
                    categories
                    tags
                    domain_category
                    domain_tags
                    domain_metadata
                }
                metadata
                permalink
                link
                owner (optional)
                preview_image_url (optional)             
            }
        ]
        resultSetSize
        timings
    }
    '''
    url = '{}?search_context={}'.format(DISCOVERY_EP, DEFAULT_DOMAIN, context)
    for category in categories:
        url = url + '&categories={}'.format(urllib.request.quote(category))
    for tag in tags:
        url = url + '&tags={}'.format(urllib.request.quote(tag))
    if text != None:
        url = url + '&q={}&min_should_match={}'.format(urllib.request.quote(text), urllib.request.quote('3<60%'))
    if asset_type != None:
        url = url + '&only={}'.format(urllib.request.quote(asset_type))
    if len(categories) == 0 and len(tags) == 0 and asset_type == None:
        url = url + '&domains={}'.format(DEFAULT_DOMAIN)
    headers = {'Content-Type': MIME_TYPE_JSON, 'Accept': MIME_TYPE_JSON, 'X-Socrata-Host': DEFAULT_DOMAIN}
    result = connect(url, None, headers)
    return result

def retrieve(endpoint, limit=10):
    '''
    '''
    url = '{}?$limit={}'.format(endpoint, limit)
    headers = {'Content-Type': MIME_TYPE_JSON, 'Accept': MIME_TYPE_CSV, 'Host': DEFAULT_DOMAIN, 'X-App-Token': APP_TOKEN}
    result = connect(url, None, headers)
    return result

if __name__ == '__main__':
    # example usage - discover datasets about speeding and take the first result
    d = discover(tags=['speed camera'])
    results = d['results']
    print('number of results:', len(results))
    for result in results:
        link = result['permalink']
        resource = result['resource']
        print('{} [{}]\n\t{}\n'.format(resource['name'], link, resource['description']))
        break

    # get the data - there doesn't appear to be a way to get the resource id 
    # via the api, so we have to browse to the discovered link to find it
    resourceId = 'h534-v2x9'
    data = retrieve(link.replace('/d', '/resource')[:-9] + resourceId)
    print(data)
    
