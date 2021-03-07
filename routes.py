from data import thanks
from data import threads
from data import messages
from data import users
from data import forums
from forms import ForumForm, RegistartionForm, LoginForm, SignatureForm, MessageForm, ThreadForm
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
            return redirect(request.referrer)
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
    if delete_type == "2":
        forums.delete_forum(delete_id)
        flash('Keskustelualue poistettu', 'success')
    if delete_type == "3":
        forums.delete_subforum(delete_id)
        flash('Alalauta poistettu', 'success')
    if delete_type == "0":
        threads.delete_thread(delete_id)
        flash('Lanka poistettu', 'success')
    return redirect("/")

@auth.route("/reply", methods=["POST"])
def reply():
    form = MessageForm(request.form)
    username = session["username"]
    reply_type = request.form["reply_type"]
    if form.validate():
        if reply_type == "1":
            sent_to = request.form["sent_to"]
            messages.send_dm(form.message.data,sent_to,username)
            flash('Viesti lähetetty', 'success')
            return redirect("/profile/"+str(sent_to)+"/chat")
        else:
            thread_id = request.form["thread_id"]
            messages.send_reply(form.message.data,thread_id,username)
            flash('Viesti lähetetty', 'success')
            return redirect(request.referrer)
    else:
        for field in form.errors:
            for error in form.errors[field]:
                flash(error, 'error')
        return redirect(request.referrer)     

@auth.route("/create_forum", methods=["POST"])
def create_forum():
    form = ForumForm(request.form)
    forum_type = request.form["forum_type"]
    if form.validate():
        if forum_type == "1":                           ##1 for subforums, 0 for forums
            forum_id = request.form["forum_id"]
            if forums.new_subforum(form.title.data,form.description.data,forum_id):
                flash('Alalauta luotu', 'success')
                return redirect("/")
            else:
                flash('Tällä keskustelualueella on jo samanniminen alalauta', 'error')
                return redirect(request.referrer)
        else:
            if forums.new_forum(form.title.data):
                flash('Keskustelualue luotu', 'success')
                return redirect("/")
            else:
                flash('Samanniminen keskustelualue on jo olemassa', 'error')
                return redirect(request.referrer)
    else:
        for field in form.errors:
            for error in form.errors[field]:
                flash(error, 'error')
        return redirect(request.referrer)    

@auth.route("/create_thread", methods=["POST"])
def create_thread():
    form = ThreadForm(request.form)
    username = session["username"]
    subforum_id = request.form["subforum_id"]
    if form.validate():
        thread_id = threads.new(form.title.data, username, subforum_id)
        if thread_id:
            messages.send_reply(form.message.data, thread_id[1], username)
            flash('Keskustelu luotu', 'success')
            return redirect("/subforum/"+str(subforum_id))
        else:
            flash('Tällä alalaudalla on jo samannimen lanka', 'error')
            return redirect(request.referrer)
    else:
        for field in form.errors:
                for error in form.errors[field]:
                    flash(error, 'error')
        return redirect(request.referrer)   

@auth.route("/lock", methods=["POST"])
def lock():   
    lock_id = request.form["lock_id"]
    lock_type = request.form["lock_type"]
    if lock_type == "1":
        threads.lock_thread(lock_id)
    else:
        threads.unlock_thread(lock_id)
    return redirect(request.referrer)  

@auth.route("/ban", methods=["POST"])
def ban():
    ban_id = request.form["ban_id"]
    ban_type = request.form["ban_type"]
    if ban_type == "1":
        users.ban_user(ban_id)
    else:
        users.unban_user(ban_id)
    return redirect(request.referrer)  
    
@auth.route("/signature", methods=["POST"])
def signature():
    form = SignatureForm(request.form)
    user_id = request.form["user_id"]
    if form.validate():
        users.add_signature(user_id,form.signature.data)
        flash('Allekirjoitus päivitetty', 'success')
    else:
        for field in form.errors:
                for error in form.errors[field]:
                    flash(error, 'error')
    return redirect(request.referrer)        

@auth.route("/sticky", methods=["POST"])
def sticky():
    sticky_id = request.form["sticky_id"]
    sticky_type = request.form["sticky_type"]
    if sticky_type == "1":
        threads.sticky_thread(sticky_id)
    else:
        threads.unsticky_thread(sticky_id)
    return redirect(request.referrer)
