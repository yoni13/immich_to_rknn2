
import argparse

parser = argparse.ArgumentParser("simple_example")
parser.add_argument("model", help="Path of the model that will be exported to rknn format.", type=str)
parser.add_argument("target_platform", help="target platform ex:rk3566", type=str)
args = parser.parse_args()

ONNX_MODEL = args.model

if not ONNX_MODEL:
    print("Please provide a model path.")
    exit(1)

from rknn.api import RKNN
rknn = RKNN(verbose=False)
rknn.config(target_platform=args.target_platform)
ret = rknn.load_onnx(model=ONNX_MODEL)

if ret != 0:
    print("Load failed!")
    exit(ret)

ret = rknn.build(do_quantization=False)

if ret != 0:
    print("Build failed!")
    exit(ret)

ret = rknn.export_rknn(ONNX_MODEL.replace('model.onnx',f'model_{args.target_platform}.rknn'))
if ret != 0:
        print('Export rknn model failed!')
        exit(ret)
print('done')

