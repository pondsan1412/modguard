from modules import function

def check():
    if not function.switch_button.check_switch():
        print('code not pass')
        return
    
check()