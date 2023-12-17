import requests
import json

class Client():
    """Creates a client for ProxyOT to access the values of your points and lists."""

    def __init__(self, username, password):
        self.server = 'http://localhost:1990/'
        r = requests.get(f'{self.server}login')
        r = requests.post(f'{self.server}login', cookies=r.cookies, data={
                          'csrf_token': r.text, 'username': username, 'password': password})
        if r.status_code != 200:
            self.auth = False
        else:
            self.cookies = r.cookies
            self.auth = True

    def get_point(self, path):
        """Return the current value of a point."""
        if not self.auth:
            raise Exception('Invalid credentials')
        p = requests.get(
            f'{self.server}/get_point?path={path}', cookies=self.cookies)
        j = json.loads(p.text)
        if j['error']:
            raise Exception(j['error'])
        else:
            return j['value']

    def get_list(self, list_name):
        """Returns a list of strings that represent the values of the points in the list."""
        if not self.auth:
            raise Exception('Invalid credentials')
        r = requests.get(
            f'{self.server}/get_list?name={list_name}', cookies=self.cookies)
        j = json.loads(r.text)
        if j['error']:
            raise Exception(j['error'])
        else:
            return j['points']
