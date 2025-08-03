--create database
CREATE DATABASE fraud_detection;

--drop and create raw and clean layer schema
DO
$$
BEGIN
   IF EXISTS (
      SELECT 1 FROM information_schema.schemata WHERE schema_name = 'raw_layer'
   ) THEN
      EXECUTE 'DROP SCHEMA raw_layer CASCADE';
   END IF;

   IF EXISTS (
      SELECT 1 FROM information_schema.schemata WHERE schema_name = 'clean_layer'
   ) THEN
      EXECUTE 'DROP SCHEMA clean_layer CASCADE';
   END IF;

   CREATE SCHEMA raw_layer;
   CREATE SCHEMA clean_layer;
END
$$;


-- drop and recreate the transactions table in raw_layer schema
DO
$$
BEGIN
   IF EXISTS (
      SELECT FROM information_schema.tables 
      WHERE  table_schema = 'raw_layer'
      AND    table_name   = 'transactions'
   ) THEN
      EXECUTE 'DROP TABLE raw_layer.transactions CASCADE';
   END IF;

   EXECUTE '
   CREATE TABLE raw_layer.transactions (
       transaction_id        UUID PRIMARY KEY,
       user_id               UUID,
       transaction_timestamp TIMESTAMP,
       transaction_amount    NUMERIC(10, 2),
       merchant_id           TEXT,
       merchant_category     TEXT,
       payment_method        TEXT,
       ip_address            INET,
       geolocation           TEXT,
       device_id             TEXT,
       device_type           TEXT,
       transaction_type      TEXT,
       transaction_status    TEXT,
       is_fraud              BOOLEAN,
       risk_score            INT
   )';
END
$$;

