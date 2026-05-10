import os
import json
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'google_key.json'
DRIVE_FOLDER_ID = '16utXW3zldC_eX5CphTDGjxdZfl8pag4E'
LOCAL_MUSIC_DIR = Path(__file__).parent / 'music'
PLAYLIST_FILE = Path(__file__).parent / 'playlist.json'

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def list_files(service, folder_id):
    results = service.files().list(
        q=f"'{folder_id}' in parents and (mimeType='audio/mpeg' or name contains '.mp3')",
        fields="files(id, name)"
    ).execute()
    return results.get('files', [])

def download_file(service, file_id, file_name, destination):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"  Скачивание {file_name}: {int(status.progress() * 100)}%")
    fh.seek(0)
    with open(destination, 'wb') as f:
        f.write(fh.read())
    print(f"✅ Сохранено: {destination}")

def add_to_playlist(name, path):
    if PLAYLIST_FILE.exists():
        with open(PLAYLIST_FILE, 'r') as f:
            playlist = json.load(f)
    else:
        playlist = []
    
    for track in playlist:
        if track['path'] == path:
            print(f"⏩ {name} уже в плейлисте")
            return
    
    playlist.append({"name": name, "path": path})
    with open(PLAYLIST_FILE, 'w') as f:
        json.dump(playlist, f, indent=2, ensure_ascii=False)
    print(f"➕ {name} добавлен в плейлист")

def sync():
    print("🔄 Синхронизация с Google Drive...")
    service = get_drive_service()
    files = list_files(service, DRIVE_FOLDER_ID)
    print(f"📁 Найдено файлов: {len(files)}")
    
    for file in files:
        file_name = file['name']
        local_path = LOCAL_MUSIC_DIR / file_name
        
        if local_path.exists():
            print(f"⏩ {file_name} уже есть на сервере")
            add_to_playlist(file_name.replace('.mp3', ''), str(local_path))
        else:
            print(f"📥 Скачивание: {file_name}")
            download_file(service, file['id'], file_name, str(local_path))
            add_to_playlist(file_name.replace('.mp3', ''), str(local_path))
    
    print("✅ Синхронизация завершена")

if __name__ == "__main__":
    sync()
