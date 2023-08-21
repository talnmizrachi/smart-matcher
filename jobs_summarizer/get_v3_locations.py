import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import psycopg2

load_dotenv()


def get_locations_data():
	engine = create_engine(os.getenv("DATABASE_URL"))
	query = 'SELECT token, country, state, city,preference_location FROM v3_students'
	df = pd.read_sql(query, con=engine, index_col='token')

	return df


def get_location_dict():
	return {
		"My country": "country"
		, "My state": "state"
		, "My city": "city"
	}


def data_preprocessor(df_):
	pref_ = df_['preference_location'].str.split(", ").explode()

	df_for_iter_ = df_.join(pref_.to_frame().fillna(""), on=df_.index, lsuffix="_", rsuffix="__")[
		["country", "state", "city", 'preference_location__']].copy()
	df_for_iter_ = df_for_iter_[df_for_iter_['preference_location__'] != 'Remote'].copy()

	return pref_, df_for_iter_


def value_formatter(val: str):
	return val.capitalize()


def add_locations(df_for_iter_, preference):
	locations = ["Remote"] if "Remote" in preference.values else []
	location_dict = get_location_dict()

	for token, row in df_for_iter_.iterrows():
		country, state, city, preference = row[['country', 'state', "city", 'preference_location__']].values

		if preference.lower() == 'my country':
			value = value_formatter(country)
		elif preference.lower() == 'my state' and state is not None:
			value = value_formatter(state)
		elif preference.lower() == 'my city':
			value = value_formatter(city)
		else:
			value = value_formatter(preference)

		if value not in locations:
			locations.append(value)

	return locations


def main():
	df = get_locations_data()
	pref, df_for_iter = data_preprocessor(df)
	locations = add_locations(df_for_iter, pref)

	return locations


if __name__ == "__main__":
	main()
