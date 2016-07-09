from config import PROJECT_URL
from apiclient.discovery import build


def main():
    apiRoot = PROJECT_URL + '/_ah/api'
    # apiRoot = 'http://localhost:8080' + '/_ah/api'
    api = 'notesapi'
    version = 'v1'
    discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (apiRoot, api, version)
    service = build(api, version, discoveryServiceUrl=discovery_url)
    response = service.mail().execute()
    print response

main()