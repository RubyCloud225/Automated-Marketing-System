-- Create the 'urls' table
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    url VARCHAR(100) NOT NULL,
    processed BOOLEAN DEFAULT FALSE
);

-- Create the 'articles' table
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    url TEXT NOT NULL
);

-- Create the 'newsletters' table
CREATE TABLE newsletters (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);

-- Create the 'EmailSubscribers' table
CREATE TABLE EmailSubscribers (
    SubscriberID SERIAL PRIMARY KEY,
    Email VARCHAR(255) NOT NULL UNIQUE,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    SubscriberDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    IsActive BOOLEAN DEFAULT TRUE,
    OptOutDate TIMESTAMP
);

-- Create the 'members' table
CREATE TABLE members (
    MemberId SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR NOT NULL
);