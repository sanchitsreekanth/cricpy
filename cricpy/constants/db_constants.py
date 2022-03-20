class DBConstants:
    """Constants related to DB operations"""

    DB_NAME = "data/ipl.db"
    CREATE_MATCHES_TABLE_QUERY = """ CREATE TABLE IF NOT EXISTS matches (
        match_id int PRIMARY KEY,
        year integer NOT NULL,
        match_number integer NOT NULL,
        match_date text NOT NULL,
        venue text NOT NULL,
        city text NOT NULL,
        first_innings text NOT NULL,
        second_innings text NOT NULL,
        winner text NOT NULL,
        status text NOT NULL,
        toss text NOT NULL,
        mom text NOT NULL,
        rpo_1 text NOT NULL,
        rpo_2 text NOT NULL,
        fow_1 text NOT NULL,
        fow_2 text NOT NULL,
        fow_overs_1 text NOT NULL,
        fow_overs_2 text NOT NULL
        );"""
        
    CREATE_MATCH_ID_TABLE_QUERY = """ CREATE TABLE IF NOT EXISTS match_id (
        match_id int PRIMARY KEY,
        match_name text NOT NULL,
        series_id text NOT NULL,
        year int NOT NULL
    );"""
        
    
