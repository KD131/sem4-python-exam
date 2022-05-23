## 1. Projekt navn
Automatiseret sekretær.

## 2. Beskrivelse
Vi har lavet et script og lagt det op på en server, der lytter til, om en google mail kommer ind på en given mail konto. Hvis der gør det kører den mailen igennem et neural netværk, den ser om hvilken kategori den hører til (Business, entertainment) og så ser om der et given dato og tidspunkt, tjekker op i ens google kalender om man allerede er booket på det tidspunkt, ellers opretter den et nyt event tilsvarende dato og tid. 


## 3. teknologier
* nltk 
* sklearn
* pickle4
* Google cloud platform
* Ubuntu
* Nginx og certbot
* duckdns


## 4. Installation
```
pip install nltk 
nltk.download('stopwords') 
pip install sklearn 
pip install pickle4 
pip install MultinomialNB
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install google-auth
pip install parsedatetime
```
*I nogle tilfælde kan man have brug for at installere MultinomialNB*

*google-auth er måske inkluderet i en af de andre libraries*

## 5. Bruger guide
Åben det her link https://elcaptaino.duckdns.org/.

Send en mail til den her mail på engelsk: pythondiller@gmail.com. 

Tjek dit response.

## 6. Status
Vi har fået hul igennem hele vejen. Så at når man sender en mail får man et response tilbage, og den laver et nyt event hvis der ikke allerede ligger et event i forvejen. Vi har valgt at lave det hele som et proof of concept, da der ikke ligger et dataset med business eller entertainment mails, så for at vores neural netværk skal virke optimalt skal man lave nogle rimelig buzz word mails, i den given kategori.

## 7. Hvad vi vil highlighte
Neural Netværk klassen.

