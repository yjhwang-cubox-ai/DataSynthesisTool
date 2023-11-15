from PIL import Image, ImageDraw, ImageFont

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
                 config["issue_date"],
                 config["issue_authority"]]
    
    for idx in range(len(texts)):
        fonts.append(ImageFont.truetype(font_path[idx], font_size[idx]))
    
    print(texts)