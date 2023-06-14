import hmac
import hashlib

def verify_request(api_key, message, sha_request_header):
    signature = hmac.new(bytes(api_key , 'latin-1'), msg = bytes(message , 'latin-1'), digestmod = hashlib.sha256).hexdigest().upper()

    if signature == sha_request_header:
        return True

    return False
