from flask import Flask,render_template,flash,session,request,redirect,url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/uploads/"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'instagram'

mysql = MySQL(app)
app.secret_key = "Insta Clone"

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
        return redirect(url_for("login"))

@app.route("/login/",methods=["GET","POST"])
def login():
    if request.method == "GET" :
        return render_template("login.html")
    else:
        data = request.form
        username = data["username"]
        password = data["password"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        resp = cursor.fetchone()
        cursor.close()
        if resp :
            db_id,db_username,db_password = resp
            if db_username == username and db_password==password :
                session["id"] = str(db_id)
                session["username"] = db_username
                session["password"] = db_password
                return redirect(url_for("feed"))
            elif db_username == username and db_password!=password :
                flash("Password Not Matched")
            else:
                flash("No Account Found")
        else:
            flash("username doesn't exists")
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

@app.route("/logout/")
def logout():
    if "username" in session:
        session.pop("id",None)
        session.pop("username",None)
        session.pop("password",None)
        return redirect(url_for("login"))
    else :
        return redirect(url_for("login"))

if __name__ == "__main__" :
    app.run(debug=True,host='0.0.0.0')