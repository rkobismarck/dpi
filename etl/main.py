
import spotipy
import pandas as pd
import json 

from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from cfg import CLIENT_ID,CLIENT_SECRET,SPOTIFY_REDIRECT_URI,DB_CONNSTR


def extract():
    '''
        -- Running extraction process --
    '''
    ds = int((datetime.today() - timedelta(days=1)).timestamp()) * 1000
    return sp.current_user_recently_played(limit=20, after=ds)

def transform(raw_data):
    '''
        -- Running transformation process --
    '''
    data = []
    for row in raw_data:
        data.append(
            {
                "played_at" :row["played_at"],
                "artist_name" :row["track"]["artists"][0]["name"],
                "song_name" :row["track"]["name"]
            }
        )
    return pd.DataFrame(data)

def load(df_data):
    '''
        -- Running loading process --
    '''
    engine = create_engine(DB_CONNSTR)
    df_data.to_sql('my_played_tracks', con=engine, index=False, if_exists='append')

def main():   
    # Extract
    spotify_raw_data = extract()
    
    # Transform (Clean-Filter-Enrich)
    clean_df = transform(spotify_raw_data['items'])

    # Load
    load(clean_df)

if __name__ == "__main__":

    scope="user-read-recently-played"

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth( 
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=scope
        )
    )
    
    main()