-- Timestamp,Employer,Location,Job Title,Years at Employer,Years of Experience,Annual Base Pay,
-- Signing Bonus,Annual Bonus,Annual Stock Value/Bonus,Gender,Additional Comments

DROP VIEW salaries_v;
DROP TABLE salaries;
DROP TABLE employers;
DROP TABLE locations;
DROP TABLE job_titles;
DROP TYPE job_category_type;
DROP TYPE gender_type;

CREATE TYPE gender_type AS ENUM('Male', 'Female', 'Other');
CREATE TYPE job_category_type as ENUM('Management', 'Data', 'Web', 'Engineering', 'Software', 'Operations', 'Applied Science', 'Other')

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
	location_country CHAR(2) DEFAULT NULL,
	location_latitude DECIMAL(6, 2) DEFAULT NULL,
	location_longitude DECIMAL(6, 2) DEFAULT NULL
);

CREATE TABLE job_titles
(
	job_title_key SERIAL PRIMARY KEY,
	job_title VARCHAR(255),
	job_title_category job_category_type,
	job_title_rank VARCHAR(50)
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

CREATE VIEW salaries_v AS
	SELECT
		salary_id,
		employers.employer_name,
		locations.location_name,
		locations.location_city,
		locations.location_state,
		locations.location_country,
		locations.location_latitude,
		locations.location_longitude,
		job_titles.job_title,
		job_titles.job_title_category,
		job_titles.job_title_rank,
		total_experience_years,
		employer_experience_years,
		annual_base_pay,
		signing_bonus,
		annual_bonus,
		stock_value_bonus,
		comments,
		submitted_at
	FROM salaries
		INNER JOIN employers ON salaries.employer_key = employers.employer_key
		INNER JOIN locations ON salaries.location_key = locations.location_key
		INNER JOIN job_titles ON salaries.job_title_key = job_titles.job_title_key;
