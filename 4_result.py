import os
import json

def get_score_from_spbleu(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get('score', '')
    except Exception as e:
        return ''

def get_score_from_chrf(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get('score', '')
    except Exception as e:
        return ''

def get_score_from_comet(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1]
                if 'score:' in last_line:
                    return float(last_line.split('score:')[1].strip())
        return ''
    except Exception as e:
        return ''

# Initialize result storage
results = []

# Define the directory to scan
work_dir = 'work'

# Find all relevant files in the work directory
for file_name in os.listdir(work_dir):
    if file_name.endswith('.hyp.spBLEU'):
        base_name = file_name.replace('.hyp.spBLEU', '')
        spBLEU_score = get_score_from_spbleu(os.path.join(work_dir, file_name))
        chrf_score = get_score_from_chrf(os.path.join(work_dir, base_name + '.hyp.chrf'))
        comet_score = get_score_from_comet(os.path.join(work_dir, base_name + '.hyp.comet'))
        xlcomet_score = get_score_from_comet(os.path.join(work_dir, base_name + '.hyp.xlcomet'))
        xxlcomet_score = get_score_from_comet(os.path.join(work_dir, base_name + '.hyp.xxlcomet'))
        parts = base_name.split('_')
        bench_name = parts[0]
        
        results.append({
            'filename': bench_name,
            'direction': 'jaen' if 'jaen' in base_name else 'enja',
            'spBLEU': spBLEU_score,
            'chrF2++': chrf_score,
            'comet': comet_score,
            'xlcomet': xlcomet_score,
            'xxlcomet': xxlcomet_score
        })

# Print the header
print("filename direction spBLEU chrF2++ comet xlcomet xxlcomet")

# Print each result
for result in results:
    print(f"{result['filename']} {result['direction']} {result['spBLEU']} {result['chrF2++']} {result['comet']} {result['xlcomet']} {result['xxlcomet']}")


