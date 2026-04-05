CREATE OR REPLACE VIEW v_earthquakes_refined AS
WITH base_data AS (
    SELECT
        id,
        magnitude,
        place,
        TO_TIMESTAMP(time_epoch/1000.0) AT TIME ZONE 'UTC' AS event_time,
        longitude,
        latitude,
        depth
    FROM raw_earthquakes
),
location_parsing AS (
    SELECT *,
    TRIM(SPLIT_PART(place, ',',2)) AS region
    FROM base_data
)
SELECT * FROM location_parsing;

CREATE OR REPLACE VIEW v_quake_analytics AS
SELECT
    id,
    event_time,
    region,
    magnitude,
    RANK() OVER (
        PARTITION BY region
        ORDER BY magnitude DESC
    ) as rank_magnitude_region,
    AVG(magnitude) OVER (
        ORDER BY event_time
        ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
    ) as moving_avg_magnitude,
    event_time - LAG(event_time) OVER (ORDER BY event_time) AS time_since_last_quake
FROM v_earthquakes_refined;