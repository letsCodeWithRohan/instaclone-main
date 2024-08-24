# Instagram-Clone
Insta Clone Flask Project

<h3>Folder Structure</h3>
<pre>
Instagram
|--static
  |--stylesheets
  |--uploads
  |--images
|--templates
  |-feed.html
  |-profile.html
  |-userprofile.html
  ....
|-app.py
</pre>

## Setup

<h4>Step-1</h4>
<p>Create new Folder and create virtual environment</p>

```html
virtualenv .venv
```
<p>OR</p>

```python
python -m venv .venv
```
<h4>Step-2</h4>
<p>Activate Virtual Environment</p>

```bash
.venv\Scripts\activate
```

<h4>Step-3</h4>
<p>Install Modules/Packages</p>

```html
pip install flask flask-mysqldb
```

<h4>Database and table setup</h4>

```SQL
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255),
  name VARCHAR(255),
  email VARCHAR(255),
  password VARCHAR(255),
  picture VARCHAR(255) DEFAULT 'def.png',
  contact VARCHAR(255) DEFAULT '1234567890',
  bio TEXT DEFAULT 'No bio added'
);
```

```SQL
CREATE TABLE posts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  caption TEXT,
  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  picture VARCHAR(255),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
```

```SQL
CREATE TABLE follows (
  id INT AUTO_INCREMENT PRIMARY KEY,
  follower_id INT NOT NULL,
  followed_id INT NOT NULL,
  follow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (follower_id) REFERENCES users(id),
  FOREIGN KEY (followed_id) REFERENCES users(id),
  UNIQUE KEY unique_follow (follower_id, followed_id)
);
```

```SQL
CREATE TABLE likes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  post_id INT NOT NULL,
  like_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (post_id) REFERENCES posts(id),
  UNIQUE KEY unique_like (user_id, post_id)
);
```

<p>Optional</p>

```SQL
SELECT 
    users.id AS user_id,
    users.username,
    users.picture AS user_picture,
    posts.id AS post_id,
    posts.caption,
    posts.date,
    posts.picture AS post_picture,
    COUNT(likes.id) AS like_count
FROM 
    users
JOIN 
    posts ON users.id = posts.user_id
LEFT JOIN 
    likes ON posts.id = likes.post_id
WHERE 
    users.id = 7
GROUP BY 
    posts.id
ORDER BY 
    posts.date DESC;
```
