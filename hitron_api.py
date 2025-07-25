import requests
import json
from urllib.parse import urlunparse
import logging

SCHEME = "http"
PATH_LOGIN = "/1/Device/Users/Login"
PATH_SYSINFO = "/1/Device/Router/SysInfo"
PATH_VERSION = "/1/Device/CM/Version"
PATH_REBOOT = "/1/Device/CM/Reboot"
PATH_CSRF = "/1/Device/Users/CSRF"

logger = logging.getLogger(__name__)

class HitronClient:
    """
    Client for interacting with a Hitron router's API.
    All methods return parsed JSON (dict) or None on error, unless otherwise noted.
    """
    def __init__(self, session=None, scheme=SCHEME, host="192.168.0.1", username="cusadmin", password="uni.2311"):
        self.sess = session or requests.Session()
        self.scheme = scheme
        self.netloc = host  # Map host to netloc for internal use
        self.username = username
        self.password = password
        self.csrf = None

    def _request(self, method, path, **kwargs):
        url = urlunparse((self.scheme, self.netloc, path, '', '', ''))
        try:
            resp = self.sess.request(method, url, timeout=10, **kwargs)
            resp.raise_for_status()
            return resp
        except (requests.RequestException, ValueError):
            return None

    def get_version(self):
        """Return router version info as dict, or None on error."""
        resp = self._request('GET', PATH_VERSION)
        return resp.json() if resp else None

    def post_login(self):
        """Login to the router. Returns result dict or None on error."""
        data = {"model": f'{{"username":"{self.username}","password":"{self.password}"}}'}
        resp = self._request('POST', PATH_LOGIN, data=data)
        return resp.json() if resp else None

    def get_sysinfo(self):
        """Return system info as dict, or None on error. Logs request and response for debugging."""
        url = urlunparse((self.scheme, self.netloc, PATH_SYSINFO, '', '', ''))
        logger.debug(f"Requesting sysinfo from URL: {url}")
        resp = self._request('GET', PATH_SYSINFO)
        if resp:
            logger.debug(f"Sysinfo response text: {resp.text}")
            try:
                return resp.json()
            except Exception as e:
                logger.error(f"JSON decode error: {e}")
                return None
        else:
            logger.error("No response received for sysinfo request.")
        return None

    def get_csrf(self):
        """Fetch and store CSRF token. Returns token string or None."""
        resp = self._request('GET', PATH_CSRF)
        if resp:
            try:
                self.csrf = resp.json().get("CSRF")
            except (json.JSONDecodeError, KeyError, AttributeError):
                self.csrf = None
        else:
            self.csrf = None
        return self.csrf

    def post_reboot(self, csrf=None):
        """Reboot the router. Returns result dict or None on error. Ensures login first."""
        login_result = self.post_login()
        if not login_result or login_result.get("result") != "success":
            logger.error(f"Reboot failed: Unable to log in to Hitron modem: {login_result}")
            return None
        if csrf is None:
            csrf = self.csrf or self.get_csrf()
        if not csrf:
            logger.error("Reboot failed: No CSRF token available.")
            return None
        data = {"csrf": csrf, "model": r'{"reboot":"1"}'}
        resp = self._request('POST', PATH_REBOOT, data=data)
        return resp.json() if resp else None

    def reboot(self):
        """Alias for post_reboot, for compatibility with button entity."""
        return self.post_reboot()

    def get_status(self):
        """
        Return a summary status dict from the router's sysinfo.
        Example fields: uptime, connected, wanIP, etc.
        Returns None on error.
        """
        sysinfo = self.get_sysinfo()
        if not sysinfo:
            return None
        return {
            "uptime": sysinfo.get("systemLanUptime"),
            "connected": bool(sysinfo.get("wanIP")),
            "wanIP": sysinfo.get("wanIP"),
            "lanIP": sysinfo.get("privLanIP"),
            "model": sysinfo.get("modelName"),
            "software_version": sysinfo.get("SoftwareVersion"),
            # Add more fields as needed
        }