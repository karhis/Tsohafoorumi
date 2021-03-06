from data import users
from data import messages
from forms import SignatureForm
from flask import Blueprint, render_template, session

profile = Blueprint('profile',__name__,url_prefix='/profile')

@profile.route("/<id>")
def profilepage(id):
    replys = messages.get_replys_titles(id)
    profile = users.get_profile(id)
    form = SignatureForm()
    return render_template("profile.html", messages=replys, id=id, profile=profile, form=form)

@profile.route("/<id>/chat", methods=["GET"])
def chat(id):
    session_username = session["username"]
    sent_dms = messages.get_sent_dms(id,session_username)
    gotten_dms = messages.get_gotten_dms(id,session_username)
    profile= users.get_profile(id)
    dms = sent_dms + gotten_dms
    dms.sort()
    return render_template("chat.html", dms=dms, id=id, profile=profile)
