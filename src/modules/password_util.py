import bcrypt

def encrypt(password_str):
  bytes = password_str.encode('utf-8')
  salt = bcrypt.gensalt()
  hash = bcrypt.hashpw(bytes, salt)
  return hash

def check_password(password_str, hashed_password):
    # try:
    user_bytes = password_str.encode('utf-8')
    result = bcrypt.checkpw(user_bytes, hashed_password)
    return result
    # except Exception as e:
    #   print(f'ERROR: {e} Password Check could not be performed.')