import json
import pprint
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
    return "Welcome"
    


@app.route('/login')
@oidc.require_login
def login():
    data = "Welcome {}\n<br /><br />".format(oidc.user_getfield('email'))
    data += "oidc_id_token: {}\n<br /><br />".format(pprint.pformat(g.oidc_id_token).replace('\n', '<br />'))
    data += "user_getinfo: {}\n<br /><br />".format(pprint.pformat(oidc.user_getinfo(USER_FIELDS)).replace('\n', '<br />'))
    data += "user_getinfo for groups: {}\n<br /><br />".format(pprint.pformat(oidc.user_getinfo(['groups'])).replace('\n', '<br />'))
    #data += "g._oidc_userinfo: {}\n<br /><br />".format(pprint.pformat(g._oidc_userinfo).replace('\n','<br />'))
    return data


@app.route('/api')
@oidc.accept_token()
def test_api():
    return json.dumps(oidc.user_getinfo(['email', 'groups']))
