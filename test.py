import argparse

from utils.file_utils import *
from utils.text_utils import *

import syntext


def main():
    json = 'data_config.json'
    config = load_config(json)
        
    generator = syntext.Generator(config["id"])
    
    for _ in range(3):
    
        text_info = generator.randomGenerator()
        set_Text_Font(text_info, config["id"])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    main()
    
    