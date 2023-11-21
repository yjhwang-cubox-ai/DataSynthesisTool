from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np
import glob
import os
from datetime import datetime, timedelta
import textwrap
from utils.file_utils import *


class Generator:
    def __init__(self, config):
        self.kor_lname_list = None
        self.korean_fname_male_list = None
        self.korean_fname_female_list = None
        self.ch_word_list = None
        self.address_front_list = None
        self.address_back_list = None
        
        self.type = config["type"]
        self.img_width = config["img_width"]
        self.img_height = config["img_height"]
        self.gender = None
        self.age = None
        self.birth_year = None
        self._front_arr_ = None
        
        self.add_hologram = config["add_hologram"]
        self.hologram_ratio = config["hologram_ratio"]
        
        self.fonts_path = []
        self.fonts_info = []
        
        self.template_list = []
        self.hologram_list = []
        
        self.save_img_dir = config["save_image_dir"]
        self.save_anno_dir = config["save_annotation_dir"]
        
        self.Information = []
        self.Id_information = {
                            'type' : [],
                            'name' : [],
                            'chinese_name' : [],
                            'resident_registration_number' : [],
                            'address': [],
                            'issue_date': [],
                            'issue_authority': [],
                            }
        self.bbox_annotation = []
        
        self.read_name_inform(config)
        self.read_address_inform(config)
        self.read_fontpath_infom(config)
        self.read_tamplate_inform(config)
        self.read_hologram_inform(config)
        
    def randomGenerator(self):
        self.clear_inform()
        self.defineType()
        self.defineGender()
        self.defineAge()
        self.genName()
        self.genChName()
        self.genResidentRegistrationNumber()
        self.genAddress()
        self.genISSDate()
        self.genISSAuth()
        self.set_Font()
        # self.DrawTextOnTemplate()
        # self.saveAnnotation()
        
        return self.Id_information
    
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
    
    def read_fontpath_infom(self, config):
        fonts_path = [config["type_font"],
                 config["kor_name_font"],
                 config["ch_name_font"],
                 config["regi_number_font"],
                 config["address_font"],
                 config["issue_date_font"],
                 config["issue_authority_font"]]
        
        self.fonts_path = fonts_path
    
    def read_tamplate_inform(self, config):
        template_dir = config["template_directory"]
        self.template_list = [file for file in glob.glob(template_dir + '/*')]
    
    def read_hologram_inform(self, config):
        hologram_dir = config["hologram_directory"]
        self.hologram_list = [file for file in glob.glob(hologram_dir + '/*')]
        
    ###########################################################################
    
    def clear_inform(self):
        self.Information.clear()
        self.bbox_annotation.clear()
        self.Id_information['name'].clear()
        self.Id_information['chinese_name'].clear()
        self.Id_information['resident_registration_number'].clear()
        self.Id_information['address'].clear()
        self.Id_information['issue_date'].clear()
        self.Id_information['issue_authority'].clear()
        
        
    def defineType(self):
        self.Information.append(self.type)
        self.Id_information['type'].append(self.type)
    
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
        
        self.Information.append('('+ch_name+')')
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
        self.Information.append(long_address)
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
        
        self.Information.append(date)
        self.Id_information['issue_date'].append(date)
        
    def genISSAuth(self):
        if '제주' in self._front_arr_[0]:
            issauth = '제주특별자치도지사'
        else:
            if self._front_arr_[1][-1] == '시':
                issauth = ' '.join(self._front_arr_) + '장'
            elif self._front_arr_[1][-1] == '구':
                issauth = ' '.join(self._front_arr_) + '청장'
            elif self._front_arr_[1][-1] == '군':
                issauth = ' '.join(self._front_arr_) + '수'
            else:
                issauth = ' '.join(self._front_arr_)
        
        self.Information.append(issauth)
        self.Id_information['issue_authority'].append(issauth)
    
    def set_Font(self):
        if len(self.Information[1]) <= 3:
            font_size = [56, 45, 45, 33, 33, 33, 42]
        elif len(self.Information[1]) == 4:
            font_size = [56, 40, 40, 33, 33, 33, 42]
        elif len(self.Information[1]) > 4:
            font_size = [56, 32, 32, 33, 33, 33, 42]
        
        for idx in range(len(self.Information)):
            self.fonts_info.append(ImageFont.truetype(self.fonts_path[idx], font_size[idx]))
    
    def DrawTextOnTemplate(self, fname):
        template_idx = np.random.choice(len(self.template_list))
        template = self.template_list[template_idx]
        
        img = Image.open(template).resize((960,600))
        draw = ImageDraw.Draw(img)
        
        # text
        if len(self.Information[1]) <= 3:
            positions = [(304, 84), (200, 179), (350, 179), (300, 252), (327, 370), (524, 472), (510, 517)]
        elif len(self.Information[1]) == 4:
            positions = [(304, 84), (200, 179), (390, 179), (300, 252), (327, 370), (524, 472), (510, 517)]
        elif len(self.Information[1]) >= 5:
            positions = [(304, 84), (180, 179), (400, 179), (300, 252), (327, 370), (524, 472), (510, 517)]
        
        # total_anno_info = []
        
        # texts = ['부산광역시 부산진구 천자로 386, 1423동 5815호, (가야제1동, 창원 마린, 푸르지오 1단지)']
        # texts = ['전라북도 임실군 관촌면 방수리 222, 020동 3507호']
    
        for idx, text in enumerate(self.Information):        
            if len(text) > 16:
                address = []
                warpped_text = textwrap.wrap(text, width=16)
                if len(warpped_text) > 2:
                    address.append(warpped_text[0])
                    
                    spare_text = ''
                    for i in range(1,len(warpped_text)):
                        spare_text += warpped_text[i]
                    spare_texts = textwrap.wrap(spare_text, width=21)
                    
                    for text_ in spare_texts:
                        address.append(text_)
                else:
                    address = warpped_text
                
                num_txts = len(address)
                text = '\n'.join(address)
                textlength = self.multiline_textsize(draw, text, font=self.fonts_info[idx])
            else:
                num_txts = 1
                textlength = draw.textlength(text, font=self.fonts_info[idx])
            
            x = positions[idx][0] - textlength // 2
            y = positions[idx][1] - self.fonts_info[idx].getbbox(text)[-1]*num_txts // 2
            
            text_bbox = draw.textbbox((x, y), text, font=self.fonts_info[idx])
            # draw.rectangle(text_bbox, outline=(0,255,0))
            
            if '\n' in text:
                splited_text = text.split('\n')
                for splt in splited_text:
                    draw.multiline_text((x,y), splt, fill="black", font=self.fonts_info[idx])
                    splt_bbox = draw.textbbox((x,y), splt, font=self.fonts_info[idx])
                    # draw.rectangle(splt_bbox, outline=(0,0,0))
                    anno_info = self.get_anno_info(draw, x, y, splt, self.fonts_info[idx])
                    self.bbox_annotation += anno_info
                    y += self.fonts_info[idx].getbbox(splt)[-1]
            else:
                draw.multiline_text((x, y), text, fill="black", font=self.fonts_info[idx])
                anno_info = self.get_anno_info(draw, x, y, text, self.fonts_info[idx])
                if anno_info[0]["text"][0] == '(':
                    anno_info[0]["text"] = '(' + len(anno_info[0]["text"][1:-1])*'#' + ')'
                self.bbox_annotation += anno_info
        
        # postprocessing
        if random.random() < 0.5:
            img = self.addFilter(img, template)
        
        if self.add_hologram == True:
            if random.random() < self.hologram_ratio:
                img = self.addHologram(img)        
        
        img_path = os.path.join(self.save_img_dir, fname)
        
        if not os.path.exists(self.save_img_dir):
            os.makedirs(self.save_img_dir)
        
        img.save(img_path)
        # print(f"{img_path} is saved!")
    
    def addFilter(self, img, template):
        filter = Image.open(template).resize((self.img_width,self.img_height)).convert("RGBA")
        
        alpha_data = []
        alpha_value = random.randint(50,100)
        alpha = Image.new("L", filter.size)
        for pixel in filter.getdata():
            alpha_data.append(alpha_value)
        alpha.putdata(alpha_data)
        filter.putalpha(alpha)
        
        img.paste(filter, (0,0), filter)
        
        return img
        
    
    def addHologram(self, img):
        hologram_idx = np.random.choice(len(self.hologram_list))
        hologram_path = self.hologram_list[hologram_idx]
        
        hologram = Image.open(hologram_path).resize((self.img_width, self.img_height)).convert("RGBA")
        
        img.paste(hologram, (0,0), hologram)
        
        return img
    
    def saveAnnotation(self, img_idx):
        annos = {"images": {"id": img_idx, "width": self.img_width, "height": self.img_height,
            "file_name": f'{img_idx}.jpg', "type": "id"
        }}
        
        annos["annotations"] = {}
        
        for idx, item in enumerate(self.bbox_annotation):
            anno_dict = {"id": idx+1, "image_id": img_idx}
            anno_dict.update(item)
            annos["annotations"][idx+1]=anno_dict
        
        anno_file_path = os.path.join(self.save_anno_dir, f"{img_idx}.json")
        
        if not os.path.exists(self.save_anno_dir):
            os.makedirs(self.save_anno_dir)
        
        with open(anno_file_path, 'w') as f:
            json.dump(annos, f)
        
        
    def multiline_textsize(self, draw, text, font):
        """ Compute the width and height of multiline text in pixels.
        """
        lines = text.split('\n')
        widths = [draw.textlength(line, font=font) for line in lines]
        return max(widths)

    def get_anno_info(self, draw, x, y, text, font):
        anno_info = []
        words = text.split()
        
        for word in words:
            word_bbox = draw.textbbox((x,y),word, font=font)
            # draw.rectangle(word_bbox, outline=(0,255,0))
            
            w = word_bbox[2] - word_bbox[0]
            
            x += w + font.getbbox(' ')[2]
            
            resize_bbox_left = word_bbox[0] - 3
            resize_bbox_top = word_bbox[1] - 3
            resize_bbox_right = word_bbox[2] + 3
            resize_bbox_bottom = word_bbox[3] + 3
            
            word_bbox_resize = (resize_bbox_left, resize_bbox_top, resize_bbox_right, resize_bbox_bottom)
            
            # draw.rectangle(word_bbox_resize, outline=(255,0,0))
            
            anno_info.append({"bbox": list(word_bbox_resize), "mask": self.get_mask_coord(word_bbox_resize), "text": word})
        
        return anno_info

    def get_mask_coord(self, bbox):
        x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3] #(left, top, right, bottom)
        return [x1,y1, x2,y1, x2,y2, x1,y2]