-- init.sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS tip_data (
                                        id SERIAL PRIMARY KEY,
                                        content TEXT,
                                        embedding vector(1536)
    );

-- Users Table
CREATE TABLE users (
    no SERIAL PRIMARY KEY,
    id VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nickname VARCHAR(50) NOT NULL UNIQUE,
    profile_image TEXT DEFAULT 'default_profile.png',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Group Table
CREATE TABLE groups (
    no SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- GroupMember Table
CREATE TABLE group_member (
    no SERIAL PRIMARY KEY,
    user_no INTEGER NOT NULL,
    group_no INTEGER NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Storage Table
CREATE TABLE storage (
    no SERIAL PRIMARY KEY,
    group_no INTEGER,
    user_no INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Tip Table
CREATE TABLE tip (
    no SERIAL PRIMARY KEY,
    user_no INTEGER NOT NULL,
    url TEXT,
    title TEXT,
    content_summary TEXT,
    is_public BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Bookmark Table
CREATE TABLE bookmark (
    no SERIAL PRIMARY KEY,
    user_no INTEGER NOT NULL,
    tip_no INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Follow Table
CREATE TABLE follow (
    no SERIAL PRIMARY KEY,
    follower_no INTEGER NOT NULL,
    following_no INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Notification Table
CREATE TABLE notification (
    no SERIAL PRIMARY KEY,
    receiver_no INTEGER NOT NULL,
    tip_no INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    type VARCHAR(50) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE NOT NULL
);

-- StorageTip Table
CREATE TABLE storage_tip (
    no SERIAL PRIMARY KEY,
    tip_no INTEGER NOT NULL,
    storage_no INTEGER NOT NULL
);

-- Tag Table
CREATE TABLE tag (
    no SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- TipTag Table
CREATE TABLE tip_tag (
    no SERIAL PRIMARY KEY,
    tip_no INTEGER NOT NULL,
    tag_no INTEGER NOT NULL
);

-- Oauth2Providers Table
CREATE TABLE oauth2_providers (
    no SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    activation BOOLEAN DEFAULT TRUE NOT NULL
);

-- UserOAuthConnections Table
CREATE TABLE user_oauth_connections (
    no SERIAL PRIMARY KEY,
    oauth2_user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    provider_no INTEGER NOT NULL,
    user_no INTEGER NOT NULL
);

-- UserCredentials Table
CREATE TABLE user_credentials (
    no SERIAL PRIMARY KEY,
    user_no INTEGER NOT NULL,
    id VARCHAR(50) NOT NULL,
    pw VARCHAR(255) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);