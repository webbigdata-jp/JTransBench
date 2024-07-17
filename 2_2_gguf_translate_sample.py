import argparse
import os
import json
import subprocess

def translate(input_text, config, instruct_str):
    prompt = config['system_prompt'] + "\n\n" + config['prompt_template'].format(instruct=instruct_str, input_str=input_text)
    
    command = [
        str(str(config['llama-cli_path'])),
        '-m', config['model_path'],
        '-e',
        '--temp', str(config['generate_params']['temp']),
        '--repeat-penalty', str(config['generate_params']['repeat_penalty']),
        '-n', str(config['generate_params']['n']),
        '-p', prompt
    ]
    
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error in translation process: {result.stderr}")
    
    return result.stdout.split(config['response_split'])[-1].strip()

def process_files(input_dir, output_dir, config):
    src_files = [f for f in os.listdir(input_dir) if f.endswith('.src')]
    
    if not src_files:
        print("警告: 入力ディレクトリに '.src' ファイルが見つかりませんでした。")
        return
    
    for src_file in src_files:
        input_file_path = os.path.join(input_dir, src_file)
        output_file_path = os.path.join(output_dir, src_file.replace('.src', '.hyp'))
        
        with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
            for line in infile:
                line = line.strip()
                if not line:
                    continue
                
                file_name = os.path.basename(input_file_path)
                if 'enja' in file_name:
                    instruct_str = "Translate English to Japanese."
                elif 'jaen' in file_name:
                    instruct_str = "Translate Japanese English."
                else:
                    raise ValueError("Filename must contain either 'enja' or 'jaen' to determine the translation direction.")

                translated_text = translate(line, config, instruct_str)
                outfile.write(translated_text + '\n')

def main(input_dir, output_dir, config_file):
    with open(config_file, 'r', encoding='utf-8') as cfg_file:
        config = json.load(cfg_file)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    process_files(input_dir, output_dir, config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate text using a specified model and configuration.")
    parser.add_argument('--input', type=str, required=True, help='Path to the input directory.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output directory.')
    parser.add_argument('--config', type=str, required=True, help='Path to the configuration file.')
    
    args = parser.parse_args()
    
    main(args.input, args.output, args.config)


