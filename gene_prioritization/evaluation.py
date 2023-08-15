import os
import requests
import re
import pandas as pd
import logging
import json

logging.basicConfig(level=logging.DEBUG,
                    filename='eval.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def evaluate_completeness(gpt_response, hgnc_complete_list):
  '''
  Try to grep a GENE SYMBOL (using regular expression)
  [A-Z0-9]+
  '''
  logging.debug('gpt_response: {}'.format(gpt_response))
  pattern = r'[ ,.!?]+'
  tokens = re.split(pattern, gpt_response)
  tokens = [token.strip() for token in tokens if len(token) > 1]
  logging.debug('tokens: {}'.format(tokens))
  overlapped_genes = set(tokens) & set(hgnc_complete_list)
  logging.debug('overlapped_genes: {}'.format(overlapped_genes))
  
  if len(overlapped_genes) > 1:
    return 1
  else:
    return 0

def evaluate_accuracy(gpt_response, true_gene_symbol):
  '''
  Match greped GENE SYMBOL with true_gene_symbol
  '''
  logging.debug('gpt_response: {}'.format(gpt_response))
  pattern = r'[ ,.!?]+'
  tokens = re.split(pattern, gpt_response)
  tokens = [token.strip() for token in tokens if len(token) > 1]
  logging.debug('tokens: {}'.format(tokens))
  logging.debug('true_gene_symbol: {}'.format(true_gene_symbol))
  if true_gene_symbol in set(tokens):
    return 1
  else:
    return 0

def evaluate_fulfillment(gpt_response, top_n):
  '''
  Try to match predifined JSON (using regular expression)
  \{"gene_list"\s*:\s*"(?:[A-Z0-9]+(?:\s*,\s*[A-Z0-9]+)*)"\}
  '''
  na_regex = re.compile(re.escape("not applicable"), re.IGNORECASE)
  na_m = re.findall(na_regex, gpt_response)
  if len(na_m) == 0:
    is_na_format = False
  else:
    is_na_format = True
  
  if top_n == '5':
    # 5*(2+1)
    gene_regex = rf'[A-Z0-9|,\s]{{15,}}'
  elif top_n == '50':
    # 50*(2+1) = 150
    gene_regex = rf'[A-Z0-9|,\s]{{150,}}'
    
  gene_list = re.findall(gene_regex, gpt_response)
  if len(gene_list) == 0:
    is_gene_list_format = False
  else:
    longest_m = max(gene_list, key=len)
    is_gene_list_format = (len(longest_m.split(',')) == int(top_n))
  if is_gene_list_format or is_na_format:
    return 1
  else:
    return 0

def get_gpt_response(file):
  with open(file, 'r') as f:
    text = f.read() 
    return text
  
def get_hgnc_complete_list(symbol_json_file='./hgnc_complete_set_2020-10-01.json'):
  # read json from url 
  if not os.path.exists(symbol_json_file):
    logging.info('Downloading HGNC complete list')
    url = "https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/archive/quarterly/json/hgnc_complete_set_2020-10-01.json"
    gene_list_json = requests.get(url).json()
    symbol_list = [doc['symbol'] for doc in gene_list_json['response']['docs']]
    logging.info('HGNC complete list downloaded')
    logging.info('length of HGNC complete list: {}'.format(len(symbol_list)))
    with open(symbol_json_file, 'w') as f:
      json.dump(symbol_list, f)
  else:
    with open(symbol_json_file, 'r') as f:
      logging.info('Reading HGNC complete list from local file')
      symbol_list = json.load(f)
      logging.info('length of HGNC complete list: {}'.format(len(symbol_list)))
  return symbol_list


def main():
  output_dir = './Experiment_test'
  hgnc_complete_list = get_hgnc_complete_list()
  mega_table_list = []
  for file in os.listdir(output_dir):
    error, c, a, f = None, None, None, None
    if file.endswith('.gpt.response') or file.endswith('.gpt.response.err'):
      logging.debug(file.split('__'))
      m = re.match(r'(.+?).gpt.response*', file)
      sample_id, true_gene, top_n, prompt, gpt_version, input_type, iteration = m.group(1).split('__')
      if file.endswith('.gpt.response'):
        error = 0
        gpt_response = get_gpt_response(os.path.join(output_dir,file))
        c = evaluate_completeness(gpt_response, hgnc_complete_list)
        if c == 1:
          a = evaluate_accuracy(gpt_response, true_gene)
        f = evaluate_fulfillment(gpt_response, top_n)
      else:
        error = 1         
    mega_table_list.append([sample_id, true_gene, top_n, prompt, gpt_version, input_type, iteration, error, c, a, f])
  mega_df = pd.DataFrame(mega_table_list)
  mega_df.to_csv('mega_eval_table.csv', index=False, header=False)
  
if __name__ == '__main__':
  main()