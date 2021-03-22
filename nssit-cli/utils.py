




def check_encryption_key(key):
    l = len(key)
    if l == 16 or l == 24 or l == 32:
        return True
    return False