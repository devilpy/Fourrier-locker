from Crypto.Hash import SHA256

def hash_me(text):
    b = str.encode(text)
    h = SHA256.new()
    h.update(b)
    shaEncryp = h.hexdigest()
    return shaEncryp

print(hash_me(str(9)))