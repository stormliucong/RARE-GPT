import os
import requests


dx_dict = {}
data_folder = './Data/HPO_input/Original_data'

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
    file_path = os.path.join(data_folder, folder_name, file_name)
    # add to dict. key: file name, value: gene
    dx_dict[file_path] = gene

input_folder = 'HPO_input'
input_folder = 'simulated_pt_input'

# go over all files in a directory
results = []
for file_path in dx_dict.keys():
  # get file name and folder
  file_name = os.path.basename(file_path)
  folder_name = os.path.basename(os.path.dirname(file_path))
  input_path = os.path.join('.', 'Data', input_folder,'Original_data', folder_name, file_name)
  output_path = os.path.join('.', 'Data', input_folder,'HPO_names', folder_name, file_name)
  # result_json = {}
  # read file
  if not os.path.isfile(output_path):
    with open(input_path) as f:
      print(f"Input: {input_path}")
      HP_IDs = f.read().splitlines()
      HP_content = ','.join(HP_IDs)

      hp_names = []
      for hp_id in HP_IDs:
        # call api to get HPO names
        res_json = requests.get('https://hpo.jax.org/api/hpo/search/?q=' + hp_id).json()
        hp_name = res_json['terms'][0]['name']
        hp_names.append(hp_name)
      
      hp_names_content = ','.join(hp_names)
      if not os.path.exists(os.path.join('.', 'Data', input_folder, 'HPO_names', folder_name)):
        os.makedirs(os.path.join('.', 'Data', input_folder,'HPO_names', folder_name))
      
      print(f"Output: {output_path}")
      with open(output_path, 'w') as f:
        f.write(hp_names_content)
