from authlib.jose import JsonWebToken

user = {'iss': 'https://accounts.google.com',
        'azp': '536726852610-o1nho8r232g3122f7ol71ih8krma78rv.apps.googleusercontent.com',
        'aud': '536726852610-o1nho8r232g3122f7ol71ih8krma78rv.apps.googleusercontent.com',
        'sub': '108134484603288420679', 'email': 'meatball0520@gmail.com', 'email_verified': True,
        'at_hash': 's3rURXt4ZFJlEpAMYQVM_w', 'nonce': '6F2NxoAV6POdSuZIFyyJ', 'name': '王博生',
        'picture': 'https://lh5.googleusercontent.com/-CTMrEGMR2rY/AAAAAAAAAAI/AAAAAAAAAAA/AMZuuclgEWSy1hVBPWiYZ_XbQR1QcC20xw/s96-c/photo.jpg',
        'given_name': '博生', 'family_name': '王', 'locale': 'zh-TW', 'iat': 1616686829, 'exp': 1616690429 }

jwt = JsonWebToken(['HS256'])
key = 'iamkey'
encode = jwt.encode(header={
    "alg": "HS256",
    "typ": "JWT"
}, payload=user, key=key)
claim = jwt.decode(encode, key=key)
claim.validate()
print()
