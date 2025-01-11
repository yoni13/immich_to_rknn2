import yaml
import time
from get_correct_models import get_corrected_models

# Define target platforms
target_platforms = ["rk3562", "rk3566", "rk3568", "rk3576", "rk3588"]

# Read the base YAML file
with open('base.yml', 'r') as file:
    data = yaml.safe_load(file)

repo_name, repo_url = get_corrected_models()

for i in range(len(repo_name)):
    clone_step = {
        'name': f'Clone model {repo_name[i]}',
        'run': f'git clone {repo_url[i]} --depth 1 {repo_name[i]}'
    }
    data['jobs']['run-python-script']['steps'].append(clone_step)

    for platform in target_platforms:
        build_textual_step = {
            'name': f'Run textual build script for {repo_name[i]} on {platform}',
            'run': f'python3 build_rknn.py {repo_name[i]}/textual/model.onnx {platform}'
        }

        build_visual_step = {
            'name': f'Run visual build script for {repo_name[i]} on {platform}',
            'run': f'python3 build_rknn.py {repo_name[i]}/visual/model.onnx {platform}'
        }

        upload_textual_step = {
            'name': f'Upload textual artifact for {repo_name[i]} on {platform}',
            'uses': 'actions/upload-artifact@v4',
            'with': {
                'name': f'{repo_name[i]}-textual-{platform}.rknn',
                'path': f'{repo_name[i]}/textual/model_{platform}.rknn'  # Assuming build_rknn.py names output accordingly
            }
        }

        upload_visual_step = {
            'name': f'Upload visual artifact for {repo_name[i]} on {platform}',
            'uses': 'actions/upload-artifact@v4',
            'with': {
                'name': f'{repo_name[i]}-visual-{platform}.rknn',
                'path': f'{repo_name[i]}/visual/model_{platform}.rknn' # Assuming build_rknn.py names output accordingly
            }
        }

        rm_textual_model_step = {
            'name': f'Remove uploaded textual model for {repo_name[i]} on {platform}',
            'run': f'rm {repo_name[i]}/textual/model_{platform}.rknn'
        }

        rm_visual_model_step = {
            'name': f'Remove uploaded visual model for {repo_name[i]} on {platform}',
            'run': f'rm {repo_name[i]}/visual/model_{platform}.rknn'
        }

        data['jobs']['run-python-script']['steps'].append(build_textual_step)
        data['jobs']['run-python-script']['steps'].append(upload_textual_step)
        data['jobs']['run-python-script']['steps'].append(rm_textual_model_step)

        data['jobs']['run-python-script']['steps'].append(build_visual_step)
        data['jobs']['run-python-script']['steps'].append(upload_visual_step)
        data['jobs']['run-python-script']['steps'].append(rm_visual_model_step)

    if i != (len(repo_name) - 1):
        data['jobs']['run-python-script']['steps'].append({
            'name': f'RM cloned repo {repo_name[i]}',
            'run': f'rm -rf {repo_name[i]}'
        })

# Write back to the YAML file
with open('.github/workflows/main.yml', 'w') as file:
    yaml.safe_dump(data, file)

with open('.github/workflows/main.yml', 'a') as file:
    file.write('''on:
  pull_request:
    branches:
    - main
  push:
    branches:
    - main''')
    file.write('\n\n')
    file.write(f'# Last updated at: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} using build_yaml.py, do not edit manually')