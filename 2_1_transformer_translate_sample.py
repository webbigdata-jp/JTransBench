import argparse
import glob
import os
import torch
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

def load_model(config):
    model = AutoModelForCausalLM.from_pretrained(config['model_id'], torch_dtype=torch.bfloat16, device_map="auto")
    if 'peft_model_id' in config and config['peft_model_id']:
        model = PeftModel.from_pretrained(model=model, model_id=config['peft_model_id'])

    tokenizer = AutoTokenizer.from_pretrained(config['model_id'])
    return model, tokenizer

def translate(model, tokenizer, text, config, instruct_str):
    prompt = config['system_prompt'] + "\n\n" + config['prompt_template'].format(instruct=instruct_str, input_str=text)
    input_ids = tokenizer(prompt, return_tensors="pt", padding=True, 
            max_length=config['tokenizer_params']['max_length'], truncation=True).input_ids.cuda()

    generate_params = config['generate_params']
    generated_ids = model.generate(input_ids=input_ids, **generate_params)
    full_outputs = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    #print(full_outputs)
    return full_outputs[0].split(config['response_split'])[-1].strip()


def process_files(input_dir, output_dir, config):
    model, tokenizer = load_model(config)

    src_files = [f for f in os.listdir(input_dir) if f.endswith('.src')]

    if not src_files:
        print("Warning: No .src files found in the directory {input_dir}")
        return

    for src_file in src_files:
        input_file_path = os.path.join(input_dir, src_file)
        output_file_path = os.path.join(output_dir, src_file.replace('.src', '.hyp'))
        print(f"translating [{src_file}].")

        with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
            for line in infile:
                line = line.strip()
                if not line:
                    continue

                file_name = os.path.basename(input_file_path)
                if 'enja' in file_name:
                    instruct_str = "Translate English to Japanese."
                elif 'jaen' in file_name:
                    instruct_str = "Translate Japanese to English."
                else:
                    raise ValueError("Filename must contain either 'enja' or 'jaen' to determine the translation direction.")

                translated_text = translate(model, tokenizer, line, config, instruct_str)
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




