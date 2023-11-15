import argparse

from utils.file_utils import *
import syntext


def main():
    json = 'data_config.json'
    config = load_config(json)
        
    generator = syntext.Generator(config["id"])
    
    for _ in range(3):
    
        generator.randomGenerator()
        print(generator.gender)
        print(generator.age)
        print(generator.Id_information)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    main()
    
    