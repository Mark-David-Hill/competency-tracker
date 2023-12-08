class Options:
  def __init__(self):
    pass

class Menu_Manager:
  def __init__(self, header, options, is_root_menu):
    self.header = header
    self.options = options
    self.is_root_menu = is_root_menu

def display_menu(menu):
  for key, value in menu.items():
    print(key)
  
def run_menu(menu, login_manager):
  quit_pending = False
  while True:
    is_main_menu = False
    menu_options = list(menu.keys())
    if menu_options[0][2] == '*' or menu_options[0][2] == '-':
      is_main_menu = True
    choices = []
    for i in range(len(menu_options)):
      choices.append(str(i + 1))
    actions = list(menu.values())
    display_menu(menu)
    if is_main_menu:
      choice = input("\nPlease choose an option from the menu above: ")
    else:
      choice = input("\nPlease choose an option from the menu above, or press 'Enter' to return to the previous menu: ")
    if choice == '' and not is_main_menu:
      return False
    elif choice == '' and is_main_menu:
      pass
    if choice in choices:
      for i in range(len(choices)):
        if choices[i] == choice:
          if callable(actions[i]):
            actions[i]()
          elif actions[i] == 'logout':
            logged_out = login_manager.logout_user_prompt()
            if logged_out is True:
              quit_pending = True
          elif actions[i] == 'quit':
            print('\n - Goodbye! -')
            quit_pending = True
          else:
            quit_pending = run_menu(actions[i])
    else:
      print("\nSorry, I didn't understand your selection. Please enter a valid option.")
    if quit_pending == True:
      break