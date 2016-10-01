#from __future__ import print_function

import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import datetime
from oauth2client.client import OAuth2WebServerFlow
import webapp2

class Scheduler(webapp2.RequestHandler):

    def __init__(self):
        self.schedule = {}
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
        self.SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'ccc-therejectedbot'
        self.flags = 0

        try:
            import argparse
            self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            self.flags = None
        self.main()


    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        # This has to be commented out because google cloud platform has
        # deprecated filesystem access
        #if not os.path.exists(credential_dir):
        #    os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def main(self):
        # credentials = self.get_credentials()
        flow = OAuth2WebServerFlow('532839862987-grmls6uf8tfej140mf32i23qptk2n310.apps.googleusercontent.com', 'WFabmhVTNtWzzEW5-TCWQZUH', 'https://www.googleapis.com/auth/spreadsheets.readonly', 'urn:ietf:wg:oauth:2.0:oob')
        authorize_url = flow.step1_get_authorize_url()
        self.redirect(authorize_url)
        # code = '4/mS6IOQVQV2aDSctWTPMkCvRvoHHF60ggO953GBj_tHM'.strip()
        # code = raw_input('Enter verification code: ').strip()
        credentials = flow.step2_exchange('4/VZADEqdv6D5LMG16_tYsQ0jJIOo4JKRoh1FpdNyU3to')
        # code = request.GET("code")
        # credentials = flow.step2_exchange(code)


        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheetId = '1tG1rFftB-hthBIgCJcfMU2PhPvt_tym0wmTBQV-OvOA'
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
