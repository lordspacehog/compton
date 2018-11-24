import json
from vyper import v
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient

PARTICLE_API_BASE = 'https://api.particle.io'
PARTICLE_API_VERSION = 'v1'
PARTICLE_TOKEN_ENDPOINT = '/'.join([PARTICLE_API_BASE, 'oauth/token'])


def build_api_path(endpoint):
    if isinstance(endpoint, list):
        return '/'.join([PARTICLE_API_BASE, PARTICLE_API_VERSION, *endpoint])
    return '/'.join([PARTICLE_API_BASE, PARTICLE_API_VERSION, endpoint])


def dechunk(content):
    event = {}
    while 1:
        line = next(content)
        if line:
            if event.get('event'):
                if line.startswith(b'data'):
                    event['data'] = json.loads(line.lstrip(b'data: '))
                    yield event
                    event = {}
                    continue

            if line.startswith(b'event'):
                event["event"] = line.lstrip(b'event: ')


def init_config():
    v.set_config_name('compton')
    v.add_config_path('/etc/compton')
    v.add_config_path('$HOME/.compton')
    v.add_config_path('.')


def read_config():
    v.read_in_config()


def init_server():
    auth = HTTPBasicAuth(
        v.get('oauth_client.id'),
        v.get('oauth_client.secret')
    )
    client = BackendApplicationClient(client_id=v.get('oauth_client.id'))
    api_session = OAuth2Session(client=client)
    token = api_session.fetch_token(
        token_url=PARTICLE_TOKEN_ENDPOINT,
        auth=auth,
    )
    return token, api_session


def subscribe_to_events(session):
    resp = session.request(
        method="GET",
        url=build_api_path([
            'products',
            v.get('product.id'),
            'events'
        ]),
        stream=True
    )

    return dechunk(resp.iter_lines())


def run_server():
    init_config()
    read_config()
    token, session = init_server()

    events = subscribe_to_events(session)

    for event in events:
        print(event)
