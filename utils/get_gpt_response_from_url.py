import requests
import re
import logging
import os

def get_file_name(output_dir, sample,top_n, prompt, gpt_version, input_type, iteration):
  logging.info(f'getting file name for {sample}')
  file_name = '_'.join([sample['sample_id'], top_n, prompt, gpt_version, input_type, iteration]) + '.gpt.response'
  return os.path.join(output_dir, file_name)

def create_manual_eval_files(row, output_dir = 'manual_evaluations'):
    sample,top_n, prompt_id, gpt_version, input_type, iteration = row['sample_id'], row['top_n'], row['prompt_id'], row['gpt_version'], row['input_type'], row['iteration']
    filename = get_file_name(output_dir, sample,top_n, prompt_id, gpt_version, input_type, iteration)
    gpt_response_url = row['URL'] 
    gpt_response_url = "https://chat.openai.com/share/354ad88d-0371-4cec-b6ec-94d0dea9b67e"

    r = requests.get(gpt_response_url)
    print(r.content)

    pattern = r"\"author\":{\"role\":\"assistant\",\"metadata\":{}},\"create_time\"\:.+?,\"content\":{\"content_type\":\"text\",\"parts\":\[\"(.+?)\"\]},\"status\":\"finished_successfully\""

    gpt_response = re.search(pattern, r.content.decode('utf-8')).group(1)

    # save to file. print \n as new line
    with open('./test_gpt_response.txt', 'w') as f:
        f.write(filename.replace('\\n', '\n'))

if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv('./manual_evaluations.csv')
    df.apply(create_manual_eval_files, axis=1)