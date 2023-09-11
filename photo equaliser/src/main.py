from photo_equaliser import *
import sys

# python main.py ../photos1 ../photos2

def main() -> None:
    args: list = sys.argv[1:]
    folder_dict1: dict = parse_folder(args[0])
    folder_dict2: dict = parse_folder(args[1])
    print(compare_folder_dicts(folder_dict1, folder_dict2))
    
    exit_cv2()
    
if __name__ == "__main__":
    main()    