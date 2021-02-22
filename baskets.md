# Feature: Hakukierros

## Hakukierroksen korit

## Yleiskatsaus:

## Ongelma:

Nykyään tiloja jaetaan prosessilla, jossa tilojen hakukriteerit eivät ole selkeästi etukäteen määritelty
ja päätöksentekoprosessi ei ole läpinäkyvä. Tämä voi johtaa siihen, että vuorojen jakoa 
ei koeta oikeudenmukaiseksi. 

## Tavoite:
* Läpinäkyvyyden lisääminen, oikeudenmukaisuuden kokemuksen lisääntyminen
* hakukriteerit ja kiintiöt ovat avoimesti tiedossa

## Personat:

Heikki on nuorison palvelukokonaisuuden työntekijä,
joka toimii tilavarauspalvelun pääkäyttäjänä.
Heikillä on laajat oikeudet syöttää järjestelmään tilojen tietoja,
muokata hakukierrosten arviointikriteerejä ym.

## Käyttökokemus:

* Olettaen että järjestelmästä järjestelmässä on nuorison hakukierros keväälle 2021,
jonka haettavien vuorojen aikaväli on 1.3.2021-1.5.2021 ja hakuaika päättyy 1.2.2021
    * Kun Heikki katsoo hakukierroksen tietoja
        * Hän näkee että hakukierroksella on "Muut hakemukset" kori, jonka ehtoja ei pystyy muuttamaan
    * Kun Heikki valitsee "Luo uusi kori"
    * Ja syöttää Korin nimeksi "Helsinkiläisten lasten ja nuorten seurat"
    * Ja valitsee asiakastyypiksi "Yhdistys tai seura"
    * Ja valitsee organisaation kotipaikkakunnaksi "Helsinki"
    * Ja valitsee ikäryhmäksi "5-10 vuotiaat" ja 11-15 vuotiaat
        * Hän näkee, hakemuskierroksella korin "Helsinkiläisten lasten ja nuorten seurat"
        * Ja näkee, että "Helsinkiläisten lasten ja nuorten seurat" kori on "Muut hakemukset" korin yläpuolella
    * Kun Heikki valitsee "Luo uusi kori"
    * Ja syöttää Korin nimeksi "Muut seurat"
    * Ja valitsee asiakastyypiksi "Yhdistys tai seura"
        * Hän näkee, hakemuskierroksella korit "Helsinkiläisten lasten ja nuorten seurat", "Muut seurat" 
        * Ja näkee, että "Muut hakemukset" kori on järjestyksessä viimeisenä

## Vaatimukset:

| Ominaisuus                      | Huomioita                                                                                        |
|---------------------------------|--------------------------------------------------------------------------------------------------|
| Nimi                            | Pakollinen                                                                                       |
| Järjestysnumero                 | Pakollinen, muodostuu korien järjestyksestä käyttöliittymällä                                    |
| Asiakastyyppi                   | Valinnainen, monivalinta. Vaihtoehdot asiakastyyppien arvoista                                   |
| Ikäryhmät                       | Valinnainen, monivalinta. Valitaan määritellyistä ikäryhmistä                                    |
| Kotipaikkakunta                 | Valinnainen. Vain yksi valinta, valitaan määritellyista paikkakunnista.                          |
| Toiminnan tyyppi                | Valinnainen. Valitaan toiminnan tyypeistä                                                        |
| Tavoiteprosentti * Ei pilotissa | Valinnainen. Monivalinta. Valitaan määritellyistä käyttäjäryhmistä.   esim. tasoryhmät           |
| Käyttäjäryhmä * Ei pilotissa    | Valinnainen. Hakukierroksen kaikkien korien tavoiteprosenttien summan tulee olla korkeintaan 100 |

## Avoimet kysymykset:
* Ei koske pilottia
    * Tarvitaanko erilliset käsitteet pririteettikoreille, jossa järjestysnumerolla on vaikutus siihen,
mihin koriin kuuluville hakemuksille jaetaan vuoroja ensimmäisenä. Näillä koreilla ei ole tavoiteprosenttia 
    * Ja allokointikoreille, joilla on tavoiteprosentti ja korien järjestyksellä ei ole väliä(?)
    * Näiden jakaminen vaatii hiukan erilaisen lähestymistavan algoritmissa, koska tavoiteprosentti saa ylittyä,
    joten sitä ei voi käsitellä maksimina, jollaisena sitä pitäisi käsitellä jos koreja käynnistetään yksi kerrallaan. 
    Tai ainakin se vaatisi sen, että prosenttia käsitellään maksimina silloin kuin käynnistetään kori tai koreja kerraallaan
    ja tavoitteena, joka voi ylittyä, silloin kuin käynnistetään koko hakukierroksen vuorojako.

# Feature: Vuorojakoehdotuksen muodostaminen

# Feature: Hakukierroksen korien allokointi

## Yleiskatsaus: 

## Ongelma:

Nykyään tiloja jaetaan prosessilla, jossa tilojen jakamisen prioriteettia hoidetaan manuaalisella paperiprosessilla.
Tämä voi johtaa siihen, että vuorojen jakoa ei koeta oikeudenmukaiseksi ja päätöksenteko ei ole läpinäkyvää.
Hakemuksia joudutaan vertailemaan ja etsimään niille sopivia aikoja manuaalisesti. 

## Tavoite:

* Hakemukset voidaan jakaa koneellisesti määriteltyjen korien vaatimusten ja tavoiteprosenttien mukaan. 
* Hakemukset jaetaan läpinäkyvästi hakukierroksen määriteltyjen prioriteettien mukaisesti. 

## Personat:

Pertti on nuorison vakiovuorohakemusten käsittelijä, jonka vastuulla on jakaa Kontulan nuorisotyöyksikön nuorisotilojen vakiovuorot.

## Käyttökokemus:

* Olettaen että järjestelmässä on nuorison hakukierros keväälle 2021, jonka haettavien vuorojen aikaväli on 1.3.2021-1.5.2021 ja hakuaika päättyy 1.2.2021
* Ja hakemus on esikäsitelty. 
    * Ja hakukierrokselle on määritelty kori nimeltään A
        * Jonka toiminnan luokka on nuorisotoiminta
        * Organisaation kotipaikka on Helsinki
        * Järjestysnumero on 1
    * Ja hakukierrokselle on määritelty kori nimeltään B
        * Jonka toiminnan luokka on nuorisotoiminta
        * Ja organisaation kotipaikkakuntaa ei ole määritelty
        * Järjestysnumero on 1
 * Ja hakukierrokselle kuuluu tilat
    * 1, 2, 3 tähän tiedot, aukioloajat
 * Ja hakukierrokselle on n hakemusta
    * tähän hakemusten tiedot
 
 * Kun Pertti avaa hakukierroksen tiedot
    * Hän näkee hakukierroksen korit A, B (ja muut hakemukset?)
    
 * Kun Pertti valitsee korin A
    * Hän näkee, että kyseiseen koriin poimitaan vuorotoiveet, joiden toiminnan luokka on nuorisotoiminta ja hakevan organisaation kotipaikka on Helsinki
 * Ja valitsee "Muodosta vuorojakoehdotus"
 * Hän näkee, että järjestelmä ehdottaa vuoroja hakemuksille, joiden toiminnan luokka on nuorisotoiminta ja organisaation kotipaikka on Helsinki    
 
## Vaatimukset:

### Priorisointikorien jakaminen
* Koreihin poimitaan hakemukset joiden
    * Ikäryhmä, käyttötarkoitus ja organisaation kotipaikka vastaa korille määriteltyjä ikäryhmiä, käyttötarkoituksia ja kotipaikkakuntaa
        * Jos korille ei ole määritelty jotain tai kaikkia näitä ominaisuuksia, saa vastaava avo hakemuksella olla tyhjä tai mikä tahansa arvo
        * Esim. jos korille ei ole määritelty käyttötarkoitusta, voi hakemuksella määritelty käyttötarkoitus olla mikä tahansa.
* Hakemus voi kuulua kriteereiden puolesta useampaan kuin yhteen koriin   
* Kun käynnistetään algoritmi koko hakukierrokselle
    * Ensimmäisenä jaetaan vuorot järjestysnumeroltaan ensimmäiselle korille
    * Sen jälkeen siitä alaspäin korien järjestysnumeroiden mukaan
    * Viimeisenä jaetaan vuoroja "Muut hakemukset" korille (catch all)
* Kun käynnistetään vuorojako yhdelle korille
    * Jaetaan vuoroja siihen kuuluville hakumuksille
* Jos hakemus sopii koreihin, joiden järjestysnumero on 1 ja 2 
    * Ja hakemus ei saa (kaikkia) haluamiaan vuoroja kun ajetaan korin 1 allokointi
        * Kun käynnistetään korin 2 allokointi, voi hakemus saada lisää vuoroja korin 2 jaossa 
* Jos hakemus sopii koreihin, joiden järjestysnumero on 1 ja 2 
    * Kun käynnistetään korin, jonka järjestysnumero on 2 allokointi ennen kuin korin 1 allokointi on ajettu
        * Lähtökohtaisesti korit pakotetaan ajamaan vähintään kerran osoitetussa järjestyksessä
            * Jos tästä halutaa poiketa ja/tai seuraavien vuorojakojen kohdalla
                * Jaetaan vuoroja valitun korin hakemuksille riippumatta sen järjestysnnumerosta. 
    
## Avoimet kysymykset:

