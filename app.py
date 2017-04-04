import json
from flask import Flask, g
from flask_oidc import OpenIDConnect

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

oidc = OpenIDConnect(app)


# provided by https://auth.mozilla.auth0.com/.well-known/openid-configuration
USER_FIELDS = ["openid", "profile", "offline_access", "name", "given_name", "family_name",
               "nickname", "email", "email_verified", "picture", "created_at", "identities", "phone", "address"]


@app.route('/')
def index():
    if not oidc.user_loggedin:
        return "Not logged in"

    data = "Welcome {}\n<br />".format(oidc.user_getfield('email'))

    data += "oidc_id_token: {}\n<br />".format(g.oidc_id_token)

    data += "user_getinfo: {}\n<br />".format(oidc.user_getinfo(fields))
    data += "g._oidc_userinfo: {}\n<br />".format(g._oidc_userinfo)
    return data
    


@app.route('/login')
@oidc.require_login
def login():
    return "Welcome {}".format(oidc.user_getfield('email'))


@app.route('/api')
@oidc.accept_token()
def test_api():
    return json.dumps('Welcome %s' % g.oidc_token_info['sub'])
