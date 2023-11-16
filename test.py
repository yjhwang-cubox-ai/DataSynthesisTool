import argparse

from utils.file_utils import *
from utils.text_utils import *

import syntext


def main():
    json = 'data_config.json'
    config = load_config(json)
        
    generator = syntext.Generator(config["id"])
    
    for idx in range(20):
        fidx = f'{idx:08}'
        fname = f'{fidx}.jpg'
        
        text_info = generator.randomGenerator()
        texts, fonts = set_Text_Font(text_info, config["id"])
        DrawTextOnTemplate(texts, fonts, config["id"], fname)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    main()
    
    