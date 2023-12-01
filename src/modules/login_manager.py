import bcrypt

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

def attempt_login(cursor, user_name, password):
  #  Get user with exact user_name as the email address
   pass

class User:
   def __init__(self) -> None:
      pass