import logging
import requests
import json
from urllib.parse import urlunparse
from getpass import getpass
from argparse import ArgumentParser

parser = ArgumentParser("Hitron router API, API version 1.11, Software Version 7.1.1.32")
parser.add_argument("-u", "--username", type=str, default="cusadmin")
parser.add_argument("-p", "--password", type=str, default="uni.2311")
parser.add_argument("-i", "--ip", type=str, default="192.168.0.1")
parser.add_argument("--sysinfo", action="store_true", default=True)
parser.add_argument("--reboot", action="store_true", default=False)
parser.add_argument("-v", "--verbose", action="store_true", default=True)
args = parser.parse_args()

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING)

NETLOC = args.ip
SCHEME = "http"
USERNAME = args.username
password = args.password

PATH_LOGIN = "/1/Device/Users/Login"
PATH_SYSINFO = "/1/Device/Router/SysInfo"
PATH_VERSION = "/1/Device/CM/Version"
PATH_REBOOT = "/1/Device/CM/Reboot"
PATH_CSRF = "/1/Device/Users/CSRF"

class HitronApi:
    def __init__(self, session, scheme=SCHEME, netloc=NETLOC, username=USERNAME, password=None):
        self.sess = session
        self.scheme = scheme
        self.netloc = netloc
        self.username = username
        self.password = password
        self.csrf = None

    def get(self, path):
        return sess.get(urlunparse((self.scheme, self.netloc, path, '', '', '')))

    def get_version(self):
        return self.get(PATH_VERSION)

    def post_login(self):
        return sess.post(urlunparse((self.scheme, self.netloc, PATH_LOGIN, '', '', '')), data={
            "model": f'{{"username":"{self.username}","password":"{self.password}"}}'
        })

    def get_sysinfo(self):
        return self.get(PATH_SYSINFO)

    def get_csrf(self):
        r = self.get(PATH_CSRF)
        try:
            self.csrf = r.json()["CSRF"]
        except (json.JSONDecodeError, KeyError) as e:
            self.csrf = None
        return r

    def post_reboot(self, csrf=None):
        if csrf is None:
            csrf = self.csrf
        return sess.post(urlunparse((SCHEME, NETLOC, PATH_REBOOT, '', '', '')), data={
            "csrf": self.csrf,
            "model": r'{"reboot":"1"}'
        })

with requests.Session() as sess:
    api = HitronApi(sess, password=password)

    if args.sysinfo:
        r = api.get_version()
        _logger.info("%s", r.json())

    r = api.post_login()
    if r.json()['result'].title().startswith('Error'):
        _logger.error("%s", r.json())
    else:
        _logger.debug("%s", r.json())

    r = api.get_csrf()
    _logger.debug("%s", r.json())

    if args.sysinfo:
        r = api.get_sysinfo()
        _logger.info("%s", r.json())
        print(r.json())

    if args.reboot:
        r = api.post_reboot()
        _logger.info("%s", r.json())
        print(r.json())