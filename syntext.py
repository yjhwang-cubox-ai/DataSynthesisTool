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
        self.birth_year = None
        self._front_arr_ = None
        
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
        self.clear_inform() # 추후 Id_information 필요없으면 없앨 것
        self.defineGender()
        self.defineAge()
        self.genName()
        self.genChName()
        self.genResidentRegistrationNumber()
        self.genAddress()
        self.genISSDate()
    
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
        self.address_back_list = [line for line in list_]    
    
    def clear_inform(self):
        self.Id_information['name'].clear()
        self.Id_information['chinese_name'].clear()
        self.Id_information['resident_registration_number'].clear()
        self.Id_information['address'].clear()
        self.Id_information['issue_date'].clear()
        self.Id_information['issuing_authority'].clear()
    
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
        self.birth_year = datetime.now().year - random.randint(self.age-2, self.age+3)
        start = datetime(self.birth_year, 1, 1, 00, 00, 00)
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
        front_fix = self.address_front_list[front_idx]
        front_arr = front_fix.split(' ')
        self._front_arr_ = front_arr[:2]
        
        back_idx = np.random.choice(len(self.address_back_list))
        back_arr = self.address_back_list[back_idx]
        
        _bld_add = self.__setBLDAddress()
        
        if random.random() < 0.75: #ROAD part
            print(back_arr[3])
            if back_arr[3] == '0':
                back_road_num = back_arr[2]
            else:
                back_road_num = '-'.join([back_arr[2], back_arr[3]])
            back_road = ' '.join([back_arr[0], back_road_num])
            
            if _bld_add != '':
                back_fix = back_road + ', ' + _bld_add
            else:
                back_fix = back_road
            
            # proc '동', '리'
            if front_arr[-1][-1] == '동':
                front_dong = front_arr[-1]
                front_fix = ' '.join(front_arr[:-1])                
                back_fix = back_fix + ' (' + front_dong + ', ' + back_arr[1] + ')' 
            elif front_arr[-1][-1] == '리':
                front_fix = ' '.join(front_arr[:-1])
                back_fix = back_fix + ' (' + back_arr[1] + ')'
        else:   # LOT part
            if back_arr[5] == '0':
                back_fix = back_arr[4]
            else:
                back_fix = '-'.join([back_arr[4], back_arr[5]])

            if _bld_add != '':
                back_fix = back_fix + ', ' + _bld_add
            else:
                back_fix = back_fix
        
        long_address = ' '.join([front_fix, back_fix])
        self.Id_information['address'].append(long_address)
    
    def __setBLDAddress(self):
        """ Determine the building number and room number
            Output  : (str)_bld_add
            Description : 
                Probabilistically, 60% is set to return the building number and room number, 
                25% to return the building number, floor, and room number, 
                and the remainder to return nothing.
        """
        rand = random.random()
        
        max_danji = 15
        max_dong = 30
        max_floor = 60
        max_ho = 20
        
        # 랜덤 값 부여
        danji = str(random.randint(0, max_danji))
        dong = str(random.randint(1, max_dong))
        floor = str(random.randint(1, max_floor))
        ho = str(random.randint(1, max_ho))
        
        if danji == 0:
            dong = dong
        else:
            dong = danji + dong
        
        if len(ho) == 1:
            ho = floor+'0'+ho
        else:
            ho = floor+ho
        
        # set building address
        if rand < 0.60:   # 동 호
            _bld_add = f'{dong}동 {ho}호'
        elif rand < 0.85: # 동 층 호
            _bld_add = f'{dong}동 {floor}층 {ho}호'
        else:   # pass
            _bld_add = ''
        return _bld_add
    
    def genISSDate(self):
        min_year = self.birth_year +17
        max_year = datetime.now().year
        
        start = datetime(min_year, 1, 1, 00, 00, 00)
        years = max_year - min_year + 1
        end = start + timedelta(days=365 * years)
        
        random_date = start + (end - start) * random.random()
        date = f'{random_date.year}. {random_date.month}. {random_date.day}.'
        
        self.Id_information['issue_date'].append(date)