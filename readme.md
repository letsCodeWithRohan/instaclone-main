HQ instagram clone

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

CREATE TABLE posts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  caption TEXT,
  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  picture VARCHAR(255),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE follows (
  id INT AUTO_INCREMENT PRIMARY KEY,
  follower_id INT NOT NULL,
  followed_id INT NOT NULL,
  follow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (follower_id) REFERENCES users(id),
  FOREIGN KEY (followed_id) REFERENCES users(id),
  UNIQUE KEY unique_follow (follower_id, followed_id)
);

CREATE TABLE likes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  post_id INT NOT NULL,
  like_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (post_id) REFERENCES posts(id),
  UNIQUE KEY unique_like (user_id, post_id)
);

SELECT 
    users.id AS user_id,
    users.username,
    users.picture AS user_picture,
    posts.id AS post_id,
    posts.caption,
    posts.date AS post_date,
    posts.picture AS post_picture
FROM 
    users
JOIN 
    posts ON users.id = posts.user_id;
