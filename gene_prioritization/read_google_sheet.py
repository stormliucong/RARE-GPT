import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# First, you need to create a Google Cloud Platform (GCP) project and enable the Google Sheets API for that project. You can follow the instructions given in the Google Sheets API documentation to create a new project and enable the API.

# Next, you need to create a service account and download the JSON key file for that account. Again, you can follow the instructions given in the Google Sheets API documentation to do this.

# Third, make sure the google sheet is shared with the service account email.


# Replace the path with the path to your JSON key file
credentials = ServiceAccountCredentials.from_json_keyfile_name('./peerless-clock-384418-1c4c2a5185b9.json',
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])

# Replace the sheet name and sheet range with your own values
sheet_name = 'Sheet1'
sheet_range = 'A1:C124'

# Authorize the credentials
gc = gspread.authorize(credentials)

# Open the workbook and select the sheet
workbook = gc.open('GPT_free_text_description')
sheet = workbook.worksheet(sheet_name)

# Get the data from the sheet
data = sheet.get_all_values()

# Create a DataFrame from the data
df = pd.DataFrame(data[1:], columns=data[0])
# Group the data by City
groups = df.groupby('ID')

# Add a sequence label to each group
df['Sequence'] = groups.cumcount()

# Print the DataFrame
df.to_csv('./Data/free_text_input/free_text_pmid_input.csv',index=None)