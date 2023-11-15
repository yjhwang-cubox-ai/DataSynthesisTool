import random
import numpy as np
from datetime import datetime, timedelta
from utils.file_utils import *


class Generator:
    def __init__(self, config):
        self.kor_lname_list = None
        self.korean_fname_male_list = None
        self.korean_fname_female_list = None
        self.ch_word_list = None
        self.address_front_list = None
        self.address_back_list = None
        
        self.gender = None
        self.age = None        
        self.Information = ['주민등록증']
        self.Id_information = {
                            'type' : ['주민등록증'],
                            'name' : [],
                            'chinese_name' : [],
                            'resident_registration_number' : [],
                            'address': [],
                            'issue_date': [],
                            'issuing_authority': [],
                            }
        
        self.read_name_inform(config)
        self.read_address_inform(config)
        
    def randomGenerator(self):      
        self.defineGender()
        self.defineAge()
        self.genName()
        self.genChName()
        self.genResidentRegistrationNumber()
        self.genAddress()
    
    def read_name_inform(self, config):
        list_ = read_csv(config["korean_lastname_list"])
        self.kor_lname_list = [line[0] for line in list_]
        list_ = read_csv(config["korean_firstname_male_list"])
        self.korean_fname_male_list = [line[0] for line in list_[1:]]
        list_ = read_csv(config["korean_firstname_female_list"])
        self.korean_fname_female_list = [line[0] for line in list_[1:]]
        list_ = read_csv(config["ch_word_list"])
        self.ch_word_list = [line[0] for line in list_]
    
    def read_address_inform(self, config):
        list_ = read_csv(config["address_front"])
        self.address_front_list = [line[0] for line in list_]
        list_ = read_csv(config["address_back"])
        self.address_back_list = [line[0] for line in list_]    
    
    def defineGender(self):
        if random.random() > 0.5:
            self.gender = 'male'
        else:
            self.gender = 'female'
    
    def defineAge(self):
        total = 50133493 - 6175946 # total: 50133493 / 0-14:6175946
    
        # 0-4, 5-9, 10-14 [1684917,2238916, 2252113]
        num_per_ages = [2422002, 3193316,3423231,                          # 15-19,20-24,25-29
                        3032832,3594213, 3758298,4195327, 4245683,4091920,  # -34,-39,-44,-49,-54,-59
                        3795217,2685773, 2009542,1593192, 1115804,562068,   # -64,-69,-74,-79,-84,-89
                        192149,41399, 5581]                                 # -94,-99,100-
        # _rate_per_ages = [floor(n/_total*10e4)/10e4 for n in _num_per_ages]
        rate_per_ages = [n/total for n in num_per_ages]
        
        # generate random number based on the distribution
        index = np.random.choice(len(rate_per_ages), p=rate_per_ages)

        self.age = index*5 + 17
    
    def genName(self):
        if self.gender == 'male':
            fname_idx = np.random.choice(len(self.korean_fname_male_list), 1)[0]
            f_name = self.korean_fname_male_list[fname_idx]
        else:
            fname_idx = np.random.choice(len(self.korean_fname_male_list), 1)[0]
            f_name = self.korean_fname_male_list[fname_idx]
        l_name = random.sample(self.kor_lname_list, 1)[0]
        self.Information.append(l_name+f_name)
        self.Id_information['name'].append(l_name + f_name)
    
    def genChName(self):
        len_charactor = len(self.Id_information['name'][0])
        ch_idx = np.random.choice(len(self.ch_word_list), len_charactor)
        
        ch_name = ''.join([self.ch_word_list[n] for n in ch_idx])
        self.Id_information['chinese_name'].append('('+ch_name+')')
        
    def genResidentRegistrationNumber(self):
        birth_year = datetime.now().year - random.randint(self.age-2, self.age+3)
        start = datetime(birth_year, 1, 1, 00, 00, 00)
        end = start + timedelta(days=365)
        random_date = start + (end - start) * random.random()
        
        birth_date = [str(random_date.year), str(random_date.month), str(random_date.day)]
        
        regi_number = ''
        
        for num in birth_date:
            if len(num) == 4:
                regi_number += num[2:]
            elif len(num) == 1:
                regi_number += '0' + num
            else:
                regi_number += num
                
        regi_number += '-'
        
        backnumber = ''.join(list(str(random.randint(0, 9)) for _ in range(6)))
        if self.gender == 'male':
            if int(birth_date[0]) >= 2000:
                backnumber = '3'+backnumber
            else:
                backnumber = '1'+backnumber
        else:
            if int(birth_date[0]) >= 2000:
                backnumber = '4'+backnumber
            else:
                backnumber = '2'+backnumber
        
        regi_number += backnumber
        self.Information.append(regi_number)
        self.Id_information['resident_registration_number'].append(regi_number)
        
    def genAddress(self):
        front_idx = np.random.choice(len(self.address_front_list))
        front_fix = self.address_back_list[front_idx]
        
        print(front_fix)