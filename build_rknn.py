import argparse
import os
parser = argparse.ArgumentParser("RKNN model converting")
parser.add_argument("model", help="Directory of the model that will be exported to rknn format ex:ViT-B-32__openai.", type=str)
parser.add_argument("target_platform", help="target platform ex:rk3566", type=str)
args = parser.parse_args()


def ConvertModel(model_path='ViT-B-32__openai/textual/model.onnx', target_platform='rk3566', dynamic_input = None):
    # E build: Repeat call the 'rknn.build' or 'rknn.hybrid_quantization_step1' is not allow!
    from rknn.api import RKNN
    rknn = RKNN(verbose=False)

    rknn.config(target_platform=target_platform, dynamic_input=dynamic_input)
    ret = rknn.load_onnx(model=model_path)

    if ret != 0:
        print("Load failed!")
        exit(ret)

    ret = rknn.build(do_quantization=False)

    if ret != 0:
        print("Build failed!")
        exit(ret)
    print(model_path.replace('model.onnx',f'{target_platform}.rknn'))
    ret = rknn.export_rknn(model_path.replace('model.onnx',f'{target_platform}.rknn'))
    if ret != 0:
            print('Export rknn model failed!')
            exit(ret)
    print('done')
    del rknn
    del RKNN



if os.path.isdir(f'{args.model}/textual') and os.path.isdir(f'{args.model}/visual'): # is a clip model
    print('Converting Clip model.')
    ConvertModel(model_path=f'{args.model}/textual/model.onnx', target_platform=args.target_platform)
    ConvertModel(model_path=f'{args.model}/visual/model.onnx', target_platform=args.target_platform)

elif os.path.isdir(f'{args.model}/detection') and os.path.isdir(f'{args.model}/recognition'): # is a facial model
    print('Converting facial model.')
    ConvertModel(model_path=f'{args.model}/detection/model.onnx', target_platform=args.target_platform, dynamic_input=[[[1, 3, 640, 640]]])
    # I just used some common faces, if immich only uses one, keep one should be fine
    ConvertModel(model_path=f'{args.model}/recognition/model.onnx', target_platform=args.target_platform, dynamic_input=[[[1, 3, 112, 112]], [[4, 3, 112, 112]], [[8, 3, 112, 112]]])

else:
    print('Unknown model.')