import dash
import dash_bootstrap_components as dbc
from dash import html,dcc, Input, Output, State
import dash_uploader as du
import os
from flask import Flask, send_from_directory, session
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user
from database import mongodb_config,mongodb_utility
import dash_mantine_components as dmc
from dash_iconify import DashIconify


server = Flask(__name__)

app = dash.Dash(__name__,server=server,use_pages=True,prevent_initial_callbacks="initial_duplicate",external_stylesheets=[dbc.themes.LITERA, dbc.icons.BOOTSTRAP,'https://oss.sheetjs.com/sheetjs/xlsx.full.min.js'],suppress_callback_exceptions=True)
#server = app.server

UPLOAD_FOLDER_ROOT = os.path.join(os.path.dirname(__file__),'uploaded_evidence')
du.configure_upload(app, UPLOAD_FOLDER_ROOT)

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_FOLDER_ROOT, path, as_attachment=True)


# Updating the Flask Server configuration with Secret Key to encrypt the user session cookie
server.config.update(SECRET_KEY=os.urandom(12))

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"

class User(UserMixin):
    # User data model. It has to have at least self.id as a minimum
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """This function loads the user by user id. Typically this looks up the user from a user database.
    We won't be registering or looking up users in this example, since we'll just login using LDAP server.
    So we'll simply return a User object with the passed in username.
    """
    return User(username)

app.layout = html.Div(children=[
    dcc.Location(id="url-login"),
    dash.page_container,
    #dcc.Store(id="login-status", storage_type="session"),
])

@app.callback(
    #Output("login-status", "data"),
    Output("user-status-header", "children"),
    Input("url-login", "pathname")
)
def update_authentication_status(path):
   
    logged_in = current_user.is_authenticated
    #print(session)
    if path == "/logout" and logged_in:
        logout_user()
    if logged_in:
        link=dmc.HoverCard(
            shadow="md",
            children=[
                dmc.HoverCardTarget(
                    dmc.Avatar(
                        #str(session["_user_id"] if session else ""), 
                        src="https://e7.pngegg.com/pngimages/799/987/png-clipart-computer-icons-avatar-icon-design-avatar-heroes-computer-wallpaper-thumbnail.png",
                        color="cyan",
                        radius="xl",
                    )
                ),
                dmc.HoverCardDropdown(
                    [   
                        dmc.Text("Welcome: "+ str(session["_user_id"] if session else ""),weight=500,color="lime"),
                        dmc.Group(
                            [
                                dmc.Tooltip(
                                    dmc.Anchor(
                                            DashIconify(icon="ri:logout-circle-line", width=20),
                                            href="/logout",
                                            #target="_blank",
                                        ),
                                    label="Logout",
                                    withArrow=True,
                                ),        
                                dmc.Tooltip(
                                    dmc.Anchor(
                                            DashIconify(icon="healthicons:ui-user-profile", width=20),
                                            href="/profile",
                                            #target="_blank",
                                        ),
                                    label="Profile",
                                    withArrow=True,
                                ),            
                            ],
                            p=0,
                        ),
                    ]
                ),
            ],
        )
    else:
        link=dmc.HoverCard(
            shadow="md",
            children=[
                dmc.HoverCardTarget(
                    dmc.Avatar(
                        radius="xl",
                    )
                ),
                dmc.HoverCardDropdown(
                    [
                        dmc.Text("Please login",weight=500,color="red"),
                        dmc.Group(
                            [
                                dmc.Tooltip(
                                    dmc.Anchor(
                                            DashIconify(icon="uiw:login", width=20),
                                            href="/login",
                                            #target="_blank",
                                        ),
                                    label="Login",
                                    withArrow=True,
                                ),              
                            ],
                            p=0,
                        ),
                    ]
                ),
            ],
        )
    return  link

@app.callback(
    Output("output-state", "children"),
    Output('url_login', 'pathname'),
    Input("login-button", "n_clicks"),
    State("uname-box", "value"),
    State("pwd-box", "value"),
    prevent_initial_call=True,
)
def login_button_click(n_clicks, username, password):
    if n_clicks > 0:
        user_exists,user_type = mongodb_utility.user_exists(username, password)
        if user_exists:
            login_user(User(username))
            if user_type == "admin":
                return "", "/admin"
            elif user_type == "customer":
                return "", "/takesurvey"
        return "Incorrect username or password", "/login"


if __name__ == "__main__":
    #app.run_server(debug=False,host='0.0.0.0',port='8080')
    app.run_server(debug=True)

