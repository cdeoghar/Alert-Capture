from flask import Flask, request, jsonify, session
import requests
import json
import os

clientID = "C12d73b781dfefdcebc358b0793c0afd405d5aaecab441e872c6bc28a0d014881"
secretID = "f5c5d7db01c3f1a7cd935931a58f131a0c6f741fd05ae0f151d6df8da04f1a3c"
redirectURI = "http://127.0.0.1:8083/oauth" # This could be different if you publicly expose this endpoint.
app = Flask(__name__)
app.secret_key = os.urandom(24)
oauth_url = "https://webexapis.com/v1/authorize?client_id=C12d73b781dfefdcebc358b0793c0afd405d5aaecab441e872c6bc28a0d014881&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8083%2Foauth&scope=spark-compliance%3Amemberships_read%20spark-admin%3Aresource_groups_read%20spark%3Aall%20analytics%3Aread_all%20spark%3Apeople_read%20spark-admin%3Avideo_mesh_api_read%20spark-admin%3Aorganizations_read%20spark%3Amessages_read%20spark-admin%3Aworkspace_metrics_read%20spark-compliance%3Ateam_memberships_read%20spark%3Amemberships_read%20identity%3Aorganizations_read%20spark-admin%3Ahybrid_clusters_read%20identity%3Agroups_read%20identity%3Atokens_read%20spark-compliance%3Amessages_read%20spark-admin%3Aevents_read%20spark-compliance%3Ameetings_read%20identity%3Apeople_read%20spark-admin%3Aworkspaces_read%20spark-admin%3Aworkspace_locations_read%20spark%3Adevices_read%20spark-compliance%3Aevents_read%20spark-admin%3Aresource_group_memberships_read%20spark-compliance%3Arooms_read%20spark-admin%3Acall_qualities_read%20spark%3Akms%20audit%3Aevents_read%20spark-admin%3Ahybrid_connectors_read%20spark-admin%3Amessages_read%20spark-compliance%3Ateams_read%20spark-admin%3Areports_read%20spark%3Ateams_read&state=1234abcd"

template1 = f"""<h1>GRANT INTEGRATION ACCESS</h1>
  <!-- STEP 1 : Button that kicks off the flow by sending your user to the following URL along with a standard set of OAuth query parameters, state parameter is                             hard coded here-->
  <!-- The scope parameter in the integration is set to spark:all for simplicity in this example, in production this should be fine tuned -->
  <div class='center'>
    <a href={oauth_url}>
      <div class='button' style='width:512px;'>GRANT</div>
    </a>
  </div>"""


@app.route("/oauth") # Endpoint acting as Redirect URI.
def oauth():
  print("function : oauth()")
  """Retrieves oauth code to generate tokens for users"""
  state = request.args.get("state")
  state = '1234abcd'
  print('state : ' + state)
  if state == '1234abcd':
    code = request.args.get("code") # STEP 2 : Capture value of the 
                                    # authorization code.
    print("OAuth code:", code)
    print("OAuth state:", state)
    get_tokens(code)
    return jsonify({"status": "success", "code": code, "state": state})
  else:
    return template1

def get_tokens(code):
    print("function : get_tokens()")
    print("code:", code)
    #STEP 3 : use code in response from webex api to collect the code parameter
    #to obtain an access token or refresh token
    url = "https://webexapis.com/v1/access_token"
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    payload = ("grant_type=authorization_code&client_id={0}&client_secret={1}&"
                    "code={2}&redirect_uri={3}").format(clientID, secretID, code, redirectURI)
    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)
    print(results)
    
    access_token = results["access_token"]
    refresh_token = results["refresh_token"]

    session['oauth_token'] = access_token 
    session['refresh_token'] = refresh_token

    print("Token stored in session : ", session['oauth_token'])
    print("Refresh Token stored in session : ", session['refresh_token'])
    store_token_to_file(refresh_token)
    store_token_to_file(access_token, "access_token")

    return 

def get_tokens_refresh():
    print("function : get_token_refresh()")
    
    url = "https://webexapis.com/v1/access_token"
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    payload = ("grant_type=refresh_token&client_id={0}&client_secret={1}&"
                    "refresh_token={2}").format(clientID, secretID, session['refresh_token'])
    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)
    
    access_token = results["access_token"]
    refresh_token = results["refresh_token"]

    session['oauth_token'] = access_token
    session['refresh_token'] = refresh_token

    print("Token stored in session : ", session['oauth_token'])
    print("Refresh Token stored in session : ", session['refresh_token'])
    
    print("function : get_token_refresh()")
    
    url = "https://webexapis.com/v1/access_token"
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    payload = ("grant_type=refresh_token&client_id={0}&client_secret={1}&"
                    "refresh_token={2}").format(clientID, secretID, refresh_token)
    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)
    
    access_token = results["access_token"]
    refresh_token = results["refresh_token"]

    session['oauth_token'] = access_token
    session['refresh_token'] = refresh_token

    print("Token stored in session : ", access_token)
    print("Refresh Token stored in session : ", refresh_token)
    store_token_to_file(refresh_token)
    store_token_to_file(access_token, "access_token")
    return access_token, refresh_token

def read_token_from_file(file_path="refresh_token"):
        """Reads the refresh token from a file."""
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                refresh_token = file.read().strip()
                print("Read refresh_token from file:", refresh_token)
                return refresh_token
        else:
            print("refresh_token file does not exist.")
            return None

def store_token_to_file(refresh_token, file_path="refresh_token"):
    """Stores the refresh token to a file."""
    with open(file_path, "w") as file:
        file.write(refresh_token)
        print("New refresh_token stored in file:", refresh_token)
        
def get_tokens_refresh_static(refresh_token=None):
    print("function : get_token_refresh_static()")
    
    # Check if refresh_token file exists in the current folder
    refresh_token_file = "refresh_token"
    refresh_token = refresh_token or read_token_from_file(refresh_token_file)
    if not refresh_token:
        print("No refresh token found. Proceeding with provided token.")
    url = "https://webexapis.com/v1/access_token"
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    payload = ("grant_type=refresh_token&client_id={0}&client_secret={1}&"
                    "refresh_token={2}").format(clientID, secretID, refresh_token)
    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)
    
    access_token = results["access_token"]
    refresh_token = results["refresh_token"]

    # session['oauth_token'] = access_token
    # session['refresh_token'] = refresh_token

    # Store the new refresh token in the current folder
    store_token_to_file(refresh_token, refresh_token_file)
    store_token_to_file(access_token, "access_token")

    print("Token stored in session : ", access_token)
    print("Refresh Token stored in session : ", refresh_token)
    return access_token, refresh_token

@app.route("/") 
def main_page():
    """Main Grant page"""
    return template1

@app.route("/spaces",methods=['GET'])
def  spaces():
    print("function : spaces()")
    print("accessing token ...")
    response = api_call()

    print("status code : ", response.status_code)
    #Do a check on the response. If the access_token is invalid then use refresh
    # tokent to ontain a new set of access token and refresh token.
    if (response.status_code == 401) :
        get_tokens_refresh()
        response = api_call()

    r = response.json()['items']
    print("response status code : ", response.status_code)
    spaces = []
    for i in range(len(r)) :
        spaces.append(r[i]['title'])
    print(r)

    return render_template("spaces.html", spaces = spaces)

def api_call() :
    accessToken = session['oauth_token']
    url = "https://webexapis.com/v1/rooms"
    headers = {'accept':'application/json','Content-Type':'application/json','Authorization': 'Bearer ' + accessToken}
    response = requests.get(url=url, headers=headers)
    return response

# if __name__ == '__main__':
    # app.run("0.0.0.0", port=8083, debug=True)

get_tokens_refresh_static()