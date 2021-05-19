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

from send_email import send_email

import os
import glob


class CustomError(Exception):
    pass


"""
credentials.json file is needed from GCP.
Without that file, this won't work

"""

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

# def main():
#     """Shows basic usage of the Drive v3 API.
#     Prints the names and ids of the first 10 files the user has access to.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     #TODO return creds if needed

#     drive_service = build('drive', 'v3', credentials=creds)

#     # Call the Drive v3 API
#     # """ part of the quickstart
#     results = drive_service.files().list(
#         pageSize=10, fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])

#     if not items:
#         print('No files found.')
#     else:
#         print('Files:')
#         for item in items:
#             print(u'{0} ({1})'.format(item['name'], item['id']))
#     # """

#     # #* upload file to drive in parents folder
#     # file_name = "Google.py"
#     # file_metadata = {
#     #     'name': f"{file_name}",
#     #     "parents": ["1WSJDqsLHJ4yOUu2HBDjICr52fLZzAFO-"]  # folder id
#     # }
#     # media = MediaFileUpload(f"./{file_name}")
#     # file = drive_service.files().create(body=file_metadata,
#     #                                     media_body=media,
#     #                                     fields='id').execute()
#     # print('File ID: %s' % file.get('id'))

#     #* delete file
#     # file_id = '1HldbxgYklxoECXVQBMFKd-cVO0DljAWP'

#     # res = drive_service.files().delete(fileId=file_id).execute()
#     # print(res)

#     #* get create time for a file
#     # res = drive_service.files().list().execute()
#     # # res = json.dumps(res)
#     # # pprint(res["files"][0])  #TODO remove this 0
#     # # todo try to do this using batch operation
#     # file_id = res["files"][0]['id']  #TODO remove this 0
#     # res = drive_service.files().get(fileId=file_id,
#     #                                 fields='createdTime').execute()

#     # # convert rfc 3339 timestamp to datatime format in python | timezone aware
#     # created_time = iso8601.parse_date(res['createdTime'])
#     # # created_time = created_time.replace(tzinfo=None)
#     # tz = pytz.timezone("Asia/Kolkata")
#     # curr_time = datetime.now(tz=tz)
#     # # curr_time = curr_time.replace(tzinfo=tz)
#     # print("curr_time =", curr_time)
#     # print("created_time =", created_time)

#     # difference = curr_time - created_time
#     # print(difference.total_seconds())  # diff.seconds doesn't count days
#     # to_remove = difference.total_seconds() > 86400
#     # print(to_remove)  # boolean saying whether to remove or not

#     # print(res['createdTime'])  # in rfc 3339 format

#     #* empty trash
#     # res = drive_service.files().emptyTrash().execute()
#     # print(res)

#     #* Change permission
#     # file_id = '180VY1Qt_i34NSeIeL1uIOiuMnA2iytBI'

#     # def callback(request_id, response, exception):
#     #     if exception:
#     #         # Handle error
#     #         print(exception)
#     #     else:
#     #         print("Permission Id: %s" % response.get('id'))

#     # batch = drive_service.new_batch_http_request(callback=callback)
#     # user_permission = {
#     #     'type': 'anyone',
#     #     # 'role': 'commenter',
#     #     'role': 'reader',
#     #     # 'role': 'writer',
#     # }
#     # # user_permission = {
#     # #     'type': 'user',
#     # #     'role': 'writer',
#     # # }
#     # batch.add(drive_service.permissions().create(
#     #     fileId=file_id,
#     #     body=user_permission,
#     #     fields='id',
#     # ))
#     # batch.execute()

#     #* delete permissions | unable to do due to missing permissionId
#     # file_id = '1eZ0U4wdVKYXWX3P9szw68vlCFcliqp8k'

#     # def callback(request_id, response, exception):
#     #     if exception:
#     #         # Handle error
#     #         print(exception)
#     #     else:
#     #         print("Permission Id: %s" % response.get('id'))

#     # batch = drive_service.new_batch_http_request(callback=callback)
#     # user_permission = {
#     #     'type': 'anyone',
#     #     # 'role': 'commenter',
#     #     'role': 'reader',
#     #     # 'role': 'writer',
#     # }
#     # # user_permission = {
#     # #     'type': 'user',
#     # #     'role': 'writer',
#     # # }
#     # batch.add(drive_service.permissions().delete(
#     #     fileId=file_id, permissionId="15122285644999934203"))
#     # batch.execute()

# drive_service = None


def init_oauth2():
    # global drive_service
    creds = None
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

    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service


def drive_upload(file_path, file_name, drive_service):
    """file_path is the path to file on local machine
    file_name is the name on drive.
    include file extensions in both names"""

    # global drive_service
    if drive_service is None:
        raise CustomError(
            "drive_service variable not initialised.\nPlease run init_oauth2()"
        )

    # file_name = "Google.py"
    file_metadata = {
        'name': file_name  # folder id
    }
    media = MediaFileUpload(file_path)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))
    return file.get('id')  # returns the file id uploaded


def change_permission(file_id, drive_service):
    # global drive_service

    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print("Permission Id: %s")

    batch = drive_service.new_batch_http_request(callback=callback)
    user_permission = {
        'type': 'anyone',
        # 'role': 'commenter',
        'role': 'reader',
        # 'role': 'writer',
    }
    batch.add(drive_service.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id',
    ))
    batch.execute()


def drive_delete(file_id, drive_service):
    """delete file on drive with the given file_id"""
    # global drive_service

    res = drive_service.files().delete(fileId=file_id).execute()
    print(res)


def get_create_times_and_delete(drive_service):
    # global drive_service
    file_list = drive_service.files().list().execute()
    remove_fileid = []
    for curr in file_list["files"]:
        curr_file_id = curr["id"]
        curr_res = drive_service.files().get(fileId=curr_file_id,
                                             fields='createdTime').execute()
        created_time = iso8601.parse_date(curr_res['createdTime'])
        created_time = created_time.replace(tzinfo=None)
        curr_time = datetime.utcnow()
        diff = curr_time - created_time
        to_remove = diff.total_seconds() > 86400  # 24 hours
        if to_remove:
            remove_fileid.append(curr_file_id)

    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print("Permission Id: %s")

    batch = drive_service.new_batch_http_request(callback=callback)
    for file_id in remove_fileid:
        print(type(file_id))
        print(file_id)
        batch.add(drive_service.files().delete(fileId=file_id))
    batch.execute()


def the_function(file_path, file_name, receiver_address):
    """file_path is the path to file on local machine
    file_name is the name on drive.
    include file extensions in both names"""

    drive_service = init_oauth2()
    uploaded_fileid = drive_upload(file_path, file_name, drive_service)
    change_permission(uploaded_fileid, drive_service)
    get_create_times_and_delete(drive_service)
    # return the uploaded fileid in the form of an email
    drive_file_link = f"drive.google.com/file/d/{uploaded_fileid}"
    print(drive_file_link)
    body = f"here is the link to your file\n{drive_file_link}"
    send_email(receiver_address, body)
    curr_dir = os.path.dirname(file_path)
    for to_remove_file in glob.glob(f"{curr_dir}"):
        os.remove(to_remove_file)


if __name__ == '__main__':
    # main()
    the_function("./drive.py", "uploaded100.py",
                 "sarveshvhawal6969@yopmail.com")
