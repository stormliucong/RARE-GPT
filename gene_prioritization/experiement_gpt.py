def query_gpt(prompt, gpt_version):
  pass

def save_results(gpt_response, file_name):
  pass

def get_file_name(sample,top_n, prompt, gpt_version, iteration):
  pass

def get_prompts(top_n, input_type, prompt):
  pass


def main():
  top_n_list = ['10', '50']
  prompt_list = ['a', 'b']
  gpt_version = ['3.5', '4']
  iteration_list = ['1','2','3']
  input_type_list = ['hpo', 'free_text']
  for iteration in iteration_list:
    for sample in sample_list:
      for top_n in top_n_list:
        for prompt in prompt_list:
          for gpt_version in gpt_version_list:
            for input_type in input_type_list:
              prompts = get_prompts(top_n, input_type, prompt)
              file_name = get_file_name(sample,top_n, prompt, gpt_version, input_type, iteration)
              gpt_response = query_gpt(prompts, file_name)
              save_results(gpt_response, file_name)
    

 
