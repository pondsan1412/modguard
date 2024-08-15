from googletrans import Translator

trans = Translator()
translated = trans.translate(text='MEC',dest='en',src='fr')
print(translated.text)