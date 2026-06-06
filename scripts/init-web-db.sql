-- Create the web dashboard database alongside the existing litellm database.
-- This script runs on first postgres startup via docker-entrypoint-initdb.d.
SELECT 'CREATE DATABASE pandora_web OWNER pandora'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'pandora_web')\gexec
