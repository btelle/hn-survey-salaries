import psycopg2

update_employers = """
	INSERT INTO employers
	(
		employer_name
	)
	SELECT DISTINCT
		lower(trim(employer))
	FROM salary_staging
	WHERE lower(trim(employer)) NOT IN(SELECT employer_name FROM employers) and employer IS NOT NULL
	;"""

update_locations = """
	INSERT INTO locations
	(
		location_name
	)
	SELECT DISTINCT
		lower(trim(location))
	FROM salary_staging
	WHERE lower(trim(location)) NOT IN(SELECT location_name FROM locations) and location IS NOT NULL
	;"""

update_location_countries = """
	UPDATE locations SET
		location_country = cca2
	FROM
		countries
	where (locations.location_name LIKE '%' || LOWER(substring(name from 0 for position(',' in name))) || '%')
		AND location_country IS NULL
	;"""

update_location_states = """
	UPDATE locations SET
		location_state = abbreviation,
		location_country = 'US'
	FROM
		us_states
	WHERE (locations.location_name LIKE '%' || LOWER(us_states.name) || '%'
			OR locations.location_name LIKE '%, ' || LOWER(us_states.abbreviation) || '%'
			OR locations.location_name LIKE '% ' || LOWER(us_states.abbreviation))
		AND locations.location_state IS NULL AND locations.location_country IS NULL
	;"""

update_location_ca_states = """
	UPDATE locations SET
		location_state = abbreviation,
		location_country = 'CA'
	FROM
		ca_states
	WHERE (locations.location_name LIKE '%' || LOWER(ca_states.name) || '%'
			OR locations.location_name LIKE '%, ' || LOWER(ca_states.abbreviation) || '%'
			OR locations.location_name LIKE '% ' || LOWER(ca_states.abbreviation))
		AND locations.location_state IS NULL and locations.location_country IS NULL
	;"""

update_location_cities = """
	UPDATE locations SET
		location_city = nullif(substring(location_name from 0 for position(',' in location_name)), '')
	WHERE location_city IS NULL
	;"""

update_zip_codes = """
	UPDATE locations SET
		location_city = lower("City"),
		location_state="State",
		location_country='US'
	FROM zip_codes
	WHERE location_name="Zipcode"::VARCHAR
		AND location_city IS NULL
	;"""

update_lat_long_by_state = """
	UPDATE locations
		SET location_latitude="Lat",
			location_longitude="Long"
	FROM zip_codes
	WHERE location_city = lower("City") and location_state="State"
	;"""

update_lat_long_by_country = """
	UPDATE locations
		SET location_latitude = substring(latlng from 0 for position(',' in latlng))::decimal(6,2),
			location_longitude = substring(latlng from position(',' in latlng)+1)::decimal(6,2)
	FROM countries
	WHERE location_country = cca2 
		AND location_latitude IS NULL and location_longitude IS NULL
	;"""

update_job_titles = """
	INSERT INTO job_titles
	(
		job_title
	)
	SELECT DISTINCT
		lower(trim(job_title))
	FROM salary_staging
	WHERE lower(trim(job_title)) NOT IN(SELECT job_title FROM job_titles) and job_title IS NOT NULL
	;"""

insert_salaries = """
	INSERT INTO salaries
	(
		salary_id,
		employer_key,
		location_key,
		job_title_key,
		submitted_at,
		total_experience_years,
		employer_experience_years,
		annual_base_pay,
		signing_bonus,
		annual_bonus,
		stock_value_bonus,
		gender,
		comments
	)
	SELECT
		stg.id as salary_id,
		em.employer_key as employer_key,
		lo.location_key as location_key,
		jt.job_title_key as job_title_key,
		stg.ts::TIMESTAMP as submitted_at,
		stg.total_experience_years::DECIMAL(6,2),
		stg.employer_experience_years::DECIMAL(6,2),
		stg.annual_base_pay::DECIMAL(12,2),
		stg.signing_bonus::DECIMAL(12,2),
		stg.annual_bonus::DECIMAL(12,2),
		stg.stock_value_bonus,
		stg.gender::gender_type,
		stg.comments

	FROM salary_staging stg
		LEFT JOIN employers em ON lower(trim(stg.employer))=em.employer_name
		LEFT JOIN locations lo ON lower(trim(stg.location))=lo.location_name
		LEFT JOIN job_titles jt ON lower(trim(stg.job_title))=jt.job_title
	WHERE stg.id NOT IN (SELECT salary_id FROM salaries);
	;"""

with psycopg2.connect(host='localhost') as conn:
	with conn.cursor() as cur:
		cur.execute(update_employers)
		cur.execute(update_locations)
		cur.execute(update_location_countries)
		cur.execute(update_location_states)
		cur.execute(update_location_ca_states)
		cur.execute(update_location_cities)
		cur.execute(update_zip_codes)
		cur.execute(update_lat_long_by_state)
		cur.execute(update_lat_long_by_country)
		cur.execute(update_job_titles)
		cur.execute(insert_salaries)
