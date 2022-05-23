## 1. Projekt navn
Automatiseret sekretær.

## 2. Beskrivelse
Vi har lavet et script og deployet på en Ubuntu server. Gennem Google Cloud platforms, publisher/subscriber service vil der bliver sendt et HTTPS request, når en email modtages på en given mail konto.  Mailens indhold køres igennem et neural netværk, og forsøger at vurdere hvilken kategori invitationen hører til (Business, Entertainment).
Derefter analyseres teksten efter start- og slut-tidspunkt, og tjekker ens google kalender om man allerede er booket på det tidspunkt. Hvis ikke man er, opretter den et nyt event med tilsvarende dato og tid.

Invitationer modtaget direkte i Google kalender håndteres også.

## 3. teknologier
* nltk 
* sklearn
* pickle4
* Google cloud platform
* Ubuntu
* Tmux
* Nginx og certbot


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
Send en mail med invitation på engelsk til: pythondiller@gmail.com.

fx :

>"Here at Financial Holdings, we value integrity, robustness, reliability,
and other such vague corporate buzzwords. We want you to come in for a
scheduled meeting the 27/05 at 12:00 and you're not leaving until 27/05
14:00. I trust we can come to a satisfactory conclusion, at least for us as
it might end in your termination.
>
>We'll be seeing you. Always.
>
>Beatrice Meagan, Financial Holdings HR Department"

Tjek dit response på link: https://elcaptaino.duckdns.org/.

## 6. Status
Programmet er opdelt i 2. Email invitationer & Calendar invitationer.
Email invitationer er færdigbygget, men med begrænsninger for formuleringen af emailen.
 - En email kan modtages, håndteres og derefter lægges i kalenderen.
Vi har lidt udfordringer med forskellige tidspunktformuleringer.

Da vi selv har måtte lave træningsdata og derfor har et ret smalt datasæt, så for at vores neural netværk skal virke optimalt, skal man bruge nogle buzzwords i den givne kategori.

Calendar invitationer: 
Logik og Google API er færdigbygget. Desværre har vi haft udfordringer med at håndtere et sync update fra Google, når en ændring bliver lavet på et specifikt event. Denne del er derfor deaktiveret.

## 7. Hvad vi vil highlighte
Neural Netværk klassen.

