-- init.sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS tip_data (
                                        id SERIAL PRIMARY KEY,
                                        content TEXT,
                                        embedding vector(1536)
    );
