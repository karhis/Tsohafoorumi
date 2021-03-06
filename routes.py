from data import thanks
from data import threads
from data import messages
from data import users
from data import forums
from forms import RegistartionForm, LoginForm
from flask import Blueprint, request, redirect, render_template, session, flash

auth = Blueprint('auth',__name__)

@auth.route("/login")
def login_form():
    form = LoginForm()
    return render_template("login.html", form=form)

@auth.route("/login", methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate():
        if users.login(form.username.data,form.password.data):
            flash('Sisäänkirjautuminen onnistui!', 'success')
            return redirect("/")
        else:
            flash('Sisäänkirjautuminen epäonnistui, väärä käyttäjätunnus tai salasana', 'error')
            return redirect(request.referrer)
    else:
        for field in form.errors:
            for error in form.errors[field]:
                flash(error, 'error')
        return redirect(request.referrer)

@auth.route("/logout")
def logout():
    users.logout()
    flash('Olet kirjautunut ulos', 'success')
    return redirect("/")

@auth.route("/register")
def register_form():
        form = RegistartionForm()
        return render_template("register.html", form=form)

@auth.route("/register", methods=["POST"])
def register():
    form = RegistartionForm(request.form)
    if form.validate():
        if users.register(form.username.data,form.password.data):
            flash('Rekisteröityminen onnistui!', 'success')
            return redirect("/")
        else:
            flash('Käyttäjätunnus on jo käytössä', 'error')
    else:
        for field in form.errors:
                for error in form.errors[field]:
                    flash(error, 'error')
        return redirect(request.referrer)

@auth.route("/thank", methods=["POST"])
def thank():
    username = session["username"]
    thank_type = request.form["thank_type"]
    if thank_type == "1":           #1 for messages, 0 for threads
        message_id = request.form["message_id"]
        thanks.thank_message(message_id,username)
        return redirect(request.referrer)     
    else:
        thread_id = request.form["thread_id"]
        thanks.thank_thread(thread_id,username)
        return redirect(request.referrer)

@auth.route("/delete", methods=["POST"])
def delete():   
    delete_id = request.form["delete_id"]
    delete_type = request.form["delete_type"]
    if delete_type == "1":          #1 for messages, 0 for threads, 2 for forums, 3 for subforums
        messages.delete_message(delete_id)
        flash('Viesti poistettu', 'success')
        return redirect("/")
    if delete_type == "2":
        forums.delete_forum(delete_id)
        flash('Keskustelualue poistettu', 'success')
        return redirect("/")
    if delete_type == "3":
        forums.delete_subforum(delete_id)
        flash('Alalauta poistettu', 'success')
        return redirect("/")
    else: 
        threads.delete_thread(delete_id)
        flash('Lanka poistettu', 'success')
        return redirect("/")

@auth.route("/reply", methods=["POST"])
def reply():
    username = session["username"]
    message = request.form["message"]
    reply_type = request.form["reply_type"]
    if reply_type == "1":
        sent_to = request.form["sent_to"]
        messages.send_dm(message, sent_to, username)
        flash('Viesti lähetetty', 'success')
        return redirect("/profile/"+str(sent_to)+"/chat")
    else:
        thread_id = request.form["thread_id"]
        messages.send_reply(message, thread_id, username)
        flash('Viesti lähetetty', 'success')
        return redirect(request.referrer)

@auth.route("/create_forum", methods=["POST"])
def create_forum():
    forumname = request.form["forumname"]
    forum_type = request.form["forum_type"]
    if forum_type == "1":
        forum_id = request.form["forum_id"]
        descri = request.form["descri"]
        forums.new_subforum(forumname,descri,forum_id)
        flash('Alalauta luotu', 'success')
        return redirect("/")
    else:
        forums.new_forum(forumname)
        flash('Keskustelualue luotu', 'success')
        return redirect("/")

@auth.route("/create_thread", methods=["POST"])
def create_thread():
    title = request.form["title"]
    username = session["username"]
    subforum_id = request.form["subforum_id"]
    thread_id = threads.new(title, username, subforum_id)
    message = request.form["message"]
    messages.send_reply(message, thread_id, username)
    flash('Keskustelu luotu', 'success')
    return redirect("/subforum/"+str(subforum_id))

@auth.route("/lock", methods=["POST"])
def lock():   
    lock_id = request.form["lock_id"]
    lock_type = request.form["lock_type"]
    if lock_type == "1":
        threads.lock_thread(lock_id)
        return redirect("/")
    else:
        threads.unlock_thread(lock_id)
        return redirect("/")

@auth.route("/ban", methods=["POST"])
def ban():
    ban_id = request.form["ban_id"]
    ban_type = request.form["ban_type"]
    if ban_type == "1":
        users.ban_user(ban_id)
        return redirect("/")
    else:
        users.unban_user(ban_id)
        return redirect("/")
    
@auth.route("/signature", methods=["POST"])
def signature():
    user_id = request.form["user_id"]
    signature = request.form["signature"]
    users.add_signature(user_id,signature)
    flash('Allekirjoitus päivitetty', 'success')
    return redirect(request.referrer)
