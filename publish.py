import psycopg2, sqlalchemy, pandas

db = sqlalchemy.create_engine('postgresql://localhost:5432/brandontelle')
df = pandas.read_sql_query('select * from salaries_v order by salary_id',con=db)
df.to_csv('data/salaries_clean.csv')

db.dispose()