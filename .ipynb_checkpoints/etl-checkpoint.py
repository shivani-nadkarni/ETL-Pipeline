{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "id": "iHAjUTaOKGRb"
   },
   "outputs": [],
   "source": [
    "import requests\n",
    "import datetime\n",
    "import pandas as pd\n",
    "import json\n",
    "from io import StringIO"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "id": "1BxA3sBAKRD4"
   },
   "outputs": [],
   "source": [
    "TOKEN = \"BQA83XUZLhuWEgqT52eNWwJO6YQ5BuHm2L4AzxknyN4lOp5af5-KFps-ZcLrhCG-56ygBoqiv7OUaGIhC7RTXJFOX9gRcyENzsRmuAuguZoL_IxNtk9rH_H4-3sa7-kI5m7AYE8M_cGO99iEksWagcKAu3bLQiZXZ7O4Ogr3\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "id": "5HC0TDy9KYjt"
   },
   "outputs": [],
   "source": [
    "headers = {\n",
    "\t\t\"Accept\" : \"application/json\",\n",
    "\t\t\"Content-Type\" : \"application/json\",\n",
    "\t\t\"Authorization\" : \"Bearer {token}\".format(token = TOKEN)\n",
    "\t}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "id": "yICfKwSQKbEw"
   },
   "outputs": [],
   "source": [
    "today = datetime.datetime.now()\n",
    "yesterday = today - datetime.timedelta(days=1)\n",
    "yesterday_in_unix = int(yesterday.timestamp()*1000)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# making the API call and storing the response\n",
    "r = requests.get(\"https://api.spotify.com/v1/me/player/recently-played?after={time}\".format(time=yesterday_in_unix), headers=headers)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'items': [], 'next': None, 'cursors': None, 'limit': 20, 'href': 'https://api.spotify.com/v1/me/player/recently-played?after=1635687454319'}\n"
     ]
    }
   ],
   "source": [
    "# print the ouput \n",
    "print(r.json())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# replace the single quotes with double quotes\n",
    "response = r.text.replace(\"'\", '\"')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "response = r.json()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'items': [], 'next': None, 'cursors': None, 'limit': 20, 'href': 'https://api.spotify.com/v1/me/player/recently-played?after=1635687454319'}\n"
     ]
    }
   ],
   "source": [
    "# reprint the output\n",
    "print(response)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "dict"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "type(response)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "song_names = []\n",
    "artists = []\n",
    "played_at = []\n",
    "timestamp = []"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {
    "id": "I2quWVxrQrhR"
   },
   "outputs": [],
   "source": [
    "for song in response['items']:\n",
    "    artists.append(song['track']['album']['artists'][0]['name'])\n",
    "    song_names.append(song['track']['album']['name'])\n",
    "    played_at.append(song['played_at'])\n",
    "    timestamp.append(song['played_at'][:10])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[]\n"
     ]
    }
   ],
   "source": [
    "print(artists)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[]\n"
     ]
    }
   ],
   "source": [
    "print(song_names)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[]\n"
     ]
    }
   ],
   "source": [
    "print(timestamp)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "songs_dict = {\n",
    "    \"song_name\" : song_names,\n",
    "    \"artists\" : artists,\n",
    "    \"played_at\" : played_at,\n",
    "    \"timestamp\" : timestamp\n",
    "}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'song_name': [], 'artists': [], 'played_at': [], 'timestamp': []}\n"
     ]
    }
   ],
   "source": [
    "print(songs_dict)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [],
   "source": [
    "song_df = pd.DataFrame(songs_dict, columns = [\"song_name\", \"artists\", \"played_at\", \"timestamp\"])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Empty DataFrame\n",
      "Columns: [song_name, artists, played_at, timestamp]\n",
      "Index: []\n"
     ]
    }
   ],
   "source": [
    "print(song_df)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [],
   "source": [
    "def check_if_valid_data(df: pd.DataFrame) -> bool:\n",
    "    # check if dataframe is empty\n",
    "    if df.empty:\n",
    "        print(\"No songs downloaded.\")\n",
    "        return False\n",
    "    \n",
    "    # primary key check\n",
    "    if pd.Series(df['played_at']).is_unique:\n",
    "        pass\n",
    "    else:\n",
    "        raise Exception(\"Primary Key check is violated.\")\n",
    "        \n",
    "    # Check for null values\n",
    "    if df.isnull().values.any():\n",
    "        raise Exception(\"Null value found.\")\n",
    "        \n",
    "    # check if songs are of yesterday's date\n",
    "    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)\n",
    "    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)\n",
    "    \n",
    "    timestamps = df[\"timestamp\"].tolist()\n",
    "    for timestamp in timestamps:\n",
    "        if datetime.datetime.strptime\n",
    "    \n",
    "    \n",
    "    \n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "colab": {
   "name": "ETL",
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}
