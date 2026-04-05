CREATE TABLE IF NOT EXISTS daily_earthquake_summary(
    report_date DATE PRIMARY KEY,
    total_events INT,
    max_magnitude FLOAT,
    most_active_region TEXT
);

CREATE OR REPLACE PROCEDURE ps_generate_daily_report()
LANGUAGE plpgsql
AS $$
BEGIN 
    INSERT INTO daily_earthquake_summary (report_date, total_events, max_magnitude, most_active_region)
    SELECT
        CURRENT_DATE,
        COUNT(*),
        MAX(magnitude),
        (SELECT region 
         FROM v_earthquakes_refined
         WHERE event_time >= CURRENT_DATE -INTERVAL '1 day'
         GROUP BY region 
         ORDER BY COUNT(*) DESC 
         LIMIT 1)
    FROM v_earthquakes_refined
    WHERE event_time >= CURRENT_DATE - INTERVAL '1 day'
    ON CONFLICT (report_date) DO UPDATE
    SET total_events = EXCLUDED.total_events,
        max_magnitude = EXCLUDED.max_magnitude,
        most_active_region = EXCLUDED.most_active_region;

    COMMIT;
    RAISE NOTICE 'Reporte diario generado con exito';
END;
$$;