import argparse
import os
import onnx

from numpy import cumsum
from rknn.api.custom_op import get_node_attr

class RKCumSum:
    # Just CumSum with a different name so it wont conflict
    op_type = "RKCumSum"

    def shape_infer(self, node, in_shapes, in_dtypes):
        return in_shapes.copy(), in_dtypes.copy()

    def compute(self, node, inputs):
        x = inputs[0]
        axis = get_node_attr(node, "axis")
        return [cumsum(x, axis=axis)]


# Function to modify the ONNX model
def modify_onnx_change_op_type(input_onnx_path, output_onnx_path, old_op_type, new_op_type):
    print(f"Loading ONNX model: {input_onnx_path}")
    model = onnx.load(input_onnx_path)
    graph = model.graph
    nodes_changed = 0
    new_nodes = []

    for node in graph.node:
        if node.op_type == old_op_type:
            print(f"  Found node '{node.name}' with op_type '{old_op_type}'. Changing to '{new_op_type}'.")
            # Create a new node with the new op_type, keeping everything else
            new_node = onnx.helper.make_node(
                new_op_type,         # New operator type
                node.input,          # Same inputs
                node.output,         # Same outputs
                name=node.name,      # Keep the original name if desired
                # Copy attributes (important for axis in CumSum)
                **{attr.name: onnx.helper.get_attribute_value(attr) for attr in node.attribute}
            )
            new_nodes.append(new_node)
            nodes_changed += 1
        else:
            # Keep nodes that don't match the old_op_type
            new_nodes.append(node)

    if nodes_changed > 0:
        # Remove old nodes
        graph.ClearField("node")
        # Add the modified list of nodes
        graph.node.extend(new_nodes)

        # Optional: Check model validity after modification
        try:
            onnx.checker.check_model(input_onnx_path)
            print("ONNX model check passed after modification.")
        except onnx.checker.ValidationError as e:
            print(f"ONNX model check failed after modification: {e}")
            # Decide if you want to proceed despite validation error

        print(f"Saving modified ONNX model to: {output_onnx_path}")
        onnx.save(model, output_onnx_path)
        print(f"Successfully changed {nodes_changed} nodes from '{old_op_type}' to '{new_op_type}'.")
        return True # Indicate modification happened
    else:
        print(f"No nodes with op_type '{old_op_type}' found. No modifications made.")
        # Copy original to output if you want the script to always produce the output file
        # import shutil
        # shutil.copyfile(input_onnx_path, output_onnx_path)
        return False # Indicate no modification happened


parser = argparse.ArgumentParser("RKNN model converting")
parser.add_argument("model", help="Directory of the model that will be exported to RKNN ex:ViT-B-32__openai.", type=str)
parser.add_argument("target_platform", help="target platform ex:rk3566", type=str)
args = parser.parse_args()


def ConvertModel(model_path='ViT-B-32__openai/textual/model.onnx', target_platform='rk3566', dynamic_input = None):
    # E build: Repeat call the 'rknn.build' or 'rknn.hybrid_quantization_step1' is not allow!
    from rknn.api import RKNN
    rknn = RKNN(verbose=False)

    rknn.config(target_platform=target_platform, dynamic_input=dynamic_input)

    modified_onnx_path = model_path.replace('.onnx', '_mycumsum.onnx')
    modified = modify_onnx_change_op_type(model_path, modified_onnx_path, "CumSum", "RKCumSum")
    onnx_to_load = modified_onnx_path if modified else model_path
    if modified:
        ret = rknn.reg_custom_op(RKCumSum())

        if ret != 0:
            raise RuntimeError("Register Custom OP failed!")


    ret = rknn.load_onnx(model=onnx_to_load)

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

    if not os.path.isfile(f'{model_path.replace("onnx","rknn")}'):
        print(f'Dummy model not found at {model_path.replace("onnx","rknn")}, creating one')
        with open(f'{model_path.replace("onnx","rknn")}', 'w'):
            pass


if os.path.isdir(f'{args.model}/textual') and os.path.isdir(f'{args.model}/visual'): # is a clip model
    print('Converting Clip model.')
    ConvertModel(model_path=f'{args.model}/textual/model.onnx', target_platform=args.target_platform)
    ConvertModel(model_path=f'{args.model}/visual/model.onnx', target_platform=args.target_platform)

elif os.path.isdir(f'{args.model}/detection') and os.path.isdir(f'{args.model}/recognition'): # is a facial model
    print('Converting facial model.')
    ConvertModel(f'{args.model}/detection/model.onnx', args.target_platform, [[[1, 3, 640, 640]]])
    ConvertModel(f'{args.model}/recognition/model.onnx', args.target_platform, [[[1, 3, 112, 112]]])

else:
    print('Unknown model.')
