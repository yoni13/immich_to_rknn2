
import argparse

parser = argparse.ArgumentParser("simple_example")
parser.add_argument("model", help="Path of the model that will be exported to rknn format.", type=str)
args = parser.parse_args()

ONNX_MODEL = args.model

if not ONNX_MODEL:
    print("Please provide a model path.")
    exit(1)

from rknn.api import RKNN
rknn = RKNN(verbose=False)
rknn.config(target_platform='rk3566',dynamic_input=[[[1, 3, 640, 640]]])
ret = rknn.load_onnx(model=ONNX_MODEL)
# input size is from immich/machine-learning/ann/export/run.py

if ret != 0:
    print("Load failed!")
    exit(ret)

ret = rknn.build(do_quantization=False)

if ret != 0:
    print("Build failed!")
    exit(ret)

ret = rknn.export_rknn(ONNX_MODEL.replace('onnx','rknn'))
if ret != 0:
        print('Export rknn model failed!')
        exit(ret)
print('done')

