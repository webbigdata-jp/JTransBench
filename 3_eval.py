import os
import subprocess
from glob import glob

work_dir = 'work'
model_path = 'models/flores200_sacrebleu_tokenizer_spm.model'
spm_script_path = 'external/fairseq/scripts/spm_encode.py'

# Find all *hyp and *ref files in the work directory
hyp_files = glob(os.path.join(work_dir, '*.hyp'))
ref_files = glob(os.path.join(work_dir, '*.ref'))

# Run spm_encode.py on each hyp file
for hyp_file in hyp_files:
    output_file = hyp_file + '.out'
    subprocess.run(['python', spm_script_path,
                    '--model', model_path,
                    '--output_format=piece',
                    '--inputs', hyp_file,
                    '--outputs', output_file])

# Run spm_encode.py on each ref file
for ref_file in ref_files:
    output_file = ref_file + '.out'
    subprocess.run(['python', spm_script_path,
                    '--model', model_path,
                    '--output_format=piece',
                    '--inputs', ref_file,
                    '--outputs', output_file])

# Run sacrebleu with chrf metric
for hyp_file in hyp_files:
    ref_file = hyp_file.replace('.hyp', '.ref')
    hyp_out_file = hyp_file + '.out'
    ref_out_file = ref_file + '.out'
    chrf_output_file = hyp_file + '.chrf'

    if os.path.exists(ref_out_file) and os.path.exists(hyp_out_file):
        with open(chrf_output_file, 'w') as output:
            subprocess.run(['sacrebleu', '-m', 'chrf', '--chrf-word-order', '2', ref_out_file], stdin=open(hyp_out_file), stdout=output)

# Run sacrebleu with spBLEU metric
for hyp_file in hyp_files:
    ref_file = hyp_file.replace('.hyp', '.ref')
    spBLEU_output_file = hyp_file + '.spBLEU'

    if os.path.exists(ref_file):
        with open(spBLEU_output_file, 'w') as output:
            subprocess.run(['sacrebleu', ref_file, '-w', '2', '-tok', 'ja-mecab'], stdin=open(hyp_file), stdout=output)

# Run comet-score
for hyp_file in hyp_files:
    ref_file = hyp_file.replace('.hyp', '.ref')
    src_file = hyp_file.replace('.hyp', '.src')
    comet_output_file = hyp_file + '.comet'
    xlcomet_output_file = hyp_file + '.xlcomet'
    xxlcomet_output_file = hyp_file + '.xxlcomet'

    if os.path.exists(ref_file) and os.path.exists(src_file):
        subprocess.run(['comet-score', '-s', src_file, '-t', hyp_file, '-r', ref_file, '--batch_size', '32'], stdout=open(comet_output_file, 'w'))
        #subprocess.run(['comet-score', '-s', src_file, '-t', hyp_file, '-r', ref_file, '--batch_size', '2', '--model', 'Unbabel/XCOMET-XL'], stdout=open(xlcomet_output_file, 'w'))
        #subprocess.run(['comet-score', '-s', src_file, '-t', hyp_file, '-r', ref_file, '--batch_size', '2', '--model', 'Unbabel/XCOMET-XXL'], stdout=open(xxlcomet_output_file, 'w'))




