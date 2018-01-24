from imgurpython import ImgurClient

client_id= '978480f212b2fba'
client_secret= 'f6816fc6b2874541f74c9a8ef8a94c556841d792'
refresh_token= '80ddfe566ccfc68403b632be352fa4c7bb53ad0e'
access_token= 'f8abdffaf2902a85d6ebb44af4f4d2c010d095bd'

client = ImgurClient(client_id, client_secret, access_token, refresh_token)
image = client.upload_from_path('photo1.png', anon=True)
print(image)