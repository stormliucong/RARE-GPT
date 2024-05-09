# RARE-GPT: Rare Disease Diagnosis Support using GPT

RARE-GPT is based on the GPT architecture by OpenAI, which provides support for diagnosing rare diseases. With the help of artificial intelligence, we aim to provide accurate and timely diagnoses for patients with rare diseases. The project also included using llama2 as a benchmark.

## Features

- We evaluated different zero-short prompts for phenotypic-driven gene ranking tasks using ChatGPT 
- ChatGPT3.5-turbo, ChatGPT4, LLama2-Chat-7B, LLama2-Chat-13B, LLama2-Chat-70B were evaluated
- Different input clinical features - HPO names and free-text were evaluated
- Top 10 and Top 50 results were evaluated
- We evaluated the variablity of ChatGPT by repeating the experiment three times
- Another prompts are designed for llama2 base model to evaluate the performance of llama2.

## Getting Started
- Installation 
    ```sh
    python3.10 -m venv .openai
    source .openai/bin/activate
    pip install -r requirements.txt # openai-0.27 required for this GPT-4.
    ```
- Find all required codes in `gene_priorization` folder.
- You will need a open api key to run the program. Please put the following json into a `config.py` file. (Not needed for llama2)
    ```python
    OPENAI_API_KEY = "xxx"
    ```
- To collect GPT response. run `experiment_gpt.py`. Check the arguments and help.
- To collect llama2 response, run `experiment_llama2.py`. Check the arguments and help.
- Due to possible failure in single GPT or llama2 experiment. `*.err` file and empty file will be generated. Check the error to debug and also move successfully generated file to another folder to avoid re-processing. Check `utils.sh` for details.
- To generate evaluation, fun `evaluation.py`. You will need output folders as input from above two.
- run `gene_analysis.Rmd` (TBD: comments and clean codes) to generate tables and figures.




## free text dataset
- We have collected the free-text dataset in a [google sheet](https://docs.google.com/spreadsheets/d/1GL_mEX2Iqz5ANvftYWa2mwDKxnA05jN-s2SKDw3rLeo/edit#gid=0)
- `read_google_sheet.py` can be used to read google sheet and create a pandas dataframe locally.
- Extra steps are needed to enable the google service API
 - you need to create a Google Cloud Platform (GCP) project and enable the Google Sheets API for that project. You can follow the instructions given in the Google Sheets API documentation to create a new project and enable the API.
 - you need to create a service account and download the JSON key file for that account. 
 - you can follow the instructions given in the Google Sheets API documentation to do this.
 - make sure the google sheet is shared with the service account email.


## Other Tech notes
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
