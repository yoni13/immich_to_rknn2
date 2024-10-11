import yaml
import time

# 讀取 YAML 檔案
with open('base.yml', 'r') as file:
    data = yaml.safe_load(file)
    file.close()

repo_name = ['ViT-L-16-SigLIP-384__webli']
repo_url = ['https://huggingface.co/immich-app/ViT-L-16-SigLIP-384__webli']

for i in range(len(repo_name)):

    clone_step = {
        'name': 'Clone model',
        'run': 'git clone ' + repo_url[i]
    }

    build_textual_step = {
        'name': 'Run textual build script',
        'run': 'python build_rknn.py '+ repo_name[i] + '/textual/model.onnx'
    }

    build_visual_step = {
        'name': 'Run visual build script',
        'run': 'python build_rknn.py '+ repo_name[i] + '/visual/model.onnx'
    }

    upload_textual_step = {
        'name': 'Upload textual artifact',
        'uses': 'actions/upload-artifact@v4',
        'with': {
            'name': repo_name[i]+'-textual.rknn',
            'path': repo_name[i]+'/textual/model.rknn'
        }
    }

    upload_visual_step = {
        'name': 'Upload visual artifact',
        'uses': 'actions/upload-artifact@v4',
        'with': {
            'name': repo_name[i]+'-visual.rknn',
            'path': repo_name[i]+'/visual/model.rknn'
        }
    }

    rm_textual_model_step = {
        'name': 'Remove uploaded textual model',
        'run': 'rm ' + repo_name[i] + '/textual/model.rknn'
    }

    rm_visual_model_step = {
        'name': 'Remove uploaded visual model',
        'run': 'rm ' + repo_name[i] + '/visual/model.rknn'
    }


    data['jobs']['run-python-script']['steps'].append(clone_step)

    data['jobs']['run-python-script']['steps'].append(build_textual_step)
    data['jobs']['run-python-script']['steps'].append(upload_textual_step)
    data['jobs']['run-python-script']['steps'].append(rm_textual_model_step)

    data['jobs']['run-python-script']['steps'].append(build_visual_step)
    data['jobs']['run-python-script']['steps'].append(upload_visual_step)
    data['jobs']['run-python-script']['steps'].append(rm_visual_model_step)

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
    - main
  push:
    branches:
    - main''')
    
    # add time to the end of the file
    file.write('\n\n')
    file.write(f'# Last updated at: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} using build_yaml.py, do not edit manually')
    file.close()