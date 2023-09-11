import cv2
import numpy as np
import os

def parse_folder(folder_path: str) -> dict:
    all_files: list = os.listdir(folder_path)
    data = {}
    
    for file_name in all_files:
        full_file_name: str = os.path.join(folder_path, file_name)
        if os.path.isfile(full_file_name):
            data[full_file_name] = cv2.imread(full_file_name)
     
    return data        

def is_similar(image1: np.ndarray, image2: np.ndarray) -> bool:
    return image1.shape == image2.shape and not(np.bitwise_xor(image1,image2).any())

def is_one_similar(original_image: np.ndarray, images: dict.values) -> bool:
    for image in images:
        if is_similar(original_image, image):
            return True
    return False    

def compare_folder_dicts(folder_dict1: dict, folder_dict2: dict) -> bool:
    for key_dict1 in folder_dict1.keys():
        if is_one_similar(folder_dict1[key_dict1], folder_dict2.values()): 
            return True 
    return False    

def exit_cv2() -> None:
    cv2.destroyAllWindows()