import sqlalchemy, psycopg2, re, pandas, math

# Download CSV file here: https://docs.google.com/feeds/download/spreadsheets/Export?docID=1a1Df6dg2Pby1UoNlZU2l0FEykKsQKttu7O6q7iQd2bU&exportFormat=csv
sheet_url = './salaries.csv'

def convert_currency(text):
	# convert foreign to USD
	conversion_rates = {
		'cad': 0.766,
		'eur': 1.12,
		'£': 1.422,
		'gbp': 1.422,
		'aud': 0.763
	}
	
	matches = re.search('([0-9\.]+)', text.replace(',', '').replace('k', '000'))

	if matches:
		try:
			amount = float(matches.group(1))
			for curr in conversion_rates:
				if curr in text:
					amount = amount * conversion_rates[curr]
			return amount
		except ValueError:
			pass
	return None


if __name__ == '__main__':
	db = sqlalchemy.create_engine('postgresql://localhost:5432/brandontelle')
	db.engine.execute("DROP TABLE IF EXISTS public.salary_staging;")

	dataframe = pandas.read_csv(sheet_url, header=0, names=['ts', 'employer', 'location', 'job_title', 'employer_experience_years', 'total_experience_years', 'annual_base_pay', 'signing_bonus', 'annual_bonus', 'stock_value_bonus', 'gender', 'comments'])

	for row in dataframe.itertuples():
		# employer
		if type(row[2]) is str:
			emp = row[2].lower().replace(',', '').replace('.com', '').replace('inc.', '').replace('inc', '').replace('corporation', '').replace('corp', '').replace('university', '').strip()
			dataframe.set_value(row[0], 'employer', emp)

		# years
		year_columns = {5: 'employer_experience_years', 6: 'total_experience_years'}
		for i in year_columns:
			if type(row[i]) is str:
				if 'year' in row[i].lower():
					dataframe.set_value(row[0], year_columns[i], row[i].lower().replace('years', '').replace('year', '').strip())
				
				if '+' in row[i] or '>' in row[i] or '<' in row[i]:
					dataframe.set_value(row[0], year_columns[i], row[i].lower().replace('+', '').replace('<', '').replace('>', '').strip())

		# currency
		currency_columns = {7: 'annual_base_pay', 8: 'signing_bonus', 9: 'annual_bonus'}
		for i in currency_columns:
			if type(row[i]) is str:
				dataframe.set_value(row[0], currency_columns[i], convert_currency(row[i].lower()))

		# gender
		if(type(row[11]) is not str or row[11].lower() not in ['male', 'female']):
			dataframe.set_value(row[0], 'gender', 'Other')

	for row in dataframe.itertuples():
		for r in [5,6,7,8,9]:
			try:
				float(row[r])
				if (r > 6 and float(row[r]) >= math.pow(10, 10)) or (r <= 6 and float(row[r]) >= 60):
					print(row)
					dataframe = dataframe.drop(row[0])
					break;

			except ValueError:
				print(row)
				dataframe = dataframe.drop(row[0])
				break
			except TypeError:
				pass


	dataframe.to_sql('salary_staging', db, index_label='id')
	db.dispose()
