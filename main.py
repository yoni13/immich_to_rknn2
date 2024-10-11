import os
import subprocess

subprocess.run(["sudo", "apt-get", "update","-y"])
subprocess.run(["sudo", "apt-get", "install", "git","ffmpeg", "libsm6","libxext6","-y"])
subprocess.run(["git", "lfs", "install"])



def download_and_build_rknn(repo_name,repo_url):
    subprocess.run(["git", "clone", repo_url])
    os.chdir(repo_name)
    if os.dir.exists("textual"):
        subprocess.run(["python3", "build_rknn.py", "--model", "textual/model.onnx"])
    if os.dir.exists("visual"):
        subprocess.run(["python3", "build_rknn.py", "--model", "visual/model.onnx"])
    os.chdir("..")
    os.remove(repo_name)

download_and_build_rknn("ViT-L-16-SigLIP-384__webli","https://huggingface.co/immich-app/ViT-L-16-SigLIP-384__webli")