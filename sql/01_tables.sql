CREATE TABLE IF NOT EXISTS raw_earthquakes(
    id VARCHAR(50) PRIMARY KEY,
    magnitude FLOAT,
    place VARCHAR(255),
    time_epoch BIGINT,
    update_epoch BIGINT,
    longitude FLOAT,
    latitude FLOAT,
    depth FLOAT,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS daily_earthquake_summary(
    report_date DATE PRIMARY KEY,
    total_events INT,
    max_magnitude FLOAT,
    most_active_region TEXT
);