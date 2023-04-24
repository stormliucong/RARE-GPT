### GPT_Gene_Prioritization
Research project for using ChatGPT for rare disease gene prioritization

#### Getting started
- python3.10 required for openai-0.27.
- openai-0.27 required for this GPT-4.

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

#### running program
- You will need a open api key to run the program. Please put the following json into a `api_key.json` file.
```
{"api_key": xxxxx}
```
