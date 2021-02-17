#Feature: Hakukierroksen korien allokointi

##Yleiskatsaus:

##Ongelma:

##Tavoite:

##Personat:

Pertti on nuorison vakiovuorohakemusten käsittelijä, jonka vastuulla on jakaa Kontulan nuorisotyöyksikön nuorisotilojen vakiovuorot.

##Käyttökokemus:
* Hakemukset on esikäsitelty, eli on varmistettu, että ne ovat sisällöllisesti järkeviä ja niiden pisteytettävät tekstivastaukset on pisteytetty.

* Olettaen että järjestelmässä on nuorison hakukierros keväälle 2021, jonka haettavien vuorojen aikaväli on 1.3.2021-1.5.2021 ja hakuaika päättyy 1.2.2021
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
 
##Vaatimukset:
 * katso hakukierroksen valmistelu. 
 
 * Koreihin poimitaan hakemukset joiden
    * Ikäryhmä, käyttötarkoitus ja organisaation kotipaikka vastaa korille määriteltyjä ikäryhmiä, käyttötarkoituksia ja kotipaikkakuntaa
        * Jos korille ei ole määritelty jotain tai kaikkia näitä ominaisuuksia, saa vastaava avo hakemuksella olla tyhjä tai mikä tahansa arvo
        * Esim. jos korille ei ole määritelty käyttötarkoitusta, voi hakemuksella määritelty käyttötarkoitus olla mikä tahansa.
   
 * Jos hakemus sopii korin määritysten puolesta useampaan kuin yhteen koriin, poimitaan se koriin??
    * Kun käynnistetään algoritmi koko hakukierrokselle???
    * Kun käynnistetään algoritmi yhdelle korille???
    * Kun käynnistetään algoritmi useammalle korille???
 * Jos hakemus sopii koreihin, joiden järjestysnumero on 1 ja 2 
    * Ja hakemus ei saa haluamiaan vuoroja kun ajetaan korin 1 allokointi
        * Kun käynnistetään korin 2 allokointi hakemukselle tapahtuu jotain???
 * Jos hakemus sopii koreihin, joiden järjestysnumero on 1 ja 2 
    * Kun käynnistetään korin, jonka järjestysnumero on 2 allokointi ennen kuin korin 1 allokointi on ajettu
        * haku
    
##Avoimet kysymykset:

* Jos/kun määritellyt korit eivät poimi kaikkia mahdollisia hakemuksia, miten tämä tulisi hoitaa. Tehdäänkö automaattisesti tai pakotetaan käyttäjä tekemään “catch all“ kori, johon poimitaan kaikki mitkä ei sovi muihin koreihin. Jos allokointia käynnistetään kori kerrallaan, niin voisi olla selkeä käyttäjälle. Vai tehdäänkö niin, että kaikki mitkä ei osu koreihin, jaetaan silloin kun käynnistetäään kaikkien hakemusten jako (ei kori kerrallaan).
* Koreja on mahdollista tehdä niin, että hakemus saattaa osua useampaan koriin. Jos hakemus kriteereiden puitteissa osuisi koriin 1 ja koriin 2, ja käynnistetään kori 2 ensimmäisenä. Otetaanko tämä hakemus mukaan koriin 2 vai jääkö se odottamaan korin 1 käynnistämistä.
* Ajaako korien järjestysnumero käynnistysjärjestyksen ohi vai ajaako käynnistysjärjestys korien järjestyksen ohi. 
* Hakemus kriteerien puolesta osuu koreihin 1 ja 2. Käynnistetään kori 1, hakemus ei saa aikaa syystä x. Pitäisikö se silloin ottaa mukaan koriin 2. Ehkä hieman marginaalitapaus, mutta mahdollista erityisesti siinä vaiheessa kun koreille tulee ne tavoiteprosentit
 *Mitä hakemuksen hylkääminen tekee, hylkääkö ehdotetut vuorot tiettyyn tilaan, pitääkö estää jakaminen uudestaan samaan tilaan, liittykö tämä mitenkään koreihin?

