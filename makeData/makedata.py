import random

def read_txt(path, encoding='cp949'):
    f = open(path, "r", encoding=encoding)
    
    lst = []
    while True:
        line = f.readline().strip()
        if not line: break
        lst.append(line)
    
    return lst

def synth_name():
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
    
    return name_merged
    
def synth_idnum():
    idnum = []
    for i in range(14):
        
        if i == 6:
            idnum.append('-')
        elif i == 7:
            randi = random.randint(1,2)
            idnum.append(randi)
        else:
            randint = random.randint(0,9)
            idnum.append(randint)
    return idnum

def main():
    syn_name = synth_name()
    syn_idnum = synth_idnum()
    
    print(syn_name)
    print(syn_idnum)

if __name__ == "__main__":
    main()