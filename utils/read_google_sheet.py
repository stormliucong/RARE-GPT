import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Replace the path with the path to your JSON key file
credentials = ServiceAccountCredentials.from_json_keyfile_name('./peerless-clock-384418-1c4c2a5185b9.json',
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])

# Replace the sheet name and sheet range with your own values
sheet_name = 'Sheet2'
sheet_range = 'A1:C130'

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


# according to Jun.
# I double checked and erased gene related text and for the quality check 1 out of 10 was not fitted(90% are good). I colored blue in the excel file, and it was only PMID29092958 that seemed inaccurate.
df = df[~df['ID'].isin(['PMID29092958','PMID30559313'])]
df = df[df['Gene'] != 'Unknown']

# Print the DataFrame
df.to_csv('./Data/free_text_input/free_text_pmid_input.csv',index=None)