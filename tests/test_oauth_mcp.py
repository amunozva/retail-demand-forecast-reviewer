"""OAuth boundary checks: local synthetic RSA keys, never production credentials."""
import json
import os
import threading
import unittest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from urllib import error, request

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from forecast_tool import mcp_server, oauth_auth

ISSUER = 'https://dev-b8nt1qlq3zd4hjh5.us.auth0.com/'
RESOURCE = 'https://retail-demand-forecast-reviewer.onrender.com/mcp'


class OAuthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = (oauth_auth.DOMAIN, oauth_auth.RESOURCE, oauth_auth.SCOPE,
                   oauth_auth.ISSUER, oauth_auth._client, os.getenv('MCP_AUTH_MODE'))
        cls.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        oauth_auth.DOMAIN = 'dev-b8nt1qlq3zd4hjh5.us.auth0.com'
        oauth_auth.ISSUER = ISSUER
        oauth_auth.RESOURCE = RESOURCE
        oauth_auth.SCOPE = 'forecast:read'
        oauth_auth._client = SimpleNamespace(get_signing_key_from_jwt=lambda _token:
                                              SimpleNamespace(key=cls.private_key.public_key()))
        os.environ['MCP_AUTH_MODE'] = 'oauth'
        cls.server = mcp_server.ThreadingHTTPServer(('127.0.0.1', 0), mcp_server.Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        (oauth_auth.DOMAIN, oauth_auth.RESOURCE, oauth_auth.SCOPE,
         oauth_auth.ISSUER, oauth_auth._client, old_mode) = cls.old
        if old_mode is None:
            os.environ.pop('MCP_AUTH_MODE', None)
        else:
            os.environ['MCP_AUTH_MODE'] = old_mode

    def token(self, issuer=ISSUER, audience=RESOURCE, scope='forecast:read', expiry=None):
        now = datetime.now(timezone.utc)
        return jwt.encode({'iss': issuer, 'aud': audience, 'scope': scope, 'iat': now,
                           'exp': expiry or now + timedelta(minutes=10), 'sub': 'test'},
                          self.private_key, algorithm='RS256', headers={'kid': 'test'})

    def call(self, method='POST', path='/mcp', token=None):
        headers = {'Content-Type': 'application/json'}
        if token is not None:
            headers['Authorization'] = 'Bearer ' + token
        data = None if method == 'GET' else json.dumps({
            'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list', 'params': {}
        }).encode()
        req = request.Request('http://127.0.0.1:%d%s' % (self.server.server_port, path),
                              data=data, headers=headers, method=method)
        try:
            resp = request.urlopen(req, timeout=5)
        except error.HTTPError as exc:
            resp = exc
        with resp:
            return resp.status, dict(resp.headers), json.loads(resp.read() or b'{}')

    def test_protected_resource_metadata(self):
        for path in ('/.well-known/oauth-protected-resource',
                     '/.well-known/oauth-protected-resource/mcp'):
            code, _, body = self.call('GET', path)
            self.assertEqual(code, 200)
            self.assertEqual(body['resource'], RESOURCE)
            self.assertEqual(body['authorization_servers'], [ISSUER])

    def test_challenge_includes_metadata(self):
        code, headers, _ = self.call()
        self.assertEqual(code, 401)
        self.assertIn('resource_metadata="https://retail-demand-forecast-reviewer.onrender.com/.well-known/oauth-protected-resource/mcp"',
                      headers['WWW-Authenticate'])

    def test_valid_token_exposes_forecast_tool(self):
        code, _, body = self.call(token=self.token())
        self.assertEqual(code, 200)
        self.assertEqual(body['result']['tools'][0]['name'], 'analyze_orange_juice_demand')

    def test_wrong_issuer_rejected(self):
        self.assertEqual(self.call(token=self.token(issuer='https://another.auth0.com/'))[0], 401)

    def test_wrong_audience_rejected(self):
        self.assertEqual(self.call(token=self.token(audience='https://other.example/mcp'))[0], 401)

    def test_missing_scope_rejected(self):
        self.assertEqual(self.call(token=self.token(scope='openid profile'))[0], 401)

    def test_expired_token_rejected(self):
        expiry = datetime.now(timezone.utc)-timedelta(hours=1)
        self.assertEqual(self.call(token=self.token(expiry=expiry))[0], 401)


if __name__ == '__main__':
    unittest.main()
