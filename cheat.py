email_auth = 0
token_auth = 1

def check_creditials(method, input1, input2):
    if method == email_auth:
        return email_validate_login(input1, input2)
    elif method == token_auth:
        return token_validate_login(input1)

def email_validate_login(email, password):
    return True
def token_validate_login(token):
    return False
