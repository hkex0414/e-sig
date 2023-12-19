from PIL import Image, ImageDraw, ImageFont
import os
import time
import io
import win32clipboard
import configparser
import sys

def main():
    base_w, base_h = (320, 320)
    config = configparser.ConfigParser()
    print(os.path.dirname(os.path.abspath(sys.argv[0])))
    config.read(os.path.dirname(os.path.abspath(sys.argv[0])) + '\config.ini', encoding='utf-8')
    moji_upper = config.get('Settings', 'moji_upper')
    moji_lower = config.get('Settings', 'moji_lower')
    fontpath = config.get('Settings', 'font_path')
    yohaku = 10
    
    image = Image.new('RGBA', (base_w, base_h), (0, 0, 0, 0))  # 背景色を透明に設定
    image.putalpha(0)
    d = ImageDraw.Draw(image)
    
    d.ellipse([(yohaku, yohaku), (base_w - yohaku, base_h - yohaku)], outline='red', width=6)  # 円を描画
    
    # はんこ上部の文字を入れる
    adjust = 9
    hight = (( (base_h-yohaku*2) / 3 ) * 1) + yohaku
    d.line([(0+yohaku+adjust,hight),(base_w-yohaku-adjust,hight)],fill='red',width=6) # よこ線を入れる
    
    font = ImageFont.truetype(fontpath, 60)
    moji_w = d.textlength(moji_upper, font=font)
    moji_h  = 60
    moji_w = (base_w/2) - (moji_w/2)
    moji_h = hight - moji_h - yohaku
    d.text(( moji_w,moji_h), moji_upper, font=font, fill='red')
        
    hight = (( (base_h-yohaku*2) / 3 ) * 2) + yohaku
    d.line([(0+yohaku+adjust,hight),(base_w-yohaku-adjust,hight)],fill='red',width=6) # よこ線を入れる
    
    # 日付を入れる
    now = time.localtime()
    date = time.strftime('%Y.%m.%d', now) 
    
    font = ImageFont.truetype(fontpath, 55)
    moji_w = d.textlength(date, font=font)
    moji_h  = 55
    moji_w = (base_w/2) - (moji_w/2)
    moji_h = (base_h/2) - (moji_h/2)
    d.text(( moji_w,moji_h), date, font=font, fill='red')
    
    
    # はんこ下部の文字を入れる
    font = ImageFont.truetype(fontpath, 60)
    moji_w = d.textlength(moji_lower, font=font)
    moji_h  = 60
    moji_w = (base_w/2) - (moji_w/2)
    moji_h = hight + yohaku
    d.text(( moji_w,moji_h), moji_lower, font=font, fill='red')
    
    # 画像をファイルに保存
    image.save(os.path.dirname(os.path.abspath(sys.argv[0])) + '\{}.png'.format(time.strftime('%Y_%m_%d', now) ))
    
    # 画像をクリップボードに登録
    image_clipboard = Image.open(os.path.dirname(os.path.abspath(sys.argv[0])) + '\{}.png'.format(time.strftime('%Y_%m_%d', now)))
    output = io.BytesIO()
    image_clipboard.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


if __name__ == '__main__':
    main()