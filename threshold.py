from googletrans import Translator
trans = Translator()
translated  = trans.detect(text='สวัสดีครับ')
print(translated.lang)