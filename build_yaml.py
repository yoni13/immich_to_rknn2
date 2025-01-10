import yaml
import time
from get_correct_models import get_corrected_models

# Define target platforms
target_platforms = ['rk3566', 'rk3588']

# Read the YAML file
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
        build_detection_step = {
            'name': f'Run detection build script for {repo_name[i]} on {platform}',
            'run': f'python3 build_rknn.py {repo_name[i]}/detection/model.onnx {platform}'
        }

        build_recognition_step = {
            'name': f'Run recognition build script for {repo_name[i]} on {platform}',
            'run': f'python3 build_rknn.py {repo_name[i]}/recognition/model.onnx {platform}'
        }

        upload_detection_step = {
            'name': f'Upload detection artifact for {repo_name[i]} on {platform}',
            'uses': 'actions/upload-artifact@v4',
            'with': {
                'name': f'{repo_name[i]}-detection-{platform}.rknn',
                'path': f'{repo_name[i]}/detection/model_{platform}.rknn'  # Assuming build_rknn.py saves with platform name
            }
        }

        upload_recognition_step = {
            'name': f'Upload recognition artifact for {repo_name[i]} on {platform}',
            'uses': 'actions/upload-artifact@v4',
            'with': {
                'name': f'{repo_name[i]}-recognition-{platform}.rknn',
                'path': f'{repo_name[i]}/recognition/model_{platform}.rknn'  # Assuming build_rknn.py saves with platform name
            }
        }

        rm_detection_model_step = {
            'name': f'Remove uploaded detection model for {repo_name[i]} on {platform}',
            'run': f'rm {repo_name[i]}/detection/model_{platform}.rknn'
        }

        rm_recognition_model_step = {
            'name': f'Remove uploaded recognition model for {repo_name[i]} on {platform}',
            'run': f'rm {repo_name[i]}/recognition/model_{platform}.rknn'
        }

        data['jobs']['run-python-script']['steps'].append(build_detection_step)
        data['jobs']['run-python-script']['steps'].append(upload_detection_step)
        data['jobs']['run-python-script']['steps'].append(rm_detection_model_step)

        data['jobs']['run-python-script']['steps'].append(build_recognition_step)
        data['jobs']['run-python-script']['steps'].append(upload_recognition_step)
        data['jobs']['run-python-script']['steps'].append(rm_recognition_model_step)

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
    - facial
  push:
    branches:
    - facial''')

    # add time to the end of the file
    file.write('\n\n')
    file.write(f'# Last updated at: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} using build_yaml.py, do not edit manually')