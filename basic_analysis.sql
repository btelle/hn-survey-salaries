-- Average salary across job category and title rank
SELECT 
	AVG(annual_base_pay+coalesce(annual_bonus, 0))::decimal(12, 2) as 'avg_annual_pay', 
	COUNT(*) as 'total_salaries', 
	job_title_category, 
	job_title_rank 
FROM salaries_v 
WHERE 
	job_title_category <> 'Other' 
	AND location_country='US' 
GROUP BY job_title_category, job_title_rank 
ORDER BY AVG(annual_base_pay+coalesce(annual_bonus, 0)) DESC;

-- Pay amount per total years worked vs pay amount per years at current job
-- Much higher base_pay_dollars_per_year_at_current_job indicates higher relative starting salaries
SELECT 
	job_title_category, 
	avg(annual_base_pay) / avg(total_experience_years) as base_pay_dollars_per_year_worked, 
	avg(annual_base_pay) / avg(employer_experience_years) as base_pay_dollars_per_year_at_current_job 
FROM salaries_v 
WHERE 
	job_title_category <> 'Other' 
	AND location_country='US' 
GROUP BY job_title_category 
ORDER BY base_pay_dollars_per_year_worked DESC;

-- Partition salary by total years exp to see raise trends
SELECT avg(annual_base_pay),
	job_title_category, 
	case when total_experience_years >= 0 and total_experience_years <=2 then '0-2'
		 when total_experience_years > 2 and total_experience_years <= 4 then '3-4'
		 when total_experience_years > 4 and total_experience_years <= 7 then '5-7'
		 when total_experience_years > 7 then '8+' end as experience_partition
FROM salaries_v
WHERE job_title_category <> 'Other'
	and total_experience_years IS NOT NULL
	and location_country = 'US'
GROUP BY job_title_category, experience_partition
ORDER BY job_title_category, experience_partition;

-- Most popular cities
SELECT 
	case 
		when location_state IS NOT NULL then location_city|| ', ' || location_state 
		else location_city end 
		as location, 
	COUNT(*) 
FROM salaries_v 
WHERE location_city IS NOT NULL 
GROUP BY location_city, location_state 
HAVING COUNT(*) > 1 
ORDER BY COUNT(*) DESC ;

-- Average "youth" of a company
SELECT 
	employer_name, 
	avg(employer_experience_years) 
FROM salaries_v 
WHERE employer_name IS NOT NULL 
GROUP BY employer_name 
HAVING COUNT(*) > 4 
ORDER BY avg(employer_experience_years) desc;
