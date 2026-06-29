# ============================================================
# auth.py
# Handles Registration, Login, and User Storage
# Used by app.py - do not run this file directly
# ============================================================


import json
import os
import hashlib

USER_DB = "users.json"

def hash_password(password):
return hashlib.sha256(
password.encode()
).hexdigest()

def load_users():

if not os.path.exists(USER_DB):  

    with open(USER_DB, "w") as f:  
        json.dump({}, f)  

with open(USER_DB, "r") as f:  
    return json.load(f)

def save_users(users):

with open(USER_DB, "w") as f:  
    json.dump(users, f, indent=2)

def register_user(
full_name,
username,
password
):

users = load_users()  

if username in users:  
    return False  

users[username] = {  

    "full_name": full_name,  

    "password":  
    hash_password(password)  

}  

save_users(users)  

return True

def login_user(
username,
password
):

users = load_users()  

if username not in users:  
    return None  

if (  
    users[username]["password"]  
    ==  
    hash_password(password)  
):  

    return users[username][  
        "full_name"  
    ]  

return None language agnostic chatbot project correct thana
