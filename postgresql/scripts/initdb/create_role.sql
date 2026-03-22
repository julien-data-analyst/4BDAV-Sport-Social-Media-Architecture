-- Création des groupes
CREATE ROLE "SENSOR" NOLOGIN;
CREATE ROLE "SOCIAL_MEDIA_USER" NOLOGIN;
CREATE ROLE "DATA_ANALYST" NOLOGIN;
CREATE ROLE "ANALYSE_PERFORMANCE" NOLOGIN;
CREATE ROLE "MAINTENEUR_BDD" NOLOGIN;

-- Ecriture uniquement
GRANT INSERT ON TABLE 
"public"."Activity",
"public"."Activity_Aggregation_Metrics",
"public"."Sensors_Metrics_Activities"
TO "SENSOR";

-- Lecture uniquement
GRANT SELECT ON TABLE
"public"."Aggregation",
"public"."Aggregation_Metric",
"public"."Apparatus",
"public"."Sensor",
"public"."Sensors_Apparatus",
"public"."Sensors_Metrics",
"public"."Sport",
"public"."Sports_Metrics",
"public"."User",
"public"."User_Sports"
TO "SENSOR";

-- Lecture seule
GRANT SELECT ON TABLE
"public"."User",
"public"."Sport",
"public"."Activity"
TO "SOCIAL_MEDIA_USER";

-- Lecture + écriture + modification
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE
"public"."Follow",
"public"."Media",
"public"."Post",
"public"."Professionnal",
"public"."User_Sports",
"public"."Commentary",
"public"."Like"
TO "SOCIAL_MEDIA_USER";

-- Lecture seulement sur toutes les tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "DATA_ANALYST";

-- Pour les mainteneurs de la BDD
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "MAINTENEUR_BDD";

-- Pour les analyseurs de performances sportives
GRANT SELECT ON TABLE
"public"."Activity",
"public"."Activity_Aggregation_Metrics",
"public"."Sensors_Metrics_Activities",
"public"."Aggregation",
"public"."Aggregation_Metric",
"public"."Apparatus",
"public"."Sensor",
"public"."Sensors_Apparatus",
"public"."Sensors_Metrics",
"public"."Sport",
"public"."Sports_Metrics",
"public"."User",
"public"."User_Sports"
TO "ANALYSE_PERFORMANCE";

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;

-- SENSOR user
CREATE USER sensor_user WITH PASSWORD 'Sensor123!';
GRANT "SENSOR" TO sensor_user;

-- SOCIAL MEDIA USER
CREATE USER social_user WITH PASSWORD 'Social123!';
GRANT "SOCIAL_MEDIA_USER" TO social_user;

-- DATA ANALYST
CREATE USER analyst_user WITH PASSWORD 'Analyst123!';
GRANT "DATA_ANALYST" TO analyst_user;

-- ANALYSE PERFORMANCE
CREATE USER perf_user WITH PASSWORD 'Perf123!';
GRANT "ANALYSE_PERFORMANCE" TO perf_user;

-- MAINTENEUR
CREATE USER mainteneur_user WITH PASSWORD 'Mainteneur123!';
GRANT "MAINTENEUR_BDD" TO mainteneur_user;

