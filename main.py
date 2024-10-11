import os
import subprocess
import shutil
subprocess.run(["git", "lfs", "install"])



def download_and_build_rknn(repo_name,repo_url):
    subprocess.run(["git", "clone", repo_url])
    os.chdir(repo_name)
    if os.path.islink("textual"):
        subprocess.run(["python3", "build_rknn.py", "--model", "textual/model.onnx"])
    if os.path.islink("visual"):
        subprocess.run(["python3", "build_rknn.py", "--model", "visual/model.onnx"])
    subprocess.run(["ls"])
    os.chdir("..")
    shutil.rmtree(repo_name)

download_and_build_rknn("ViT-L-16-SigLIP-384__webli","https://huggingface.co/immich-app/ViT-L-16-SigLIP-384__webli")
