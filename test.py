from modules import function
translated = 'สวัสดีครับสวัสดีครับ @ModGuard  :pepostare: '
extracted, remaining = function.message.extract_message(message=translated)
extracted_emoji, remaining_emoji = function.message.extract_custom_emoji(message=remaining)
check_bool_remaining = function.convert_boolean(text=remaining)
check_bool_extracted = function.convert_boolean(text=extracted)

def check():
    if extracted_emoji == None and remaining_emoji == None:
        return
    if check_bool_extracted == None:
       print(extracted,remaining_emoji ,extracted_emoji)
   

check()