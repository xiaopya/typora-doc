from reportlab.pdfgen import canvas  # pip install reportlab==3.6.8
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.lib.utils import ImageReader
import json
import os
from PIL import Image
from imp import reload

def save_pdf(tempdir, pagenum):

    with open(os.path.join(tempdir, str(pagenum) + ".json")) as f:
        data = json.load(f)
    c = canvas.Canvas(
        os.path.join(tempdir, str(pagenum) + ".pdf"),
        pagesize=(data['page']['pw'], data['page']['ph']),
    )

    styles = dict()
    for style in data['style']:
        for style_c in style['c']:
            if not styles.get(style_c):
                styles[style_c] = dict()
            for each in style['s']:
                styles[style_c][each] = style['s'][each]

    ttfs = [x for x in os.listdir(tempdir) if x[-4:] == '.ttf' and int(x[-8: -4], 16) == pagenum]
    ttf2font = data['font']
    reload(pdfmetrics)  # TODO: a issue here, if no reload(), font only work in page 1.
    #for ttf in ttfs:
        #pdfmetrics.registerFont(TTFont(ttf2font.get(ttf[:-4]), os.path.join(tempdir, ttf)))
        #pdfmetrics.registerFont(TTFont(ttf2font[ttf[:-4]], os.path.join(tempdir, ttf)))
    pdfmetrics.registerFont(TTFont('simsun', os.path.join('test', 'simsun.ttf')))
    try:
        img = Image.open(os.path.join(tempdir, str(pagenum) +  '.png'))
    except:
        pass

    try:
        os.mkdir(os.path.join(tempdir, str(pagenum)))
    except:
        pass

    data_body = data['body']
    data_body = sorted(data_body, key=lambda each: each['p']['z'])
    for item in data_body:
        if item['t'] == 'word':
            style = dict()
            if item.get('r'):
                for item_r in item['r']:
                    style.update(styles[item_r])
            if item.get('s'):
                style.update(item['s'])
            text = item['c']
            # TODO: bold do not work
            '''
            if style.get('bold'):
                text = '<b>' + text + '</b>'
            '''
            textobject = c.beginText()
            textobject.setTextOrigin(
                item['p']['x'],
                data['page']['ph'] - item['p']['y'] -14
            )
            if style.get('font-family'):
                textobject.setFont(
                    'simsun',
                    float(style['font-size']) if style.get('font-size') else 16)
                # textobject.setFont("d852b2711eb91a37f1115c280010001",float(style['font-size']) if style.get('font-size') else 16)
            if style.get('letter-spacing'):
                textobject.setCharSpace(float(style['letter-spacing']))

            if style.get('color'):
                textobject.setFillColorRGB(
                    int(style['color'][1: 3], 16) / 255,
                    int(style['color'][3: 5], 16) / 255,
                    int(style['color'][5: 7], 16) / 255
                )
            textobject.setFillColorRGB(0,0,0)
            textobject.textLine(text)
            c.drawText(textobject)
        elif item['t'] == 'pic':
            # TODO: is that work?
            if item['ps'] is not None and item['ps'] and item['ps'].get('_drop') and item['ps'].get('_drop') == 1:
                continue
            # follow code do not work.
            # https://groups.google.com/g/reportlab-users/c/SmIzKYdCodo
            # new_image = Image.new('RGBA', (int(item['c']['iw']), int(item['c']['ih'])))
            # new_image.paste(img, (int(item['c']['ix']), int(item['c']['iy'])))
            new_image = img.crop((
                int(item['c']['ix']), 
                int(item['c']['iy']),
                int(item['c']['iw'] + item['c']['ix']), 
                int(item['c']['ih'] + item['c']['iy'])
            ))
            img_width = None
            img_height = None
            if int(item['c']['iw']) != int(item['p']['w']) or int(item['c']['ih']) != int(item['p']['h']):
                img_width = item['p']['w']
                img_height = item['c']['ih'] / item['c']['iw'] * item['p']['w']
            new_image.save(os.path.join(tempdir, str(pagenum), '{}-{}.png'.format(item['p']['x'], item['p']['y'])))

            c.drawImage(
                os.path.join(tempdir, str(pagenum),
                             '{}-{}.png'.format(item['p']['x'], item['p']['y'])),
                float(item['p']['x']),
                float(data['page']['ph']) - int(item['c']['ih']+float(item['p']['y'])),
                width=img_width,
                height=img_height,
                mask='auto'
            )

    c.showPage()
    c.save()
