.import --csv datasets/PA22.csv bridges
ALTER TABLE bridges ADD COLUMN latitude REAL;
ALTER TABLE bridges ADD COLUMN longitude REAL;
UPDATE bridges
SET latitude = CAST(SUBSTR(LAT_016, 1, 2) AS REAL) +
               CAST(SUBSTR(LAT_016, 3, 2) AS REAL) / 60 +
               CAST(SUBSTR(LAT_016, 5) AS REAL) / 360000,
    longitude = -(CAST(SUBSTR(LONG_017, 1, 3) AS REAL) +
                  CAST(SUBSTR(LONG_017, 4, 2) AS REAL) / 60 +
                  CAST(SUBSTR(LONG_017, 6) AS REAL) / 360000);
