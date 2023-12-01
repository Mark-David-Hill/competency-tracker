import bcrypt
from modules.database_manager import get_user_with_specific_email

def encrypt_password(password_str):
  bytes = password_str.encode('utf-8')
  salt = bcrypt.gensalt()
  hash = bcrypt.hashpw(bytes, salt)
  return hash

def check_password(password_str, hashed_password):
    # try:
    hash = bytes(hashed_password, 'utf-8')
    user_bytes = password_str.encode('utf-8')
    result = bcrypt.checkpw(user_bytes, hash)
    return result
    # except Exception as e:
    #   print(f'ERROR: {e} Password Check could not be performed.')

class User:
   def __init__(self, user_data) -> None:
      id, first_name, last_name, phone, email, password_hash_str, is_active, date_created, hire_date, user_type = self.user_data
      full_name = first_name + ' ' + last_name

def attempt_login(cursor, user_name, password):
  try:
    user_data = get_user_with_specific_email(cursor, user_name)
    hash_str = user_data[5]
    is_valid_password = check_password(password, hash_str)
    if user_data[4] == user_name and is_valid_password:
      # current_user = User(user_data)
      # return current_user
      return True
    else:
      return False
  except:
    print(f'ERROR: Incorrect User Name. Login attempt failed.')