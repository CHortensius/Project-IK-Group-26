from imgurpython import ImgurClient

client_id= '978480f212b2fba'
client_secret= 'f6816fc6b2874541f74c9a8ef8a94c556841d792'
refresh_token= '80ddfe566ccfc68403b632be352fa4c7bb53ad0e'
access_token= 'f8abdffaf2902a85d6ebb44af4f4d2c010d095bd'

client = ImgurClient(client_id, client_secret, access_token, refresh_token)
image = client.upload_from_path('photo1.png', anon=True)
print(image)



## Alex, dit bestand zorgt ervoor dat de, lokaal opgeslagen afbeeldingen, worden geupload naar de imgur website.
## Wanneer je deze code runt krijg je een dict eruit, waar verschillende keys staan. De laatste key is een url naar waar de foto staat. Als je deze in de database zet,
## kunnen wij m straks makkelijk laten zien op de website. Dan is het namelijk alleen de url aanroepen. Waar nu photo1.png staat, moet dan het pad naar waar de foto is opgeslagen.
## Verder zijn de andere bestanden in de ImgurApi map niet echt van toepassing, maar laat ik voor de zekerheid even staan. Hoop dat je dit verhaal begrijpt :)