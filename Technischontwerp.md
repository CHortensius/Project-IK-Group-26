# Technisch Ontwerp

## Controllers

#### Welkompagina route (De eerste pagina van de website)
Dit zal de eerste route zijn naar onze website. De gebruiker krijgt hier een scherm te zien, waarop het doel van de website duidelijk wordt. Tevens komen hier 2 opties tevoorschijn: inloggen als bestaande gebruiker, en een account aanmaken als nieuwe gebruiker.  Dit zal een GET-request worden.

#### Inlogroute
De gebruiker krijgt hier de optie om in te loggen. Hij/zij zal een inlognaam en wachtwoord in moeten vullen, om hierna naar zijn of haar home page te worden gestuurd. Dit zal een POST-request worden.

#### Uitlogroute
Wanneer een gebruiker wilt uitloggen, kan hij/zij klikken op de button ‘uitloggen’. Hier komt geen scherm bij. De gebruiker wordt namelijk, na het succesvol uitloggen, teruggestuurd naar de welkompagina.

#### Aanmeldroute
Wanneer de gebruiker nieuw is bij de website zal hij/zij een account moeten aanmaken. Dit door een gebuikersnaam te verzinnen, en 2x een wachtwoord in te voeren. Hier hoort een apart scherm bij.

#### Uploadroute
Hier kan de gebruiker een foto bestand kiezen, en uploaden op de website. Ook hier hoort een scherm bij.

#### Verwijder route

De gebruiker kan via deze route een foto (die ze zelf hebben geplaatst) verwijderen. Hier komt geen apart scherm voor, alleen een flash bericht.

#### Like route
Via deze weg kunnen gebruikers foto’s liken. Hier hoort geen apart scherm bij.

#### Reageer route
Via deze weg kunnen gebruikers onder foto’s reacties achterlaten. Hier komt een apart scherm voor.

#### Volg route
De gebruiker kan via deze weg andere gebruikers gaan volgen, zodat zij de foto’s van die gebruikers op de startpagina te zien krijgen.

#### Startpagina route
Nadat een gebruiker heeft ingelogd komt hij/zij op de startpagina terecht. Hier krijgt de gebruiker in eerste instantie foto’s te zien van gebruikers die hij/zij volgt. Eventueel kan de gebruiker via de discover-route, andere foto’s van andere gebruikers zien. Dit zal geen apart scherm worden, alleen een ‘tab’ in het startpagina scherm

#### Eigen account route
Hier kan de gebruiker zijn of haar eigen account bekijken. Hier hoort een scherm bij

#### Iemand anders zijn account route
Hier kan de gebruiker een andermans account zien. Het enige verschil met het eigen account pagina, is dat hier geen foto’s verwijderd kunnen worden. Hier hoort een apart scherm bij.

## Views
![Schets 1](https://imgur.com/a/0pBzq.jpg"Schets")
## Frameworks
Flask Framework. Dit omdat wij hier al wegwijs door zijn geraakt tijdens Pset7: Finance

Bootstrap: https://getbootstrap.com
Dit moet ons gaan helpen met het design van de website. Hiermee kunnen wij gemakkelijker dingen aanpassen in de html/css codes.
