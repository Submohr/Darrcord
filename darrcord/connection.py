class Connection(object):
    ENDPOINT: str
    API_KEY: str
    HEADERS: dict

    def __init__(self, ENDPOINT, API_KEY):
        self.ENDPOINT = ENDPOINT
        self.API_KEY = API_KEY
        self.HEADERS = {'X-Api-Key': self.API_KEY,
                        'Content-Type': "application/json"}
