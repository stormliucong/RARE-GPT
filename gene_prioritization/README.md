### GPT_Gene_Prioritization
Research project for using ChatGPT for rare disease gene prioritization

#### Getting started
- python3.10 required for openai-0.27.
- openai-0.27 required for this GPT-4.
- You will need a open api key to run the program. Please put the following json into a `api_key.json` file.
```json
{"api_key": xxxxx}
```
- You will need a google service API key see [Google Sheets API instruction](https://developers.google.com/sheets/api/guides/concepts). Here is an example
```json
{
  "type": "service_account",
  "project_id": "peerless-clock-xxxxxx",
  "private_key_id": "privatekeyid",
  "private_key": "-----BEGIN PRIVATE KEY-----\nprivatekey\n-----END PRIVATE KEY-----\n",
  "client_email": "python@peerless-clock-xxxxxx.iam.gserviceaccount.com",
  "client_id": "116xxxxxxxxxxxxxxxx",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/python%40peerless-clock-xxxxxx.iam.gserviceaccount.com"
}
```

#### install python 3.10
- Install the required dependency for adding custom PPAs.
`sudo apt install software-properties-common -y`
- Then proceed and add the deadsnakes PPA to the APT package manager sources list as below.
`sudo add-apt-repository ppa:deadsnakes/ppa`
- With the deadsnakes repository added to your Ubuntu 20.04|18.04 system, now download Python 3.10 with the single command below.
`sudo apt install python3.10`
- Verify the installation by checking the installed version.
`python3.10 --version`



#### install virtual env openai 0.27
- install the venv of the specific python version 
`sudo apt install python3.10-venv`
- install venv .openai
`python3.10 -m venv .openai`
- activate virtual env
    - in windows
    `.openai  \Scripts\activate.bat`
    - in linux/mac
    `source .openai/bin/activate`
- install openai 
`pip install openai`
- check openai version version
`pip show openai`
- install requirement
`pip install -r requirements.txt`

#### free text dataset
- We have collected the free-text dataset in a [google sheet](https://docs.google.com/spreadsheets/d/1GL_mEX2Iqz5ANvftYWa2mwDKxnA05jN-s2SKDw3rLeo/edit#gid=0)
- `read_google_sheet.py` can be used to read google sheet and create a pandas dataframe locally.
- Extra steps are needed to enable the google service API
 - you need to create a Google Cloud Platform (GCP) project and enable the Google Sheets API for that project. You can follow the instructions given in the Google Sheets API documentation to create a new project and enable the API.
 - you need to create a service account and download the JSON key file for that account. 
 - you can follow the instructions given in the Google Sheets API documentation to do this.
 - make sure the google sheet is shared with the service account email.


#### Explain of each script

- `get_hpo_names.py` will get hpo names by calling hpo jax api
- `hpo_based_prediction.py` and `free_text_based_prediction` will make prediction by calling openai's API
- `simulate_patients_hpo.py` will create decoy patients
- `post-processing-*.py` will identify gene names and parse GPT predicted results
- `summary-*` will summarize the results and generate the tables


