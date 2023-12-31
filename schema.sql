
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'USER',
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP    
);


DROP TABLE IF EXISTS address;

CREATE TABLE address (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address_line_1 TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    pin INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)                                                                          
);


