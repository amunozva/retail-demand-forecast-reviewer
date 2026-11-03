"""Auth0 OAuth 2.1 access-token verification and RFC 9728 resource metadata."""
import os

RESOURCE = os.getenv('MCP_RESOURCE_URI', '').rstrip('/')
DOMAIN = os.getenv('AUTH0_DOMAIN', '').strip().rstrip('/')
SCOPE = os.getenv('AUTH0_REQUIRED_SCOPE', 'forecast:read')
ISSUER = f'https://{DOMAIN}/'
METADATA_PATH = '/.well-known/oauth-protected-resource/mcp'
_client = None


def validate_config():
    if (not DOMAIN or '://' in DOMAIN or '/' in DOMAIN or not RESOURCE.startswith('https://')
            or not RESOURCE.endswith('/mcp') or not SCOPE.strip()):
        raise SystemExit('OAuth needs AUTH0_DOMAIN, https MCP_RESOURCE_URI ending /mcp, and AUTH0_REQUIRED_SCOPE')


def metadata():
    return {'resource': RESOURCE, 'authorization_servers': [ISSUER],
            'scopes_supported': [SCOPE], 'bearer_methods_supported': ['header']}


def metadata_url():
    return RESOURCE[:-len('/mcp')] + METADATA_PATH


def challenge():
    return f'Bearer realm="retail-demand-reviewer", resource_metadata="{metadata_url()}", scope="{SCOPE}"'


def verify(header):
    global _client
    if not header.startswith('Bearer ') or header.count(' ') != 1:
        return False
    token = header[7:]
    if not token:
        return False
    try:
        import jwt
        from jwt import PyJWKClient
        if _client is None:
            _client = PyJWKClient(ISSUER + '.well-known/jwks.json', cache_jwk_set=True, lifespan=300)
        signing_key = _client.get_signing_key_from_jwt(token)
        claims = jwt.decode(token, signing_key.key, algorithms=['RS256'], issuer=ISSUER,
                            audience=RESOURCE, options={'require': ['iss', 'aud', 'exp', 'iat']}, leeway=30)
        scope_claim = claims.get('scope', '')
        return isinstance(scope_claim, str) and SCOPE in scope_claim.split()
    except Exception:
        # JWKS/network errors and any invalid JWT fail closed. Never log tokens.
        return False
