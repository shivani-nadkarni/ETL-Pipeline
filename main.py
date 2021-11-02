import requests
import datetime
import pandas as pd
import json
from io import StringIO
import sqlite3

def check_if_valid_data(df: pd.DataFrame) -> bool:
    # check if dataframe is empty
    if df.empty:
        print("No songs downloaded. Ending execution.")
        return False
    
    # primary key check
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated.")
        
    # Check for null values
    if df.isnull().values.any():
        raise Exception("Null value found.")
        
    # check if songs are of yesterday's date
    # yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    # yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    # print(yesterday)
    
    # timestamps = df["timestamp"].tolist()
    # for timestamp in timestamps:
    #     if datetime.datetime.strptime(timestamp, "%Y-%m-%d") != yesterday:
    #         raise Exception("At least one of the returned songs are not from yesterday") 

# main 
if __name__ == "__main__":
	# authorisation token from spotify
	TOKEN = "BQCz3SPIjEo9rarivqpOarIay9mNUFYdr3acEyy1n_KBWhuQXwHcWaeUQgUE_YE-ile5ff2zrqL5NtkUjAoceDM08Lk8-kAGqs_ZvgI_fFLyK-v9Q0FeNFux0iFZoq5hsRBMBjDiDd7bJ-uqXP-M7OnyscrDDSp_WwtiBLXk"
	DATABASE_LOCATION = "sqlite:///songs.db"
	TABLE_NAME = "my_played_tracks"

	headers = {
		"Accept" : "application/json",
		"Content-Type" : "application/json",
		"Authorization" : "Bearer {token}".format(token = TOKEN)
	}

	# converting date to epoch milliseconds
	today = datetime.datetime.now()
	yesterday = today - datetime.timedelta(days=60)

	yesterday_in_unix = int(yesterday.timestamp())

	print(yesterday_in_unix)

	# Spotify api call to fetch recently played songs
	r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_in_unix), headers=headers)

	# replace the single quotes with double quotes
	response = r.json()

	# List declarations
	song_names = []
	artists = []
	played_at = []
	timestamp = []

	# populate the lists
	for song in response["items"]:
	    artists.append(song['track']['album']['artists'][0]['name'])
	    song_names.append(song['track']['album']['name'])
	    played_at.append(song['played_at'])
	    timestamp.append(song['played_at'][:10])

	# create a dictionary containing the above lists    
	songs_dict = {
	    "song_name" : song_names,
	    "artists" : artists,
	    "played_at" : played_at,
	    "timestamp" : timestamp
	}
	# create dataframe
	song_df = pd.DataFrame(songs_dict, columns = ["song_name", "artists", "played_at", "timestamp"])

	print(song_df)
	# Validate spotify data
	check_if_valid_data(song_df)

	# Load stage

	# create a connection object - which represents the database
	conn = sqlite3.connect('songs.db')

	# Create the cursor object
	cursor = conn.cursor()

	# writing sql query to create the table
	sql_query = """
	CREATE TABLE IF NOT EXISTS my_played_tracks(
		song_name VARCHAR(200),
		artists VARCHAR(200),
		played_at VARCHAR(200),
		timestamp VARCHAR(200),
		CONSTRAINT primay_key_constraint PRIMARY KEY (played_at)
	)
	"""
	# execute the sql query to create a new table
	cursor.execute(sql_query)

	# save the dataframe to the database
	try:
		song_df.to_sql(TABLE_NAME, conn, index=False, if_exists="append")
	except Exception as e:
		print(e)

	# commit and close the database connection
	conn.commit()
	conn.close()

	print("Connection closed succesfully.")

	## query = ......
	## conn.execute(query)

