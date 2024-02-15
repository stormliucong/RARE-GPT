import os
import replicate
import config
os.environ['REPLICATE_API_TOKEN'] = config.REPLICATE_API_KEY
gpt_version = "llama-2-7b-chat"
response = ""
prompt = '''
 Consider you are a genetic counselor. The phenotype description of the patient is Patient 2, complained with visual problems and voice understanding problems also at 13 years. She had audiological and ophthalmologic examinations in Tunisia at 38 years. ABR showed a bilateral absence of responses at 105 dB. Her vocal audiogram confirmed a bilateral severe defect contrasting with a 30 dB defect at the tonal audiometry. Visual evoked potentials (VEP) were present but with a small amplitude and expanded latencies (P100=145ms). Her metabolic and neurological examinations were normal.. Can you suggest a list of 10 possible genes to test? Please consider the phenotype gene relationship, and use the knowledge you have trained on. No need to access the real-time database to generate outcomes. Please return gene symbols as a comma-separated list. Example: "ABC1, BRAC2, BRAC1" or "Not Applicable" if you can not provide the result.
'''
# The meta/llama-2-7b-chat model can stream output as it's running.
for event in replicate.stream(
'meta/' + gpt_version,
input={
    "debug": False,
    "top_p": 1,
    "prompt": prompt,
    "temperature": 0,
    "max_new_tokens": 500,
    "min_new_tokens": -1
},
):
    response += print(str(event), end="")

print(response)
