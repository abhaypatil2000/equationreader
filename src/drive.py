from __future__ import print_function
from datetime import datetime
import os.path
from re import T
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import json
# from prettyprint import pp
from pprint import pprint

# import httplib2
# import os, io
# from apiclient import discovery
# from oauth2client import client
# from oauth2client import tools
# from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import iso8601
import pytz
"""
credentials.json file is needed from GCP.
Without that file, this won't work

"""

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    #TODO return creds if needed

    drive_service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    """ part of the quickstart
    # results = drive_service.files().list(
    #     pageSize=10, fields="nextPageToken, files(id, name)").execute()
    # items = results.get('files', [])

    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['name'], item['id']))
    """

    #* upload file to drive in parents folder
    file_name = "Google.py"
    file_metadata = {
        'name': f"{file_name}",
        "parents": ["1WSJDqsLHJ4yOUu2HBDjICr52fLZzAFO-"]  # folder id
    }
    media = MediaFileUpload(f"./{file_name}")
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))

    #* delete file
    # file_id = '1HldbxgYklxoECXVQBMFKd-cVO0DljAWP'

    # res = drive_service.files().delete(fileId=file_id).execute()
    # print(res)

    #* get create time for a file
    # res = drive_service.files().list().execute()
    # # res = json.dumps(res)
    # # pprint(res["files"][0])  #TODO remove this 0
    # # todo try to do this using batch operation
    # file_id = res["files"][0]['id']  #TODO remove this 0
    # res = drive_service.files().get(fileId=file_id,
    #                                 fields='createdTime').execute()

    # # convert rfc 3339 timestamp to datatime format in python | timezone aware
    # created_time = iso8601.parse_date(res['createdTime'])
    # # created_time = created_time.replace(tzinfo=None)
    # tz = pytz.timezone("Asia/Kolkata")
    # curr_time = datetime.now(tz=tz)
    # # curr_time = curr_time.replace(tzinfo=tz)
    # print("curr_time =", curr_time)
    # print("created_time =", created_time)

    # difference = curr_time - created_time
    # print(difference.total_seconds())  # diff.seconds doesn't count days
    # to_remove = difference.total_seconds() > 86400
    # print(to_remove)  # boolean saying whether to remove or not

    # print(res['createdTime'])  # in rfc 3339 format

    #* empty trash
    # res = drive_service.files().emptyTrash().execute()
    # print(res)

    #* Change permission
    # file_id = '1eZ0U4wdVKYXWX3P9szw68vlCFcliqp8k'

    # def callback(request_id, response, exception):
    #     if exception:
    #         # Handle error
    #         print(exception)
    #     else:
    #         print("Permission Id: %s" % response.get('id'))

    # batch = drive_service.new_batch_http_request(callback=callback)
    # user_permission = {
    #     'type': 'anyone',
    #     # 'role': 'commenter',
    #     'role': 'reader',
    #     # 'role': 'writer',
    # }
    # # user_permission = {
    # #     'type': 'user',
    # #     'role': 'writer',
    # # }
    # batch.add(drive_service.permissions().create(
    #     fileId=file_id,
    #     body=user_permission,
    #     fields='id',
    # ))
    # batch.execute()

    #* delete permissions | unable to do due to missing permissionId
    # file_id = '1eZ0U4wdVKYXWX3P9szw68vlCFcliqp8k'

    # def callback(request_id, response, exception):
    #     if exception:
    #         # Handle error
    #         print(exception)
    #     else:
    #         print("Permission Id: %s" % response.get('id'))

    # batch = drive_service.new_batch_http_request(callback=callback)
    # user_permission = {
    #     'type': 'anyone',
    #     # 'role': 'commenter',
    #     'role': 'reader',
    #     # 'role': 'writer',
    # }
    # # user_permission = {
    # #     'type': 'user',
    # #     'role': 'writer',
    # # }
    # batch.add(drive_service.permissions().delete(
    #     fileId=file_id, permissionId="15122285644999934203"))
    # batch.execute()


if __name__ == '__main__':
    main()