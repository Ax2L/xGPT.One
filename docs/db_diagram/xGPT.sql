CREATE TABLE "DevelopmentSteps" (
  "id" serial PRIMARY KEY,
  "app" integer,
  "previous_step" integer,
  "high_level_step" varchar,
  "messages" text,
  "llm_response" jsonb,
  "prompt_path" text,
  "prompt_data" jsonb,
  "llm_req_num" integer,
  "token_limit_exception_raised" boolean
);

CREATE TABLE "CommandRuns" (
  "id" serial PRIMARY KEY,
  "app" integer,
  "previous_step" integer,
  "high_level_step" varchar,
  "command" text,
  "cli_response" jsonb
);

CREATE TABLE "UserInputs" (
  "id" serial PRIMARY KEY,
  "app" integer,
  "previous_step" integer,
  "high_level_step" varchar,
  "query" text,
  "user_input" text
);

CREATE TABLE "UserApps" (
  "id" serial PRIMARY KEY,
  "app_name" varchar,
  "user_id" integer
);

CREATE TABLE "File" (
  "id" serial PRIMARY KEY,
  "app" integer,
  "path" varchar,
  "name" varchar,
  "description" text
);

CREATE TABLE "FileSnapshot" (
  "id" serial PRIMARY KEY,
  "file_id" integer,
  "snapshot_time" timestamp
);

CREATE TABLE "Users" (
  "id" serial PRIMARY KEY,
  "username" varchar UNIQUE,
  "hashed_password" varchar,
  "email" varchar UNIQUE,
  "display_name" varchar,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "UserAPIKeys" (
  "id" serial PRIMARY KEY,
  "user_id" integer,
  "openai_key" varchar,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "UserSettings" (
  "id" serial PRIMARY KEY,
  "user_id" integer,
  "theme" varchar,
  "language" varchar,
  "notification_preference" boolean,
  "created_at" timestamp,
  "updated_at" timestamp
);

ALTER TABLE "UserApps" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "UserAPIKeys" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "UserSettings" ADD FOREIGN KEY ("user_id") REFERENCES "Users" ("id");

ALTER TABLE "DevelopmentSteps" ADD FOREIGN KEY ("previous_step") REFERENCES "DevelopmentSteps" ("id");

ALTER TABLE "CommandRuns" ADD FOREIGN KEY ("previous_step") REFERENCES "CommandRuns" ("id");

ALTER TABLE "UserInputs" ADD FOREIGN KEY ("previous_step") REFERENCES "UserInputs" ("id");

ALTER TABLE "FileSnapshot" ADD FOREIGN KEY ("file_id") REFERENCES "File" ("id");

ALTER TABLE "DevelopmentSteps" ADD FOREIGN KEY ("app") REFERENCES "UserApps" ("id");

ALTER TABLE "CommandRuns" ADD FOREIGN KEY ("app") REFERENCES "UserApps" ("id");

ALTER TABLE "UserInputs" ADD FOREIGN KEY ("app") REFERENCES "UserApps" ("id");
