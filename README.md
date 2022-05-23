## 1. Projekt navn
Automatiseret sekretær.

## 2. Beskrivelse
Vi har lavet et script og deployet på en ubunto server. Gennem Google cloud platforms, publicher/subscriber service vil der bliver sendt et HTTPS request, når en email modtages på en given mail konto.  Mailens indhold kørers igennem et neural netværk, og forsøger at vurdere hvilken kategori invitationen hører til (Business, entertainment).
Derefter analyseres teksten efter start og slut tidspunkt, og tjekker op i ens google kalender om man allerede er booket på det tidspunkt, og hvis ikke opretter et nyt event med tilsvarende dato og tid.

Invitationer modtaget direkte i google kalender håndteres også.

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
fx : "Here at Financial Holdings, we value integrity, robustness, reliability,
and other such vague corporate buzzwords. We want you to come in for a
scheduled meeting the 27/05 at 12:00 and you're not leaving until 27/05
14:00. I trust we can come to a satisfactory conclusion, at least for us as
it might end in your termination.

We'll be seeing you. Always.

Beatrice Meagan, Financial Holdings HR Department
"

Tjek dit response på link: https://elcaptaino.duckdns.org/.

## 6. Status
Programet er opdelt 2. Emails invitationer & Calender invitationer
Emails invitationer er færdig bygget, men med begrændsninger for formuleringen af emailen.
 - En email kan modtages, håndteres og derefter lægges i kalenderen. 
Vi har lidt udfordringer med forskellige tidspunkt formuleringer.

Da vi selv har måtte lave trænings data, og derfor har et ret smalt datasæt. så for at vores neural netværk skal virke optimalt skal man bruge nogle buzzwords, i den given kategori.

Calender invitationer: 
Logik og google api er færdigbygget. Desværre har vi haft udfordringer med at håndtere et sync update fra google, når en ændring bliver lavet på et specifikt event. Denne del er derfor deactiveret.

## 7. Hvad vi vil highlighte
Neural Netværk klassen.
End to End
Google Pub/Sub service

