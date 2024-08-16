import secret_stuff
import deepl
api_ = deepl.Translator(auth_key=secret_stuff.api_keys)
lang_detected = api_.translate_text(context='I')
print(lang_detected.detected_source_lang)