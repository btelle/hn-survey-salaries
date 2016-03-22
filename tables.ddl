-- Timestamp,Employer,Location,Job Title,Years at Employer,Years of Experience,Annual Base Pay,
-- Signing Bonus,Annual Bonus,Annual Stock Value/Bonus,Gender,Additional Comments

DROP TABLE IF EXISTS salary_staging;
DROP TABLE salaries;
DROP TABLE employers;
DROP TABLE locations;
DROP TABLE job_titles;
DROP TYPE gender_type;

CREATE TYPE gender_type AS ENUM('Male', 'Female', 'Other');

-- Staging table
CREATE TABLE salary_staging
(
	id INT NOT NULL PRIMARY KEY,
	ts TIMESTAMP NOT NULL,
	employer VARCHAR(255) DEFAULT NULL,
	location VARCHAR(255) DEFAULT NULL,
	job_title VARCHAR(255) DEFAULT NULL,
	total_experience_years INT DEFAULT NULL,
	employer_experience_years INT DEFAULT NULL,
	annual_base_pay DECIMAL(12, 2) DEFAULT NULL,
	signing_bonus DECIMAL(12, 2) DEFAULT NULL,
	annual_bonus DECIMAL(12, 2) DEFAULT NULL,
	stock_value_bonus DECIMAL(12, 2) DEFAULT NULL,
	gender gender_type DEFAULT 'Other',
	comments TEXT
);

-- Dimensions
CREATE TABLE employers
(
	employer_key SERIAL PRIMARY KEY,
	employer_name VARCHAR(255)
);

CREATE TABLE locations
(
	location_key SERIAL PRIMARY KEY,
	location_name VARCHAR(255) NOT NULL,
	location_city VARCHAR(255) DEFAULT NULL,
	location_state CHAR(2) DEFAULT NULL,
	location_country CHAR(2) DEFAULT NULL
);

CREATE TABLE job_titles
(
	job_title_key SERIAL PRIMARY KEY,
	job_title VARCHAR(255)
);

-- Salaries table
CREATE TABLE salaries 
(
	salary_id INT NOT NULL PRIMARY KEY,
	submitted_at TIMESTAMP NOT NULL,
	employer_key INT REFERENCES employers DEFAULT NULL,
	location_key INT REFERENCES locations DEFAULT NULL,
	job_title_key INT REFERENCES job_titles DEFAULT NULL,
	total_experience_years DECIMAL(6, 2) DEFAULT NULL,
	employer_experience_years DECIMAL(6, 2) DEFAULT NULL,
	annual_base_pay DECIMAL(12, 2) DEFAULT NULL,
	signing_bonus DECIMAL(12, 2) DEFAULT NULL,
	annual_bonus DECIMAL(12, 2) DEFAULT NULL,
	stock_value_bonus VARCHAR(255) DEFAULT NULL,
	gender gender_type DEFAULT 'Other',
	comments TEXT
);