# openai chat complete example
import os
import openai
import json
import requests

# read json file
with open('./api_key.json') as f:
  data = json.load(f)
  openai.api_key = data['api_key']

def generate_gpt4_response(content, print_output=False):
  '''
  Generates a response from the GPT-4 chatbot given a prompt.
  '''

  completions = openai.ChatCompletion.create( #a method that allows you to generate text-based chatbot responses using a pre-trained GPT language model.
      model="gpt-4", 
      temperature = 0, #controls the level of randomness or creativity in the generated text; . A higher temperature value will result in a more diverse and creative output, as it increases the probability of sampling lower probability tokens. 
#         max_tokens = 2000, #controls the maximum number of tokens (words or subwords) in the generated text.
#         stop = ['###'], #specifies a sequence of tokens that the GPT model should stop generating text when it encounters
      n = 1, #the number of possible chat completions or responses that the GPT model should generate in response to a given prompt
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "please provide a list of top {x} possible genes to test given the following phenotypes."},
        {"role": "user", "content": ""},
        {"role": "assistant", "content": "I have found HPO terms:\nglobal developmental delay | HP_0001263\nataxia | HP_0001251\nepisodes of paroxysmal laughter | HP_0000749\nlaughter | HP_0000748\nseizures | HP_0001250\nmicrocephaly | HP_0000252\nprominent jaw | HP_0002051\nwide mouth | HP_0000154\npointed chin | HP_0000307\nTongue thrusting | HP_0000182\nmovement disorder | HP_0100022\nwide based, ataxic gait | HP_0002136\nataxic gait | HP_0002066\njerky limb movements | HP_0002276\nflapping of the hands | HP_0100023"},
        {"role": "user", "content": content}
    ]
  )
  
  # return status code

  # Displaying the output can be helpful if things go wrong
  if print_output:
      print(completions)

  # Return the first choice's text
  return completions.choices[0]['message']['content'] #I only want the first repsonses

dx_dict = {}
data_folder = '/Users/cl3720/Desktop/copilot-examples/GPT_Gene_Prioritization/Data/Original_data'
hpo_name_folder = '/Users/cl3720/Desktop/copilot-examples/GPT_Gene_Prioritization/Data/HPO_names'
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
    gene = line[2]
    
    # get the full path of the file
    file_path = os.path.join(hpo_name_folder, folder_name, file_name)
    # add to dict. key: file name, value: gene
    dx_dict[file_path] = gene

# go over all files in a directory
results = []

for file_path in list(dx_dict.keys()):
      
    
  file_name = os.path.basename(file_path)
  folder_name = os.path.basename(os.path.dirname(file_path))
  for top_n in ['5', '10', '50']:
        
    output_path = os.path.join('.', 'Data', 'GPT_response', 'top_' + top_n, folder_name, file_name)
    output_error_path = os.path.join('.', 'Data', 'GPT_response', 'top_' + top_n, folder_name, file_name + '_error')

    if not os.path.exists(os.path.join('.', 'Data', 'GPT_response', 'top_' + top_n, folder_name)):
      os.makedirs(os.path.join('.', 'Data', 'GPT_response', 'top_' + top_n, folder_name))
    # file exists
    if not os.path.exists(output_path):
      with open(file_path) as f:
        hpo_content = f.read()
        # call api to get gene prioritization
        content = 'The phenotype desciprtion of the patient is {content}. Can you suggest a list of top {x} possible genes to test? Please return gene symbols as a comma separated list. Example: "ABC1,BRAC2,BRAC1"'.format(x = top_n, content = hpo_content)
        print(content)
        try:
          gene_prioritization = generate_gpt4_response(content,print_output=True)
          with open(output_path, 'w') as f:
            f.write(gene_prioritization)
        except Exception as e:
          gene_prioritization = str(e)
          with open(output_error_path, 'w') as f:
            f.write(gene_prioritization)
      
    

