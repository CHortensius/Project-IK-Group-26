## Photosharing voor Fotografen: Sophie, Alex en Cas 

### Samenvatting
Welkom bij onze webapp "Naam website"! Een website waar je aan fotografie-skills kunt werken of andere fotografen kunt voorzien van de beste tips & tricks voor het maken van het perfecte shot. "Naam website" is handig voor iedereen die zich bezig houdt met fotografie: als hobby dan wel als professie. Door je foto hier te posten kunnen anderen je nog meer leren zodat je binnen no time het perfecte shot kunt schieten. Bovendien is het een platform waar je je creativiteit kan delen met liefhebbers. Het is een nieuw, origineel platform die aansluit bij de grote passie van fotografieliefhebbers wereldwijd. 

### Minimum viable product 
- Gebruikers moeten een account kunnen maken
- Gebruikers moeten foto’s kunnen uploaden
- Gebruikers moeten op foto’s kunnen reageren 
- Gebruikers moeten andere gebruikers kunnen volgen
- Gebruikers moeten een pagina met foto’s van gebruikers die ze volgen hebben (FRIENDS)
- Gebruikers moeten een pagina met foto’s van willekeurige gebruikers hebben (DISCOVERY)
- Gebruikers moeten foto’s van andere gebruikers kunnen liken

### Externe Componenten
- Bootstrap: Gebruiken we voor een CSS opmaak van onze website
- Imgur API: Om de foto's die worden geupload op te slaan en de URL te kunnen opslaan in de database
- MyPHPAdmin: Database voor het opslaan van gebruikers en foto's 
- Flask: Python framework voor het bouwen van een website

### Concurrende bestaande websites
- Instagram: instagram is bedoeld voor elk soort foto's. Onze website zal zich echt gaan richten op professionele fotografie, en is gericht op feedback in plaats van connecten met vrienden. 
- Tumblr: Hier geldt eigenlijk hetzelfde als voor instagram: het is niet expliciet voor professionele fotografie.
- Pinterest: Hier plaatst men foto's voor zichzelf, in de vorm van een pin-board, niet in de hoop op reacties/tips.
- Steam: Op steam kunnen reacties geliked en disliked worden. Dit gaan wij meenemen om hierdoor de fotografen te motiveren om betere foto's te maken. Echter richt "Naam website" zich vooral op positieve feedback: het platform is niet bedoeld om andere gebruikers 'af te kraken' zoals bij Steam wel gebeurd.

### Opzet van de website
##### WELKOMPAGINA:
De pagina waar je op komt wanneer je de website opent. Hier vindt je een uitleg over de website en een optie om je aan te melden of in te loggen. 
##### REGISTER:
Hier kan je een account aanmaken (POST). Dit wordt opgeslagen in een database en zo onthouden. 
##### LOGIN:
Hier kan je inloggen als je accountnaam en wachtwoord al bestaat. Ook d.m.v. POST
##### DISCOVERYPAGINA: 
Dit is de pagina waar je komt als je bent ingelogd of aangemeld. Hier vindt je d.m.v. GET: 
- Een link naar je profielpagina
- Een optie om de foto's die je ziet op de Discover pagina te filteren. Keuze tussen: Discover (Alle foto's die zijn geupload op chronologische volgorde) en Friends (Alle foto's die de gebruikers die jij volgt op chronologische volgorde)
- Een optie om uit te loggen, waarna je terugkeert naar de Welkompagina. 
##### PROFIELPAGINA:
Via de Discoverypagina kan je naar je eigen profielpagina. Hier vindt je:
- Foto's die jij hebt geupload
- Een optie om een foto te uploaden en hier een comment bij te schrijven
- Een knopje met 'Friends', waar je kan zien wie jij allemaal volgt en wie jou volgt
- Een optie om uit te loggen, waarna je terugkeert naar de Welkompagina.
##### ACCOUNTPAGINA:
Via 'Friends' kan je naar een accountpagina van een andere gebruiker. Hier vindt je foto's van deze gebruiker. 
#### UITLOGGEN:
Vanaf elke pagina vindt je rechtsboven de mogelijkheid om uit te loggen. Dan return je naar de welkompagina. 

### Updates in de loop van het project
##### MANIER VAN SCROLLEN
We hebben ervoor gekozen om de foto’s zo groot mogelijk weer te geven zodat de hoogwaardige kwaliteit van de foto’s het beste tot z’n recht komt.  Je ziet dus één grote foto en wanneer je naar beneden scrollt zie je de volgende. Dit scrollen gaat door tot de laatste foto (je hoeft dus niet op ‘volgende’ of ‘vorige’ te drukken)
##### ACCOUNTGEGEVENS
 We vragen de gebruikers om een gebruikersnaam, een wachtwoord en een bevestiging van het wachtwoord.  
##### COMMENTEN
 Een comment achterlaten bij een foto gaat als volgt: Je krijgt een optie om een comment te schrijven. Hieronder zie je een +: naast het + je kun je alle dingen aan de foto die je goed vindt beschrijven. Het zelfde geldt voor het - teken die onder het + teken staat. Als je geen pluspunten of juist geen minpunten hebt, laat je het leeg.
##### LIKEN
Liken a.h.v. JavaScript zodat de pagina niet bij elke like gerefreshed moet worden. 


 
