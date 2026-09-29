from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def get_hashpassword(password:str)->str:
    return password_hash.hash(password)

def verify_password(plain_pass:str,hash_pass:str)->bool:
    return password_hash.verify(plain_pass,hash_pass)