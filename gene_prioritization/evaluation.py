def evaluate_meaningfulness(gpt_response):
  '''
  Try to grep a GENE SYMBOL (using regular expression)
  [A-Z0-9]+
  '''
  pass

def evaluate_accuracy(gpt_response, true_gene_symbol):
  '''
  Match greped GENE SYMBOL with true_gene_symbol
  '''
  pass

def evaluate_fulfillment(gpt_response):
  '''
  Try to match predifined JSON (using regular expression)
  \{"gene_list"\s*:\s*"(?:[A-Z0-9]+(?:\s*,\s*[A-Z0-9]+)*)"\}
  '''
  pass

def get_gpt_response(sample,top_n, prompt, gpt_version, input_type, iteration):
  pass

def get_true_gene_symbol(sample):
  pass

def main():
  top_n_list = ['10', '50']
  prompt_list = ['a', 'b']
  gpt_version = ['3.5', '4']
  iteration_list = ['1','2','3']
  input_type_list = ['hpo', free_text']
  mega_table_list = []
  for sample in sample_list:
    true_gene_symbol = get_true_gene_symbol(sample)
    for top_n in top_n_list:
      for prompt in prompt_list:
        for gpt_version in gpt_version_list:
          for iteration in iteration_list:
            for input_type in input_type_list:
              gpt_response = get_gpt_response(sample,top_n, prompt, gpt_version, input_type, iteration)
              m = evaluate_meaningfulness(gpt_response)
              if m == 1:
                a = evaluate_accuracy(gpt_response, true_gene_symbol)
                f = evaluate_fulfillment(gpt_response)
              else:
                a = None
                f = None
              mega_table_list.append((sample,top_n, prompt, gpt_version, iteration, m, a, f ))
  mega_df = pd.DataFrame(mega_table_list)
  
    
