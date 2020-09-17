import json
import os
from copy import deepcopy
from tqdm import tqdm

def load_json(path):
    return json.load(open(path, 'r'))

def save_json(data, path):
    return json.dump(data, open(path, 'w'))

def apply_patch_on_split(split_data, split_patch):
    patched_split = []
    for instance in tqdm(split_data):
        instance_id = instance['id']
        if instance_id in split_patch.keys():
            new_instance = deepcopy(instance)
            new_instance['relation'] = split_patch[instance_id]
            patched_split.append(new_instance)
    return patched_split

def apply_patches(split_dir, patch_dir, split_names=['train', 'dev', 'test']):
    patches = {name: None for name in split_names}
    for name in split_names:
        # Set paths
        split_path = os.path.join(split_dir, name + '.json')
        patch_path = os.path.join(patch_dir, name + '_id2label.json')
        # Load data
        split_data = load_json(split_path)
        patch_id2label = load_json(patch_path)
        patch = apply_patch_on_split(split_data, patch_id2label)
        patches[name] = patch
    return patches

def save_patches(patch2data, save_dir):
    for patch_name, data in patch2data.items():
        save_path = os.path.join(save_dir, patch_name + '.json')
        save_json(data, save_path)

if __name__ == '__main__':
    tacred_dir = None # Directory where TACRED is stored
    patch_dir = os.getcwd() # Directory where patches are located
    save_dir = None # Directory where patched data should be saved
    os.makedirs(save_dir, exist_ok=True)
    # Apply patches on data splits
    patch2data = apply_patches(split_dir=tacred_dir, patch_dir=patch_dir)
    # Save patched data to desired directory
    save_patches(patch2data=patch2data, save_dir=save_dir)