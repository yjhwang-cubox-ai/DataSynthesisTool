from PIL import Image, ImageDraw, ImageFont
import os
import glob
import numpy as np
import textwrap

def set_Text_Font(texts, config):
    texts = [texts[v][0] for v in texts.keys()]
    fonts = []
    
    if len(texts[1]) <= 3:
        font_size = [56, 45, 45, 33, 33, 33, 42]
    elif len(texts[1]) == 4:
        font_size = [56, 40, 40, 33, 33, 33, 42]
    elif len(texts[1]) > 4:
        font_size = [56, 32, 32, 33, 33, 33, 42]
        
    font_path = [config["type_font"],
                 config["kor_name_font"],
                 config["ch_name_font"],
                 config["regi_number_font"],
                 config["address_font"],
                 config["issue_date_font"],
                 config["issue_authority_font"]]
    
    for idx in range(len(texts)):
        fonts.append(ImageFont.truetype(font_path[idx], font_size[idx]))
        
    return texts, fonts

def DrawTextOnTemplate(texts, font, config, fname):
    # template 선택
    template_dir = config["template_directory"]
    template_list = [file for file in glob.glob(template_dir + '/*')]
    
    template_idx = np.random.choice(len(template_list))
    template = template_list[template_idx]
    
    img = Image.open(template).resize((960,600))
    draw = ImageDraw.Draw(img)
    
    # text
    if len(texts[1]) <= 3:
        positions = [(304, 84), (200, 179), (350, 181), (300, 252), (327, 370), (524, 472), (510, 517)]
    elif len(texts[1]) == 4:
        positions = [(304, 84), (200, 179), (370, 181), (300, 252), (327, 370), (524, 472), (510, 517)]
    elif len(texts[1]) >= 5:
        positions = [(304, 84), (180, 179), (400, 181), (300, 252), (327, 370), (524, 472), (510, 517)]
    get_anno_info = []
    
    # texts = ['부산광역시 부산진구 천자로 386, 1423동 5815호, (가야제1동, 창원 마린, 푸르지오 1단지)']
    # texts = ['전라북도 임실군 관촌면 방수리 222, 020동 3507호']
   
    for idx, text in enumerate(texts):        
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
            textlength = multiline_textsize(draw, text, font=font[idx])
        else:
            num_txts = 1
            textlength = draw.textlength(text, font=font[idx])
        
        x = positions[idx][0] - textlength // 2
        y = positions[idx][1] - font[idx].getbbox(text)[-1]*num_txts // 2
        
        text_bbox = draw.textbbox((x, y), text, font=font[idx])
        draw.rectangle(text_bbox, outline=(0,255,0))
        
        if '\n' in text:
            splited_text = text.split('\n')
            for splt in splited_text:
                draw.multiline_text((x,y), splt, fill="black", font=font[idx])
                splt_bbox = draw.textbbox((x,y), splt, font=font[idx])
                draw.rectangle(splt_bbox, outline=(0,0,0))
                y += font[idx].getbbox(splt)[-1]
        else:
            draw.multiline_text((x, y), text, fill="black", font=font[idx])
        
    # img.show()
    img.save(fname)
    print(f"{fname} is saved!")

def multiline_textsize(draw, text, font):
    """ Compute the width and height of multiline text in pixels.
    """
    lines = text.split('\n')
    widths = [draw.textlength(line, font=font) for line in lines]
    return max(widths)