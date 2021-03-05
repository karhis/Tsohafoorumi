from data import users
from flask import Blueprint, render_template

userlist = Blueprint('userlist',__name__)

@userlist.route("/userlist")
def userlistpage():
    userslist = users.get_userlist()
    return render_template("/userlist.html", users=userslist)        
