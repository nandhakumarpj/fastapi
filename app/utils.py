from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.
    
    Args:
        password (str): The password to hash.
        
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)