import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from test import api_key
# Installiere die erforderlichen Python-Pakete, falls noch nicht installiert:
# pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

def get_playlist_videos(api_key, playlist_id):
    # Authentifizierung und Erstellung des YouTube Data API-Clients
    api_service_name = "youtube"
    api_version = "v3"
    
    # Authentifiziere dich mit deinem API-Schlüssel
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
    
    # Hole die Playlist-Items
    playlist_items = []
    nextPageToken = None
    
    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,  # Anzahl der Ergebnisse pro Abfrage (maximal 50)
            pageToken=nextPageToken
        )
        response = request.execute()
        
        # Füge die Videos zur Liste hinzu
        playlist_items.extend(response.get("items", []))
        
        # Überprüfe, ob es weitere Seiten gibt
        nextPageToken = response.get("nextPageToken")
        if not nextPageToken:
            break
    
    # Extrahiere die Video-IDs aus den Playlist-Items
    video_ids = [item["contentDetails"]["videoId"] for item in playlist_items]
    
    return video_ids

# Beispielaufruf der Funktion
if __name__ == "__main__":
    
    playlist_id = "LL"
    
    video_ids = get_playlist_videos(api_key, playlist_id)
    
    print("Video-IDs in der Playlist:")
    for video_id in video_ids:
        print(video_id)
