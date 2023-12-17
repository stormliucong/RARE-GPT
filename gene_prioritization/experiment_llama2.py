import os
import pandas as pd
import logging
import random
import re
from multiprocessing import pool, active_children
import time 
from transformers import AutoTokenizer
import transformers
import torch
import argparse



def get_llama2_pipeline(model):
  tokenizer = AutoTokenizer.from_pretrained(model)
  pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto"
  )
  return pipeline, tokenizer

def query_llama2(prompt, pipeline, tokenizer, test):
  logging.debug(f'querying llama2')
  if test:
    return prompt + '.test.response'
  sequences = pipeline(
    prompt,
    do_sample=True,
    top_k=1,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=1000, # controls the maximum number of tokens (words or subwords) in the generated text.
  )
  llama2_response = sequences[0]['generated_text']
  # substring llama2_response by removing the prompt in the beginning
  llama2_response = llama2_response[len(prompt):]
  
  return llama2_response

def get_file_name(output_dir, sample,top_n, prompt, gpt_version, input_type, iteration):
  logging.debug(f'getting file name for {sample}')
  file_name = '__'.join([sample['sample_id'], sample['true_gene'], top_n, prompt, gpt_version, input_type, iteration]) + '.gpt.response'
  return os.path.join(output_dir, file_name)

def get_prompts(top_n, prompt, sample):
  logging.debug(f'getting prompts for {sample}')
  clinical_description = sample['content']
  if prompt == "a":
    # Original
    content = f'The phenotype description of the patient is {clinical_description}. Can you suggest a list of {top_n} possible genes to test? Please return gene symbols as a comma-separated list. Example: "ABC1, BRAC2, BRAC1" or "Not Applicable" if you can not provide the result.'
  
  if prompt == "b":
    # Original + Role
    content = f'Consider you are a genetic counselor. The phenotype description of the patient is {clinical_description}. Can you suggest a list of {top_n} possible genes to test? Please return gene symbols as a comma-separated list. Example: "ABC1, BRAC2, BRAC1" or "Not Applicable" if you can not provide the result.'
  
  if prompt == 'c':
    # Original + Instruction
    content = f'The phenotype description of the patient is {clinical_description}. Can you suggest a list of {top_n} possible genes to test? Please consider the phenotype gene relationship, and use the knowledge you have trained on. No need to access the real-time database to generate outcomes. Please return gene symbols as a comma-separated list. Example: "ABC1, BRAC2, BRAC1" or "Not Applicable" if you can not provide the result.'
  
  if prompt == 'd':
    # Original + Role + Instruction
    content = f'Consider you are a genetic counselor. The phenotype description of the patient is {clinical_description}. Can you suggest a list of {top_n} possible genes to test? Please consider the phenotype gene relationship, and use the knowledge you have trained on. No need to access the real-time database to generate outcomes. Please return gene symbols as a comma-separated list. Example: "ABC1, BRAC2, BRAC1" or "Not Applicable" if you can not provide the result.'
  
  if prompt == 'e':
    # prompt for llama2
    content = f'The phenotype description of the patient is {clinical_description}. Can you suggest a list of {top_n} possible genes to test? Please return gene symbols as a comma-separated list. Example: "ABC1, BRAC2, BRAC1" or "Not Applicable" if you can not provide the result. The predicted gene list is: '
  
  return content


def get_sample_list(input_type):
  logging.debug(f'getting sample list for {input_type}')
  # sample_list = [{"sample_id": 123, "true_gene": "ABC", "content": "muscular dystropy"}]
  # sample_list = [{"sample_id": 123, "true_gene": "ABC", "content": "patient diagnosed with muscular dystropy"}]
  if input_type == 'hpo_concepts':
    # get sample list for hpo input
    data_folder = './Data/HPO_input/Original_data'
    sample_list_hpo = []
    with open(os.path.join(data_folder, 'probe_info')) as f:
      for line in f:
          line = line.strip()
          # change multiple spaces or tabs to a single tab
          while '  ' in line:
              line = line.replace('  ', ' ')
          line = line.replace(' ', '\t')
          line = line.split('\t')
          # get the first element
          folder_name = line[0]
          # get the second element
          file_name = line[1]
          # get the third element
          true_gene = line[2]
          sample_id = folder_name + '.' + file_name
          sample_list_hpo.append({"sample_id": sample_id, "true_gene": true_gene})

    for sample in sample_list_hpo:
      folder_name, file_name = sample['sample_id'].split('.')
      input_path = os.path.join('.', 'Data', 'HPO_input', 'HPO_names', folder_name, file_name)
      with open(input_path) as f:
        hpo_content = f.read()
        sample['content'] = hpo_content.replace('\n',';')
    return sample_list_hpo
  
  if input_type == 'free_text':
    # get sample list for free text input
    data_folder = './Data/free_text_input'

    free_text_df = pd.read_csv(os.path.join(data_folder, 'free_text_pmid_input.csv'))
    sample_list_free_text = []
    for index, row in free_text_df.iterrows():
      free_text = row['Free-text']
      id = row['ID']
      true_gene = row['Gene']
      seq = str(row['Sequence'])
      sample_id = id + '.' + seq
      sample_list_free_text.append({"sample_id": sample_id, "true_gene": true_gene, 'content': free_text})
    return sample_list_free_text
  
def gpt_worker(file, pipeline, tokenizer):
  file_name = file['file_name']
  sample = file['sample']
  # get file name from a file path.
  m = re.match(r'(.+?).gpt.response*', os.path.basename(file_name))
  sample_id, true_gene, top_n, prompt_id, gpt_version, input_type, iteration = m.group(1).split('__')
  try:
    random_int = random.randint(1, 3)
    time.sleep(random_int)
    prompt = get_prompts(top_n, prompt_id, sample)
    # gpt_response = query_gpt(prompt, gpt_version, test = False, print_output = False)
    gpt_response = query_llama2(prompt, pipeline, tokenizer, test = False)
    with open(file_name, 'w') as f:
      f.write(gpt_response)
  except Exception as e:
    logging.error(f'error saving results to {file_name}')
    logging.error(f'error message: {str(e)}')
    with open(file_name + '.err', 'w') as f:
      f.write(str(e))
      logging.error(f'writing error to {file_name}.err')

if __name__ == '__main__':  # parse argument
  parser = argparse.ArgumentParser()
  parser.add_argument('--probability_of_1', type=float, default=0.1, help='sample rate of the files to be processed. 1.0 means all files will be processed. 0.5 means 50% of the files will be processed.')
  parser.add_argument('--output_dir', type=str, default='./Experiment_004subset', help='output directory')
  parser.add_argument('--previous_dir', type=str, default='./Experiment_003subset', help='# change this to your previous output directory. The program will check if the file exists in the previous directory. If it does, it will skip the file.')
  parser.add_argument('--log_file_name', type=str, default='experiment_gpt.log', help='log file name')
  parser.add_argument('--llama2_model_path', type=str, default='llama2-7b', help='llama2 model path')
  args = parser.parse_args()
  
  
  # add time stamp to logging
  logging.basicConfig(level=logging.INFO,
                    filename=args['log_file_name'],
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
  # load base llama2 model.
  pipeline, tokenizer = get_llama2_pipeline(args['llama2_model_path']) # add your model path here.
  # # Probability of getting 1
  probability_of_1 = args['probability_of_1'] # change this to control sample rate (1 means all samples are processed)
  
  # List of choices (1 or 0)
  choices = [1, 0]
  file_list = []
  output_dir = args['output_dir']
  previous_dir = args['previous_dir']
  top_n_list = ['10', '50']
  prompt_list = ['e']
  gpt_version_list = ['llama2-7b']
  iteration_list = ['1','2','3']
  input_type_list = ['hpo_concepts', 'free_text']
  for iteration in iteration_list:
    for input_type in input_type_list:
      sample_list = get_sample_list(input_type)
      for top_n in top_n_list:
        for prompt_id in prompt_list:
          for gpt_version in gpt_version_list:
            for sample in sample_list:
              file_name = get_file_name(output_dir, sample,top_n, prompt_id, gpt_version, input_type, iteration)
              history_file = get_file_name(previous_dir, sample,top_n, prompt_id, gpt_version, input_type, iteration)
              if os.path.exists(history_file) or os.path.exists(history_file + '.err'):
                logging.debug(f'file {file_name} already exists, skipping')
                continue
              random_flag = random.choices(choices, [probability_of_1, 1 - probability_of_1])[0]
              # random_flag = 1
              if random_flag == 1:
                file_list.append({"file_name": file_name, "sample": sample})

  logging.info(f'number of files to be processed: {len(file_list)}')
  # gpt_master(file_list)
  for file in file_list:
    gpt_worker(file, pipeline, tokenizer)
                
                
  

 
