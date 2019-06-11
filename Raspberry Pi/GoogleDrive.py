from __future__ import print_function
import httplib2
import os, io
from apiclient import discovery
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'

class GoogleDrive:
    def __init__(self,filename,filepath,mimetype):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('drive', 'v3', http=creds.authorize(Http()))

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        
        #dodanie do dysk
        file_metadata = {'name': filename}
        media = MediaFileUpload(filepath,mimetype=mimetype)
        file2 = service.files().create(body=file_metadata,media_body=media,fields='id').execute()
        print('File ID: %s' % file2.get('id'))
        
        #przeniesienie do folderu
        file_id = file2.get('id')
        folder_id = '1DCIiVclMjlSWsmbYZgRxr9xI0eqweNWw'
        # Przygotowanie wczesniejszego folderu do usuniecia
        file2 = service.files().get(fileId=file_id,fields='parents').execute()
        previous_parents = ",".join(file2.get('parents'))
        # Operacja przeniesienia do folderu
        file2 = service.files().update(fileId=file_id,addParents=folder_id,removeParents=previous_parents,fields='id, parents').execute()