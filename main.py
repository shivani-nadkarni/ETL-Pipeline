import requests
import datetime
import pandas as pd
import json
from io import StringIO
import sqlalchemy
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
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    print(yesterday)
    
    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, "%Y-%m-%d") != yesterday:
            raise Exception("At least one of the returned songs are not from yesterday") 

# main 
if __name__ == "__main__":
	# authorisation token from spotify
	TOKEN = "BQA9xBaVA8nAyK4eZZAzq4uXyJ0DB1lxRAkVAZsf5OY6HumZ_eryNRT6plAcfPq5oGHmRJY9O04S904NyzKrriBQqawek3eT33i6EmJyJwaSTtaihPMu7fj3d6jA9tSto5sNfVXmFTkYF1C2or721eK16SSOH4Cqdvs_FbHB"
	DATABASE_LOCATION = "sqlite:///songs.db"
	headers = {
		"Accept" : "application/json",
		"Content-Type" : "application/json",
		"Authorization" : "Bearer {token}".format(token = TOKEN)
	}

	# converting date to epoch milliseconds
	today = datetime.datetime.now()
	yesterday = today - datetime.timedelta(days=1)

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
	#check_if_valid_data(song_df)

	# Load stage

	# create an Sql Connection to our SQLite Database
	engine = sqlalchemy.create_engine(DATABASE_LOCATION)

	conn = engine.connect()

	print(connected succesfully)

	## query = ......
	## conn.execute(query)

