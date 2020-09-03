from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def google_connect():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service

def fetch_sheet (service, name, data_range):
    """Return data from a sheet"""
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId = name,
                                range = data_range).execute()
    values = result.get('values', [])
    return values

def create_sheets (service, name):
    """Create a sheet"""
    spreadsheet = {'properties': {'title': name}}
    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                    fields='spreadsheetId').execute()
    id = spreadsheet.get('spreadsheetId')
    return id

def write_sheet (service, name, data, data_range):
    """Write to a sheet"""
    response_date = service.spreadsheets().values().update(
        spreadsheetId = name,
        valueInputOption = 'RAW',
        range = data_range,
        body = dict(
            majorDimension = 'ROWS',
            values = data.T.reset_index().T.values.tolist())
    ).execute()
    print('Sheet successfully Updated')


def append_sheet (service, sheet_id, range_name, data):
    """Append to a sheet"""
    body = {'values': data}
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_id, range=range_name,
    valueInputOption='RAW', body=body).execute()
    print('{0} cells appended.'.format(result.get('updates').get('updatedCells')))


def clear_sheet (service, sheet_id, data_range):
    """Clear the sheet"""
    request_body = {}
    request = service.spreadsheets().values().clear(spreadsheetId=sheet_id, range=data_range, body=request_body)
    response = request.execute()
