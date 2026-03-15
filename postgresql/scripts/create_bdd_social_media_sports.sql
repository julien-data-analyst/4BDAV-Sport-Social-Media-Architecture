CREATE TABLE IF NOT EXISTS "User" (
	"id" TEXT NOT NULL UNIQUE,
	"firstname" TEXT NOT NULL,
	"lastname" TEXT NOT NULL,
	"created_date" TIMESTAMP NOT NULL,
	"description" TEXT NOT NULL,
	"email" TEXT NOT NULL,
	"password" TEXT NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Sport" (
	"id" TEXT NOT NULL UNIQUE,
	"name" TEXT NOT NULL,
	"description" TEXT NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Activity" (
	"id" TEXT NOT NULL UNIQUE,
	"beginning_date" TIMESTAMP NOT NULL,
	"ending_date" TIMESTAMP NOT NULL,
	"commentary" TEXT,
	"id_user_sport" TEXT NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Post" (
	"id" TEXT NOT NULL UNIQUE,
	"id_activity" TEXT,
	"upload_date" TIMESTAMP NOT NULL,
	"modified_date" TIMESTAMP,
	"content" TEXT NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Activity_Aggregation_Metrics" (
	"id" TEXT NOT NULL UNIQUE,
	"id_activity" TEXT NOT NULL,
	"id_aggregation_metric" TEXT NOT NULL,
	"value" NUMERIC NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Metric" (
	"id" TEXT NOT NULL UNIQUE,
	"name" TEXT NOT NULL,
	"unity" VARCHAR(10) NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	"formula" TEXT,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Like" (
	"id" TEXT NOT NULL UNIQUE,
	"id_user_posted" TEXT NOT NULL,
	"id_post_liked" TEXT NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	"like" BOOLEAN NOT NULL,
	"modified_date" TIMESTAMP,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Commentary" (
	"id" TEXT NOT NULL UNIQUE,
	"id_user_writer" TEXT NOT NULL,
	"id_post" TEXT NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	"content" TEXT NOT NULL,
	"id_commentary_response" TEXT,
	"modified_date" TIMESTAMP,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Follow" (
	"id" TEXT NOT NULL UNIQUE,
	"id_user_follower" TEXT NOT NULL,
	"id_user_sport_followed" TEXT NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Media" (
	"id" TEXT NOT NULL UNIQUE,
	"URL" TEXT NOT NULL,
	"id_post" TEXT NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "User_Sports" (
	"id" TEXT NOT NULL UNIQUE,
	"user_id" TEXT NOT NULL,
	"sport_id" TEXT NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Professionnal" (
	"id" TEXT NOT NULL UNIQUE,
	"user_sport_id" TEXT NOT NULL,
	"title" TEXT NOT NULL,
	"description" TEXT,
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Sports_Metrics" (
	"id" TEXT NOT NULL UNIQUE,
	"sport_id" TEXT NOT NULL,
	"metric_id" TEXT NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Sensor" (
	"id" TEXT NOT NULL UNIQUE,
	"name" TEXT NOT NULL,
	"type" TEXT NOT NULL,
	"formula" TEXT,
	"unity" VARCHAR(10),
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Apparatus" (
	"id" TEXT NOT NULL UNIQUE,
	"name" TEXT NOT NULL,
	"type" TEXT NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Sensors_Apparatus" (
	"id" TEXT NOT NULL UNIQUE,
	"sensor_id" TEXT NOT NULL,
	"apparatus_id" TEXT NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Sensors_Activities" (
	"id" TEXT NOT NULL UNIQUE,
	"activity_id" TEXT NOT NULL,
	"sensor_id" TEXT NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Aggregation" (
	"id" TEXT NOT NULL UNIQUE,
	"name" TEXT NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Aggregation_Metric" (
	"id" TEXT NOT NULL UNIQUE,
	"name" TEXT NOT NULL,
	"id_metric" TEXT NOT NULL,
	"id_aggregation" TEXT NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);




CREATE TABLE IF NOT EXISTS "Sensors_Metrics" (
	"id" TEXT NOT NULL UNIQUE,
	"id_sensor" TEXT NOT NULL,
	"id_metric" TEXT NOT NULL,
	"upload_date" TIMESTAMP NOT NULL,
	PRIMARY KEY("id")
);



ALTER TABLE "Post"
ADD FOREIGN KEY("id_activity") REFERENCES "Activity"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Activity_Aggregation_Metrics"
ADD FOREIGN KEY("id_activity") REFERENCES "Activity"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Like"
ADD FOREIGN KEY("id_user_posted") REFERENCES "User"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Like"
ADD FOREIGN KEY("id_post_liked") REFERENCES "Post"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Commentary"
ADD FOREIGN KEY("id_user_writer") REFERENCES "User"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Commentary"
ADD FOREIGN KEY("id_post") REFERENCES "Post"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Media"
ADD FOREIGN KEY("id_post") REFERENCES "Post"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Follow"
ADD FOREIGN KEY("id_user_follower") REFERENCES "User"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Activity"
ADD FOREIGN KEY("id_user_sport") REFERENCES "User_Sports"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "User_Sports"
ADD FOREIGN KEY("user_id") REFERENCES "User"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "User_Sports"
ADD FOREIGN KEY("sport_id") REFERENCES "Sport"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Commentary"
ADD FOREIGN KEY("id_commentary_response") REFERENCES "Commentary"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Professionnal"
ADD FOREIGN KEY("user_sport_id") REFERENCES "User_Sports"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Follow"
ADD FOREIGN KEY("id_user_sport_followed") REFERENCES "User_Sports"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Sports_Metrics"
ADD FOREIGN KEY("metric_id") REFERENCES "Metric"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Sports_Metrics"
ADD FOREIGN KEY("sport_id") REFERENCES "Sport"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Sensors_Apparatus"
ADD FOREIGN KEY("apparatus_id") REFERENCES "Apparatus"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Sensors_Apparatus"
ADD FOREIGN KEY("sensor_id") REFERENCES "Sensor"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Sensors_Activities"
ADD FOREIGN KEY("activity_id") REFERENCES "Activity"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Sensors_Activities"
ADD FOREIGN KEY("sensor_id") REFERENCES "Sensor"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Activity_Aggregation_Metrics"
ADD FOREIGN KEY("id_aggregation_metric") REFERENCES "Aggregation_Metric"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Aggregation_Metric"
ADD FOREIGN KEY("id_aggregation") REFERENCES "Aggregation"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Aggregation_Metric"
ADD FOREIGN KEY("id_metric") REFERENCES "Metric"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Sensors_Metrics"
ADD FOREIGN KEY("id_sensor") REFERENCES "Sensor"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;
ALTER TABLE "Sensors_Metrics"
ADD FOREIGN KEY("id_metric") REFERENCES "Metric"("id")
ON UPDATE NO ACTION ON DELETE NO ACTION;