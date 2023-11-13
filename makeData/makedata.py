import random

def read_txt(path, encoding='cp949'):
    f = open(path, "r", encoding=encoding)
    
    lst = []
    while True:
        line = f.readline().strip()
        if not line: break
        lst.append(line)
    
    return lst

def main():
    name = []
    last_name = []
    chinese = []
    
    name = read_txt("name_crawling/name_list.txt")
    last_name = read_txt("name_crawling/lastname_list.txt")
    chinese = read_txt("name_crawling/chinese.txt", 'UTF8')
           
    choice_last_name = random.choice(last_name)
    choice_name = random.choice(name)
    choice_chinese = random.sample(chinese, 3)
    
    name_merged = choice_last_name + choice_name + '(' + choice_chinese[0] + choice_chinese[1] + choice_chinese[2] + ')'
    
    
    
    print(last_name)

if __name__ == "__main__":
    main()