-- Create the pandora_web database used by the Web dashboard.
--
-- Postgres auto-runs files in /docker-entrypoint-initdb.d/ on first startup
-- (only when data volume is empty). This ensures pandora_web exists
-- alongside the litellm database created by POSTGRES_DB.
--
-- To apply to an existing deployment without data loss, create the DB
-- manually: `docker exec pandora-postgres psql -U pandora -c "CREATE DATABASE pandora_web;"`

CREATE DATABASE pandora_web;
GRANT ALL PRIVILEGES ON DATABASE pandora_web TO pandora;
