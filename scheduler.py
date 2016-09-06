#from __future__ import print_function

import sys
sys.path.insert(0, 'libs')

import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import datetime

class Scheduler():
    def __init__(self):
        self.schedule = {}

        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None
        self.main()

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API Python Quickstart'


    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def main(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheetId = '1fC9qVoGq6FHm50-gfuugH9wnyYd47Ls3ep3z7HBvOPY'
        rangeName = 'Schedule!A1:M'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName).execute()

        labels = result['values'].pop(0)
        values = result.get('values', [])

        now = datetime.date.today()
        while now.weekday() != 6:
            now += datetime.timedelta(1)

        nextSunday = now

        if not values:
            print('No data found.')
        else:
            for row in values:
                if len(row) > 0:
                    if row[0] != '':
                        d = datetime.datetime.strptime(row[0], '%m/%d/%Y')
                        if(str(nextSunday) in str(d)):
                            reformattedDate = d.strftime("%Y%m%d")
                            for i in range(len(row)):
                                if reformattedDate not in self.schedule:
                                    self.schedule[reformattedDate] = {}
                                self.schedule[reformattedDate][labels[i]] = row[i]
        # for date in self.schedule:
        #     for title in self.schedule[date]:
        #         print title + ": " + self.schedule[date][title]
                # Print columns A and E, which correspond to indices 0 and 4.
                #print('%s, %s' % (row[1], row[2]))

# if __name__ == "__main__":
#     main()

# Scheduler().schedule
