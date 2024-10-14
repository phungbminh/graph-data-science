import json
from helper.encode import NumpyEncoder
import pandas as pd
import os
def make_conversion(edge_index):
    old_keys = list(edge_index.keys())
    for old_name in old_keys:
        new_name = "--".join(old_name)
        edge_index[new_name] = edge_index[old_name]
        del edge_index[old_name]
    return edge_index

def read_mapping(mapping_path):
    mapping_dir = os.getcwd() + "/dataset/ogbl_biokg/mapping"
    mapping = pd.read_csv(os.path.join(mapping_dir, mapping_path))
    mapping['Type'] = mapping_path.split('_')[0]
    return mapping

def mapfing_df():
    mapping_dir = os.getcwd() + "/dataset/ogbl_biokg/mapping"
    mappings_files = [f for f in os.listdir(mapping_dir) if 'entidx2name' in f]
    mappings = pd.concat([read_mapping(f,) for f in mappings_files])
    mappings.rename(columns={"ent idx": "Index", "ent name": "Name"}, inplace=True)
    mappings['Label'] = mappings.apply(lambda row: f"{row['Type']}_{row['Index']}", axis=1)
    return mappings
# Hàm chuyển đổi danh sách cạnh
def convert_biokg(sub_kg, sub_label):
    split_label = sub_label.split('--')
    origin_label = [f"{split_label[0]}_{x}" for x in sub_kg[0]]
    destination_label = [f"{split_label[2]}_{x}" for x in sub_kg[1]]
    return pd.DataFrame({
        'Origin': origin_label,
        'Destination': destination_label,
        'OriginType': split_label[0],
        'DestinationType': split_label[2],
        'EdgeType': split_label[1]
    })

def load_edge_df():
    json_ir = os.getcwd() + '/edge_index.json'
    with open(json_ir, 'r') as f:
        biokg = json.load(f)
        # Chuyển đổi danh sách cạnh
    biokg_edge_list = pd.concat([convert_biokg(biokg[key], key) for key in biokg])
    return biokg_edge_list

def load_node_df(biokg_edge_list):
    # Tạo danh sách nút
    biokg_node_list = pd.DataFrame({
        'Node': pd.concat([biokg_edge_list['Origin'], biokg_edge_list['Destination']]).unique()
    })
    biokg_node_list['NodeType'] = biokg_node_list['Node'].apply(lambda x: x.split('_')[0])
    # Thêm tên nút
    mappings = mapfing_df()
    biokg_node_list = biokg_node_list.merge(mappings[['Label', 'Name']], left_on='Node', right_on='Label', how='left')
    biokg_node_list.rename(columns={'Name': 'NodeName'}, inplace=True)

    return biokg_node_list

def bioKGEdgeList(graph):
    edge_index = graph["edge_index_dict"].copy()
    edge_index = make_conversion(edge_index)
    edge_index_json = json.dumps(edge_index, cls=NumpyEncoder)
    json_ir = os.getcwd() + '/edge_index.json'
    if not os.path.exists(json_ir):
        with open('./edge_index.json', 'a') as f:
            f.write(edge_index_json + '\n')
    return load_edge_df()