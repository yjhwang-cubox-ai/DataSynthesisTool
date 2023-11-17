import multiprocessing
import argparse

from utils.file_utils import *
from utils.text_utils import *

import syntext

from time import time

def work(p_list):
    generator = p_list[0]
    data_quarter = p_list[1] // 4
    i = p_list[2]
    
    for idx in range(data_quarter * i, data_quarter * i + data_quarter):
        fidx = f'{idx:08}'
        fname = f'{fidx}.jpg'
        
        generator.randomGenerator()
        generator.DrawTextOnTemplate(fname)
        generator.saveAnnotation(fidx)

def main():
    json = 'data_config.json'
    config = load_config(json)
        
    generator = syntext.Generator(config["id"])
    
    tic= time()
    
    data_count = config["id"]["data_count"]
    p_list = [[generator, data_count, 0], [generator, data_count, 1], [generator, data_count, 2], [generator, data_count, 3]]
    pool = multiprocessing.Pool(processes=4)
    pool.map(work, p_list)
    
    pool.close()
    pool.join()
    
    print(time() - tic)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    main()
    
    