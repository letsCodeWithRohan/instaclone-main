from flask import Flask,render_template,flash,session,request,redirect,url_for
from flask_mysqldb import MySQL
from flask_socketio import SocketIO,join_room,leave_room,send
from flask_cors import CORS
import os
import socket

app = Flask(__name__)
CORS(app)

app.config["UPLOAD_FOLDER"] = "static/uploads/"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'instagram'

mysql = MySQL(app)
app.secret_key = "Insta Clone"

socketio=SocketIO(app)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

def get_owndata():
    mycursor = mysql.connection.cursor()
    mycursor.execute("SELECT * FROM users WHERE username = %s",(session["username"],))
    userdata = mycursor.fetchone()
    mycursor.close()
    return userdata

def get_userdata(id):
    mycursor = mysql.connection.cursor()
    mycursor.execute("SELECT * FROM users WHERE id = %s",(id,))
    userdata = mycursor.fetchone()
    mycursor.close()
    data = {
        "id":userdata[0],
        "username":userdata[1],
        "name":userdata[2],
        "email":userdata[3],
        "password":userdata[4],
        "profile":userdata[5],
        "mobile":userdata[6],
        "bio":userdata[7],
    }
    return data

def get_posts(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT post_id from likes WHERE user_id = %s",(id,))
    liked_posts = cursor.fetchall()
    postarr = []
    for post in liked_posts :
        for i in post :
            postarr.append(i)
    return postarr

@app.route("/",methods=["GET","POST"])
def index() :
    if request.method == "GET" :
        return render_template("index.html")
    else:
        data = request.form
        cursor = mysql.connection.cursor()
        q2 = "INSERT INTO `users`(`username`, `name`, `email`, `password`) VALUES (%s,%s,%s,%s)"
        cursor.execute(q2,(data["username"],data["name"],data["email"],data["password"]))
        mysql.connection.commit()
        cursor.close()
        flash("Registered Successfully")
        return redirect(url_for("login"))

@app.route("/login/",methods=["GET","POST"])
def login():
    if request.method == "GET" :
        return render_template("login.html")
    else:
        data = request.form
        email = data["email"]
        password = data["password"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, username, password,email,picture FROM users WHERE email = %s", (email,))
        resp = cursor.fetchone()
        cursor.close()
        if resp :
            db_id,db_username,db_password,db_email,db_profile = resp
            if db_email == email and db_password==password :
                session["id"] = str(db_id)
                session["username"] = db_username
                session["profile"] = db_profile
                session["email"] = db_email
                return redirect(url_for("feed"))
            elif db_email == email and db_password!=password :
                flash("Password Not Matched")
            else:
                flash("No Account Found")
        else:
            flash("email doesn't exists")
        return redirect(url_for('login'))

@app.route("/feed/")
def feed() :
    if "username" not in session :
        flash("Please Login First")
        return redirect(url_for("login"))
    else: 
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT users.id, users.username, users.picture, posts.id AS post_id, posts.caption, posts.date, posts.picture AS post_picture, COUNT(likes.id) AS like_count FROM users JOIN posts ON users.id = posts.user_id LEFT JOIN likes ON posts.id = likes.post_id GROUP BY posts.id ORDER BY posts.date DESC;")
        data = cursor.fetchall()
        cursor.execute("SELECT * FROM users WHERE username = %s",(session["username"],))
        userdata = cursor.fetchone()
        cursor.close()
        liked_posts = get_posts(session["id"])
        return render_template("feed.html",liked_posts=liked_posts,postdata=list(data),userdata=list(userdata))

@app.route("/post",methods=["GET","POST"])
def post_upload():
    if request.method == "POST":
        data = request.form
        picture = request.files["image"]
        picURL = os.path.join(app.config["UPLOAD_FOLDER"],picture.filename)
        picture.save(picURL)
        query = "INSERT INTO `posts`(`user_id`, `caption`, `picture`) VALUES (%s,%s,%s)"
        cursor = mysql.connection.cursor()
        cursor.execute(query,(session["id"],data["caption"],"uploads/"+picture.filename))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("feed"))

# Post Upload GET Request
@app.route("/upload/",methods=["GET","POST"])
def upload():
    if "username" not in session :
        flash("Please Login First")
        return redirect(url_for("login"))
    else: 
        if request.method == "GET":
            owndata=get_owndata()
            return render_template("upload.html",owndata=owndata)
        else:
            if request.files["image"]:
                picture = request.files["image"]
                picURL = os.path.join(app.config["UPLOAD_FOLDER"],picture.filename)
                picture.save(picURL)
                cursor = mysql.connection.cursor()
                cursor.execute("UPDATE users SET picture=%s WHERE id = %s",("uploads/"+picture.filename,session["id"]))
                mysql.connection.commit()
                session["profile"] = "uploads/"+picture.filename
                cursor.close()
                return redirect(url_for("profile"))

@app.route("/profile/")
def profile() :
    if "username" not in session :
        flash("Please Login First")
        return redirect(url_for("login"))
    else: 
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s",(session["username"],))
        userdata = cursor.fetchone()
        cursor.execute("SELECT id,picture FROM posts WHERE user_id = %s ORDER BY date DESC",(session["id"],))
        userposts = cursor.fetchall()
        cursor.execute("SELECT COUNT(follower_id) FROM `follows` WHERE follower_id=%s",(session["id"],))
        following_count = cursor.fetchone()
        cursor.execute("SELECT COUNT(followed_id) FROM `follows` WHERE followed_id=%s",(session["id"],))
        follower_count = cursor.fetchone()
        cursor.close()
        return render_template("profile.html",following_count=following_count,follower_count=follower_count,userdata=userdata,userposts=list(userposts))

@app.route("/like/<int:post_id>")
def like(post_id):
    if "id" not in session:
        flash("Please Login First")
        return redirect(url_for("login"))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO likes (user_id, post_id) VALUES (%s,%s);",(session["id"],post_id))
        mysql.connection.commit()
        cursor.close()
        return redirect(request.referrer)
    
@app.route("/dislike/<int:post_id>")
def dislike(post_id):
    if "id" not in session:
        flash("Please Login First")
        return redirect(url_for("login"))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM likes WHERE user_id = %s AND post_id = %s;",(session["id"],post_id))
        mysql.connection.commit()
        cursor.close()
        return redirect(request.referrer)

@app.route("/profile_flex/")
def profile_flex() :
    if "username" not in session :
        flash("Please Login First")
        return redirect(url_for("login"))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s",(session["username"],))
        userdata = cursor.fetchone()
        cursor.execute("SELECT users.id AS user_id, users.username, users.picture AS user_picture, posts.id AS post_id, posts.caption, posts.date, posts.picture AS post_picture, COUNT(likes.id) AS like_count FROM users JOIN posts ON users.id = posts.user_id LEFT JOIN likes ON posts.id = likes.post_id WHERE users.id = %s GROUP BY posts.id ORDER BY posts.date DESC;",(session["id"],))
        userposts = cursor.fetchall()
        cursor.execute("SELECT COUNT(follower_id) FROM `follows` WHERE follower_id=%s",(session["id"],))
        following_count = cursor.fetchone()
        cursor.execute("SELECT COUNT(followed_id) FROM `follows` WHERE followed_id=%s",(session["id"],))
        follower_count = cursor.fetchone()
        liked_posts = get_posts(session["id"])
        cursor.close()
        return render_template("profile_flex.html",liked_posts=liked_posts,following_count=following_count,follower_count=follower_count,userdata=userdata,userposts=list(userposts))


@app.route("/edit/")
def edit():
    if "username" not in session:
        flash("Please Login First")
        return redirect(url_for("login"))
    else:
        if request.method == "GET" :
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT username,name,picture,bio FROM users WHERE username = %s",(session["username"],))
            userdata = cursor.fetchone()
            cursor.close()
            return render_template("edit.html",userdata=userdata)
        
@app.route("/update/",methods=["GET","POST"])
def update():
    if request.method == "POST" :
        data = request.form
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET username=%s,name=%s,bio=%s WHERE id = %s",(data["username"],data["name"],data["bio"],session["id"]))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("profile"))

@app.route("/search/",methods=["GET","POST"])
def search():
    if "username" not in session:
        flash("Please Login First")
        return redirect(url_for("login"))
    else:
        if request.method == "GET":
            owndata = get_owndata()
            return render_template("search.html",owndata=owndata)
        else:
            data = request.form["search_input"]
            cursor = mysql.connection.cursor()
            query = "SELECT id,username, name, picture FROM users WHERE username LIKE %s"
            cursor.execute(query, ('%' + data + '%',))
            users = cursor.fetchall()
            cursor.close()
            owndata = get_owndata()
            return render_template("search.html",users=users,owndata=owndata)

@app.route("/userprofile/<int:id>")
def user_profile(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s",(id,))
    userdata = cursor.fetchone()
    cursor.execute("SELECT id,picture FROM posts WHERE user_id = %s ORDER BY date DESC",(id,))
    userposts = cursor.fetchall()
    cursor.execute("SELECT * FROM follows WHERE follower_id=%s AND followed_id=%s",(session["id"],id))
    followed = cursor.fetchone()
    cursor.execute("SELECT COUNT(follower_id) FROM `follows` WHERE follower_id=%s",(id,))
    following_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(followed_id) FROM `follows` WHERE followed_id=%s",(id,))
    follower_count = cursor.fetchone()
    cursor.close()
    owndata = get_owndata()
    return render_template("userprofile.html",userdata=userdata,userposts=userposts,followed=followed,owndata=owndata,following_count=following_count,follower_count=follower_count)

@app.route("/userprofile_flex/<int:id>")
def user_profile_flex(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s",(id,))
    userdata = cursor.fetchone()
    cursor.execute("SELECT users.id AS user_id, users.username, users.picture AS user_picture, posts.id AS post_id, posts.caption, posts.date, posts.picture AS post_picture, COUNT(likes.id) AS like_count FROM users JOIN posts ON users.id = posts.user_id LEFT JOIN likes ON posts.id = likes.post_id WHERE users.id = %s GROUP BY posts.id ORDER BY posts.date DESC;",(id,))
    userposts = cursor.fetchall()
    cursor.execute("SELECT * FROM follows WHERE follower_id=%s AND followed_id=%s",(session["id"],id))
    followed = cursor.fetchone()
    cursor.execute("SELECT COUNT(follower_id) FROM `follows` WHERE follower_id=%s",(id,))
    following_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(followed_id) FROM `follows` WHERE followed_id=%s",(id,))
    follower_count = cursor.fetchone()
    cursor.close()
    liked_posts = get_posts(session["id"])
    owndata = get_owndata()
    return render_template("userprofile_flex.html",liked_posts=liked_posts,userdata=userdata,userposts=userposts,followed=followed,owndata=owndata,following_count=following_count,follower_count=follower_count)


@app.route("/follow/<int:id>")
def follow(id):
    if "id" not in session:
        flash("Please Login First")
        return redirect(url_for("login"))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO follows (follower_id,followed_id) VALUES (%s,%s)",(session["id"],id))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("user_profile",id=id))
    
@app.route("/unfollow/<int:id>")
def unfollow(id):
    if "id" not in session:
        flash("Please Login First")
        return redirect(url_for("login"))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM follows WHERE followed_id=%s AND follower_id=%s",(id,session["id"]))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("user_profile",id=id))
    
# Under construction working
@app.route("/following/<int:id>/")
def following(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT users.id,users.username,users.name,users.picture FROM follows JOIN users ON users.id = follows.followed_id WHERE follower_id = %s",(id,))
    data = cursor.fetchall()
    userdata = get_userdata(id)
    return render_template("following.html",users=data,userdata=userdata)

@app.route("/followers/<int:id>/")
def followers(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT users.id, users.username, users.name, users.picture FROM follows JOIN users ON users.id = follows.follower_id WHERE follows.followed_id = %s",(id,))
    data = cursor.fetchall()
    userdata = get_userdata(id)
    return render_template("followers.html",users=data,userdata=userdata)

@app.route("/delete_post/<int:id>/")
def delete_post(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM likes WHERE post_id = %s",(id,))
    cursor.execute("DELETE FROM posts WHERE id = %s",(id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for("profile_flex"))

@app.route("/chat/<int:id>/")
def chat(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username,picture FROM users WHERE id = %s",(id,))
    data = cursor.fetchone()
    userdata = {}
    userdata["id"] = id
    userdata["username"] = data[0]
    userdata["profile"] = data[1]
    cursor.execute('''SELECT message, sender_id, receiver_id 
    FROM messages 
    WHERE (sender_id = %s AND receiver_id = %s) 
    OR (sender_id = %s AND receiver_id = %s) 
    ORDER BY timestamp''',(session['id'],id,id,session['id']))
    old_msg = cursor.fetchall()
    prevMsg = []
    for msg in old_msg:
        dct = {}
        dct["message"] = msg[0]
        dct["sender"] = msg[1]
        dct["receiver"] = msg[2]
        prevMsg.append(dct)
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return render_template("chat.html",userdata=userdata,user_id=id,ip_address=ip_address,loggedInId=session["id"],prevMsg=prevMsg)

@socketio.on('join')
def on_join(data):
    room = get_room_name(data['user_id'], data['other_user_id'])
    join_room(room)
    send(f"{data['username']} has joined the room.", to=room)

@socketio.on('message')
def handle_message(data):
    room = get_room_name(data['user_id'], data['other_user_id'])
    cursor = mysql.connection.cursor()
    query = "INSERT INTO messages (sender_id, receiver_id, message) VALUES (%s, %s, %s)"
    cursor.execute(query, (data['user_id'], data['other_user_id'], data['message']))
    mysql.connection.commit()
    send({'user_id': data['user_id'], 'message': data['message']}, to=room)

def get_room_name(user1, user2):
    # Generate a unique room name based on the two user IDs
    return f"room_{min(user1, user2)}_{max(user1, user2)}"

@app.route("/message/")
def message():
    cursor = mysql.connection.cursor()
    query = "SELECT users.id, users.name, users.picture FROM users WHERE users.id IN (SELECT follower_id FROM follows WHERE followed_id = %s UNION SELECT followed_id FROM follows WHERE follower_id = %s)"
    cursor.execute(query,(session['id'],session['id']))
    msg_users = cursor.fetchall()
    user_list = []
    for user in msg_users:
        dct = {}
        dct["id"] = user[0]
        dct["name"] = user[1]
        dct["profile"] = user[2]
        user_list.append(dct)
        cursor.close()
    return render_template("message.html",users=user_list)

@app.route("/logout/")
def logout():
    if "username" in session:
        session.pop("id",None)
        session.pop("email",None)
        session.pop("username",None)
        session.pop("profile",None)
        return redirect(url_for("login"))
    else :
        return redirect(url_for("login"))
    
@app.route("/more")
def more():
    return redirect(url_for("under_const"))

@app.route("/notification")
def notification():
    return redirect(url_for("under_const"))
    
@app.route("/under-construction")
def under_const():
    return render_template("construction.html")

if __name__ == "__main__" :
    socketio.run(app, debug=True,host='0.0.0.0')