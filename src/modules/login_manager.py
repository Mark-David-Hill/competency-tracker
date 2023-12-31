import bcrypt
from modules.database_manager import get_user_with_specific_email

class Login_Manager:
  def __init__(self, connection):
    self.user_logged_in = False
    self.current_user = None
    self.is_manager = False
    self.connection = connection
    self.cursor = connection.cursor()
    self.user = None
  
  class User:
   def __init__(self, id, first_name, last_name, phone, email, password_hash_str, is_active, date_created, hire_date, user_type) -> None:
    self.id = id
    self.first_name = first_name
    self.last_name = last_name
    self.phone = phone
    self.email = email
    self.password_hash_str = password_hash_str
    self.is_active = is_active
    self.date_created = date_created
    self.hire_date = hire_date
    self.user_type = user_type
    self.full_name = self.first_name + ' ' + self.last_name

  def encrypt_password(self, password_str):
    bytes = password_str.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    hash_str = hash.decode('utf-8')
    return hash_str

  def check_password(self, password_str, hashed_password):
      try:
        hash = bytes(hashed_password, 'utf-8')
        user_bytes = password_str.encode('utf-8')
        result = bcrypt.checkpw(user_bytes, hash)
        return result
      except Exception as e:
        print(f'ERROR: {e} Password Check could not be performed.')

  def attempt_login(self, cursor, user_name, password):
    try:
      user_data = get_user_with_specific_email(cursor, user_name)
      is_active = user_data[6]
      hash_str = user_data[5]
      is_valid_password = self.check_password(password, hash_str)
      if user_data[4] == user_name and is_valid_password:
        if is_active:
          id, first_name, last_name, phone, email, password_hash_str, is_active, date_created, hire_date, user_type = user_data
          self.current_user = self.User(id, first_name, last_name, phone, email, password_hash_str, is_active, date_created, hire_date, user_type)
          self.user_logged_in = True
          self.user = self.User(id, first_name, last_name, phone, email, password_hash_str, is_active, date_created, hire_date, user_type)
          if user_data[9]:
            self.is_manager = True
          return True
        else:
          print('\n- Sorry, Inactive Users cannot Login. -')
          return False
      else:
        print('\n- Incorrect User Name or Password. Login attempt failed.')
        return False
    except:
      print(f'\nERROR: Incorrect User Name or Password. Login attempt failed.')

  def logout_user(self):
    self.current_user = None
    self.user_logged_in = False
    self.is_manager = False
    
  def logout_user_prompt(self):
    should_logout = input('Are you sure you want to Logout? (Y/N)')
    if should_logout.lower() == 'y':
      self.logout_user()
      return True
    else:
      return False

  def clear(self):
    self.user_logged_in = False
    self.current_user = None
    self.is_manager = False
    self.user = None