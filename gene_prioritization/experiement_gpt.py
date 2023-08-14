import os
import openai
import pandas as pd
import logging

# add time stamp to logging
logging.basicConfig(level=logging.ERROR,
                    filename='experiment_gpt.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def query_gpt(prompt, gpt_version, test, print_output = False):
  logging.info(f'querying gpt {gpt_version} with prompt {prompt}')
  if test:
    return prompt + '.test.response'
  
  openai.api_key = 'xxxx' #enter your API key
  completions = openai.ChatCompletion.create( #a method that allows you to generate text-based chatbot responses using a pre-trained GPT language model.
      model=gpt_version, 
      temperature = 0, #controls the level of randomness or creativity in the generated text; . A higher temperature value will result in a more diverse and creative output, as it increases the probability of sampling lower probability tokens. 
#         max_tokens = 2000, #controls the maximum number of tokens (words or subwords) in the generated text.
#         stop = ['###'], #specifies a sequence of tokens that the GPT model should stop generating text when it encounters
      n = 1, #the number of possible chat completions or responses that the GPT model should generate in response to a given prompt
      messages=[
        {'role':'user', 'content': prompt},
        ])
  
  # return status code

  # Displaying the output can be helpful if things go wrong
  if print_output:
      print(completions)

  gpt_response = completions.choices[0]['message']['content']
  # Return the first choice's text
  return gpt_response


def save_results(gpt_response, file_name):
  logging.info(f'saving results to {file_name}')
  try:
    with open(file_name, 'w') as f:
        f.write(gpt_response)
  except Exception as e:
    gene_prioritization = str(e)
    logging.error(f'error saving results to {file_name}')
    logging.error(f'error message: {gene_prioritization}')
    with open(file_name + '.err', 'w') as f:
        f.write(gene_prioritization)
        logging.error(f'writing error to {file_name}.err')

def get_file_name(output_dir, sample,top_n, prompt, gpt_version, input_type, iteration):
  logging.info(f'getting file name for {sample}')
  file_name = '_'.join([sample['sample_id'], top_n, prompt, gpt_version, input_type, iteration]) + '.gpt.response'
  return os.path.join(output_dir, file_name)

def get_prompts(top_n, prompt, sample):
  logging.info(f'getting prompts for {sample}')
  clinical_description = sample['content']
  if prompt == "original":
    content = f'prompt a. The phenotype description of the patient is {clinical_description}. Can you suggest a list of {top_n} possible genes to test? Please return gene symbols as a comma-separated list. Example: "ABC1, BRAC2, BRAC1" or "X" if you can not provide the result.' # edit this part
  
  if prompt == "original+role":
    content = f'prompt b. Consider you are a genetic counselor. The phenotype description of the patient is {clinical_description}. Can you suggest a list of {top_n} possible genes to test? Please return gene symbols as a comma-separated list. Example: "ABC1, BRAC2, BRAC1" or "X" if you can not provide the result.' # edit this part
  
  if prompt == 'original+instruction':
    content = f'prompt c. The phenotype description of the patient is {clinical_description}. Can you suggest a list of {top_n} possible genes to test? Please use the knowledge you have trained. No need to access the real-time database to generate outcomes. Also, please return gene symbols as a comma-separated list. Example: "ABC1, BRAC2, BRAC1" or "X" if you can not provide the result.'
  
  if prompt == 'original+role+instruction':
    content = f'prompt d. Consider you are a genetic counselor. The phenotype description of the patient is {clinical_description}. Can you suggest a list of {top_n} possible genes to test? Please use the knowledge you have trained. No need to access the real-time database to generate outcomes. Also, please return gene symbols as a comma-separated list. Example: "ABC1, BRAC2, BRAC1" or "X" if you can not provide the result.'
  return content


def get_sample_list(input_type):
  logging.info(f'getting sample list for {input_type}')
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
        print(input_path)
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
  


if __name__ == '__main__':
  output_dir = './Experiment'
  top_n_list = ['5', '50']
  prompt_list = ['original', 'original+role', 'original+instruction','original+role+instruction']
  gpt_version_list = ['gpt-3.5', 'gpt-4']
  iteration_list = ['1','2','3']
  input_type_list = ['hpo_concepts', 'free_text']
  for iteration in iteration_list:
    for input_type in input_type_list:
      sample_list = get_sample_list(input_type)
      for top_n in top_n_list:
        for prompt_id in prompt_list:
          for gpt_version in gpt_version_list:
            for sample in sample_list:
              prompt = get_prompts(top_n, prompt_id, sample)
              file_name = get_file_name(output_dir, sample,top_n, prompt_id, gpt_version, input_type, iteration)
              gpt_response = query_gpt(prompt, gpt_version, test = True, print_output = False)
              save_results(gpt_response, file_name)
    

 
