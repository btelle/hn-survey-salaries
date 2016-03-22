from __future__ import print_function
import httplib2
import os
import sys
import pandas
import sqlalchemy, psycopg2

# Download CSV file here: https://docs.google.com/feeds/download/spreadsheets/Export?docID=1a1Df6dg2Pby1UoNlZU2l0FEykKsQKttu7O6q7iQd2bU&exportFormat=csv
sheet_url = './salaries.csv'
db = sqlalchemy.create_engine('postgresql://localhost:5432/brandontelle')
db.engine.execute("DROP TABLE IF EXISTS public.salary_staging;")

if __name__ == '__main__':
	dataframe = pandas.read_csv(sheet_url, header=0, names=['ts', 'employer', 'location', 'job_title', 'employer_experience_years', 'total_experience_years', 'annual_base_pay', 'signing_bonus', 'annual_bonus', 'stock_value_bonus', 'gender', 'comments'])

	for row in dataframe.itertuples():
		# Do some validation?

	dataframe.to_sql('salary_staging', db, index_label='id')

