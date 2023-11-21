import multiprocessing
import argparse
from tqdm import tqdm

from utils import syntext
from utils import file_utils

from time import time

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_dir", type=str)
    parser.add_argument("--num_process", type=int)
    return parser.parse_args()

def work(p_list):    
    args = parse()
    
    config = file_utils.load_config(args.config_dir)
        
    generator = syntext.Generator(config["id"])
    
    data_count = config["id"]["data_count"]
        
    data_quarter = data_count // args.num_process
    i = p_list
    
    print(f"{i}-th process start!")
    
    for idx in tqdm(range(data_quarter * i, data_quarter * i + data_quarter)):
        
        fidx = f'{idx:08}'
        fname = f'{fidx}.jpg'
        
        generator.randomGenerator()
        generator.DrawTextOnTemplate(fname)
        generator.saveAnnotation(fidx)

def main():
    
    args = parse()
    
    tic= time()
    
    p_list = []
    for worker in range(args.num_process):
        p_list.append(worker)
   
    pool = multiprocessing.Pool(processes=args.num_process)
    pool.map(work, p_list)
    
    pool.close()
    pool.join()
    
    print(time() - tic)

if __name__ == '__main__':
    main()
    
    