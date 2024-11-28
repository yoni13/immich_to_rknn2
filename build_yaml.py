import yaml
import time
from get_correct_models import get_corrected_models

# 讀取 YAML 檔案
with open('base.yml', 'r') as file:
    data = yaml.safe_load(file)
    file.close()

repo_name, repo_url = get_corrected_models()

for i in range(len(repo_name)):

    clone_step = {
        'name': 'Clone model',
        'run': 'git clone ' + repo_url[i] + ' --depth 1 '
    }

    build_detection_step = {
        'name': 'Run detection build script',
        'run': 'python build_rknn.py '+ repo_name[i] + '/detection/model.onnx'
    }

    build_recognition_step = {
        'name': 'Run recognition build script',
        'run': 'python build_rknn.py '+ repo_name[i] + '/recognition/model.onnx'
    }

    upload_detection_step = {
        'name': 'Upload detection artifact',
        'uses': 'actions/upload-artifact@v4',
        'with': {
            'name': repo_name[i]+'-detection.rknn',
            'path': repo_name[i]+'/detection/model.rknn'
        }
    }

    upload_recognition_step = {
        'name': 'Upload recognition artifact',
        'uses': 'actions/upload-artifact@v4',
        'with': {
            'name': repo_name[i]+'-recognition.rknn',
            'path': repo_name[i]+'/recognition/model.rknn'
        }
    }

    rm_detection_model_step = {
        'name': 'Remove uploaded detection model',
        'run': 'rm ' + repo_name[i] + '/detection/model.rknn'
    }

    rm_recognition_model_step = {
        'name': 'Remove uploaded recognition model',
        'run': 'rm ' + repo_name[i] + '/recognition/model.rknn'
    }


    data['jobs']['run-python-script']['steps'].append(clone_step)

    data['jobs']['run-python-script']['steps'].append(build_detection_step)
    data['jobs']['run-python-script']['steps'].append(upload_detection_step)
    data['jobs']['run-python-script']['steps'].append(rm_detection_model_step)

    data['jobs']['run-python-script']['steps'].append(build_recognition_step)
    data['jobs']['run-python-script']['steps'].append(upload_recognition_step)
    data['jobs']['run-python-script']['steps'].append(rm_recognition_model_step)

    if i != (len(repo_name) - 1):
        data['jobs']['run-python-script']['steps'].append({
            'name': 'RM cloned repo',
            'run': 'rm -rf ' + repo_name[i]
        })


# 寫回 YAML 檔案
with open('.github/workflows/main.yml', 'w') as file:
    yaml.safe_dump(data, file)
    file.close()

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
    file.close()