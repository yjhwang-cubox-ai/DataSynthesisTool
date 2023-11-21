import multiprocessing
import argparse
from tqdm import tqdm

from utils.file_utils import *
from utils.text_utils import *

from utils import syntext

from time import time

def work(p_list):
    json = 'data_config.json'
    config = load_config(json)
        
    generator = syntext.Generator(config["id"])
    
    data_count = config["id"]["data_count"]
        
    data_quarter = data_count // 16
    i = p_list
    
    print(f"{i}-th process start!")
    
    for idx in tqdm(range(data_quarter * i, data_quarter * i + data_quarter)):
        
        fidx = f'{idx:08}'
        fname = f'{fidx}.jpg'
        
        generator.randomGenerator()
        generator.DrawTextOnTemplate(fname)
        generator.saveAnnotation(fidx)

def main():
    
    tic= time()
    
    p_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
   
    pool = multiprocessing.Pool(processes=16)
    pool.map(work, p_list)
    
    pool.close()
    pool.join()
    
    print(time() - tic)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    main()
    
    