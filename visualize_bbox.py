import argparse
import json
import cv2
import os
from tqdm import tqdm

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label_dir", type=str)
    parser.add_argument("--img_dir", type=str)
    parser.add_argument("--out_dir", type=str)
    return parser.parse_args()

def get_file_list(file_dir):
    file_lists = []
    
    if file_dir is None or not os.path.exists(file_dir):
        raise Exception("not found any file in {}".format(file_dir))
    
    if os.path.isdir(file_dir):
        for single_file in os.listdir(file_dir):
            file_path = os.path.join(file_dir, single_file)
            file_lists.append(file_path)
    
    if len(file_path) == 0:
        raise Exception("not found any file in {}".format(file_dir))
    file_lists = sorted(file_lists)
    
    return file_lists
    
def main():
    
    args = parse()
    
    file_list = get_file_list(args.label_dir)
    
    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)
    
    for idx, file_path in enumerate(tqdm(file_list)):
        f = open(file_path)
        data = json.load(f)
        imgName= data["images"]["file_name"]
        annotations = data["annotations"]
        
        img_path = args.img_dir + '/' + imgName
        
        bbox_list = []
        for anno in annotations:
            item = annotations[anno]
            bbox = item["bbox"]
            bbox_list.append(bbox)
        
        img = cv2.imread(img_path)
        
        for bbox in bbox_list:
            left = int(bbox[0])
            top = int(bbox[1])
            right = int(bbox[2])
            bottom = int(bbox[3])
            img = cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255),3)
            
        output_path = args.out_dir + "/" + imgName
        cv2.imwrite(output_path, img)

if __name__ == '__main__':
    main()
    