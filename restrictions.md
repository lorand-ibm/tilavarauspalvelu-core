# Taustaa

Tietyillä tiloilla voi olla viikkokohtainen maksimituntimäärä,
jonka ne voivat olla käytössä
(esim. nurmikentillä kulumisen vuoksi täytyy asettaa esim.max.20 tuntia viikossa -rajoite). 

Tiettyjä toiminnan tyyppejä ei voida sijoittaa peräkkäisille vuoroille,
jolloin toiminnan tyypeille täytyy pystyä luomaan päivä- tai kellonaikakohtaiset merkinnät
(esim.salibandya ja futsalia ei voi sijoittaa peräkkäisille vuoroille, koska laidat täytyy purkaa)
– todennäköisempää v1:ssä. 

(TAI luokkien välille voisi teoriassa tehdä säännön,
jonka mukaan kone jättää väliin halutun aikavälin,
mutta tämä on huomattavasti aikaavievempää määrittää,
eikä palvele muita liitoksia, kuten tilojen lohkomista ja sen vaatimuksia,
joten näkisin että menemme ykkösvaihtoehdolla?).

Tietyt tilat voivat olla jaettavissa päivä- tai kellonaikakohtaisesti lohkoiksi, ja lohkojen määrä voi vaihdella. 

Kuhunkin lohkoon pitää pystyä kohdistamaan tietty toiminnan tyyppi
ja siitä muodostuu oma varattavissa oleva varausyksikkönsä.

Huom. lohkoilla on myös rajoitteita, kuten 

a) Tietyt lajit eivät sovellu harrastettavaksi vierekkäin;
mutta tämän ei teoriassa pitäisi olla ongelma (=kohdevastaavan kanssa määritettävä sääntö).

b) Pesäpallossa turvallisuussyistä asiakas on pakotettu ottamaan myös viereinen kenttäpuolisko
tai lohko (=jälleen sääntö).

Lohkoja voivat olla esim. kentän jakaminen kahdeksi kenttäpuoliskoksi.

Lohkoja voivat myös olla esim. kenttäpuoliskon jakaminen edelleen
kahtia tai useampaan osaan (esim.sulkapallokentät),
jolloin sama tila voi käytännössä toimia monen toimintatyypin käytössä. 

Lohkojen määrä ei saa ideaalisti vaikuttaa vääristäen hinnoitteluun (oma keskustelunsa).

henkilön samanaikaisten varausten määrä (esim. max 10 varausta toimipisteessä tai max 10 varausta samantyyppisissä tiloissa)

miten esimerkiksi rajataan “max 10 varausta äänitysstudioihin”, jos äänitystudio ei ole oma tilatyyppinsä?

tehdään äänitysstudioista oma kokoelma?

käytetään avainsanaa “äänitysstudio”

jatkossa myös esim. tenniskenttien hoitajille ylläpito-oikeudet vain tenniskenttiin

samanlainen tarve: kokoelma vai avainsana, jos tilatyyppi tai käyttötarkoitus ei toimi? 

Ei kannata käyttää avainsanoja tähän, koska hankala kommunikoida ylläpitäjille,
arvaamattomia sivuvaikutuksia, avainsanojen suuri määrä jne.

käyttötarkoituksen hierarkkinen rakenne voisi toimia, esim. käyttötarkoitusella liikunta alaterminä voisi olla “Tenniskentät” ja käyttötarkoituksella musiikki voisi olla alaluokka “Äänitysstudio”

mahdollisia ongelmia siinä, että käyttötarkoitukset osin päällekkäisiä ja varausyksiköllä voi olla useita käyttötarkoituksia

käyttötarkoitus

nuorisotilat vain nuorison käyttöön, liikuntatilat liikuntakäyttöön, SoTe-tilat vain SoTe-järjestöille

jos varausyksikölle ei ole määritelty omia käyttötarkoitusrajoitteita, käytetään palvelukokonaisuudelle määriteltyjä käyttötarkoitusrajoitteita

jos monimutkaisia rajoitteita, hoidetaan hakemuslomakkeella

pakollinen lisäpalvelu (-tuote)

esim. perehdytys käytävä kerran; jos on käynyt, lisäpalvelu ei ole enää pakollinen

varattava x pv etukäteen

Vähimmäis- ja maksimipituudet

huom. perustamis- ja purkuajat


#Rajoitteeet

### Henkilön samanaikaisten varausten määrä

* Toimipistetason rajoite
* Varausyksikkökohtainen rajoite

Jos varausyksikölle ei ole määritetty rajoitteita, käytetään 
toimipisteen rajoitteita. Jos varausyksikölle on asetettu rajoite, 
käytetään sitä.

Rajoitus on kuukausikohtainen maksimituntimäärä. 

Maksimituntimäärää tarkistetaan vain tulevaisuuteen, 
menneitä varauksia ei huomioida uutta varausta tehdessä
vaan katsutaan vain, että tästä hetkestä kuukausi
eteenpäin ei saa tehdä kuin maksimituntimäärän varauksia

Rajoitus on toimipistekohtainen, eli toimipisteen
kaikkiin varausyksiköihin saa olla yhteensä
vain toimipisteen maksimituntimäärän verran varauksia. 

Varausyksikön maksimituntimäärä vai vain vähentää toimipisteelle 
määriteltyä maksimituntimäärää. Eli jos toimipisteelle
on määritelty maks 10 tuntia, niin varausyksikölle
voi määritellä vain 10 tuntia pienemmän maksimituntimäärän. 

### Käyttötarkoitus

Varausyksikölle voidaaan määritellä sallittuja
käyttötarkoituksia. Jos käyttötarkoitukset on määritelty,
voi siihen tehdä varauksia vain valittuihin käyttötarkoituksiin.

Jos varausyksikölle ei ole määritetty rajoitteita, käytetään 
palvelukokonaisuuden rajoitteita. Jos varausyksikölle on asetettu rajoite, 
käytetään sitä.

Käyttötarkoituksen mukaan ajalliseen rajoittamiseen
käytetään hauki aukioloaikasovellusta, jonka
atribuuteilla voidaan määritellä mihin
käyttötarkoitukseen varausyksikkö on 
milloinkin käytettävissä.

Varmistettava hauesta, että nykyinen hauen toiminnallisuus
on tähän soveltuva. 

Meidän päähän tähän ei tarvita validointia, eli aukioloajat
eri käyttötarkoituksiin voivat olla päällekkäin. 

### Pakollinen lisäpalvelu

Esim. perehdytys. 

Tämä on hoidettavissa erillisellä varausyksiköllä. Silloin pystytään 
käyttämään jo olemassa olevaa logiikkaa ja mm. aukioloaikojen hallinnointiin
ei tarvitse tehdä muutoksia, sillä saatavuus voi vaihdella, esim. sen mukaan
milloin perehdyttäjä on saatavilla jne. 

#### Henkilökohtaiset oikeudet

Varausyksikölle voi maaritellä mitä oikeuksia
sen varaamisen tarvitsee. Esim. musiikkistudion
varaamiseen tarvitsee pakollisen perehdytyksen.

Henkilölle voidaan henkilökunnan
toimesta antaa oikeuksia, jolloin hänen varattavakseen
tulee tiloja, jotka muuten eivät olisi varattavissa. 

Esim. hankilölle annetaan oikeus, että hän on 
suorittanut perehdytyksen.

#### Henkilökohtaiset rajoitteet

Henkilölle voidaan antaa henkilökunnan toimesta määräaikaisia 
toimipiste- tai palvelusektorikohtaisia käyttökieltoja.
Käyttökiellolla on syy. 

Käyttökielto voidaan antaa esim. maksullisiin
tiloihin maksamattomien laskujen vuoksi.

Ei suuri prioriteetti. 

### Varattava x pv etukäteen

Rajoite on varausyksikkökohtainen. 

### Vähimmäis- ja maksimipituudet

Varauksen vähimmäis- ja maksimipituus.

### Varausten välinen bufferi

Varausyksikölle voidaan määritellä konfiguraatio-optioita. 

Esim. Tila penkeillä ja pöydilla, ilman penkkejä
ja pöytiä jne. 

Konfiguraatioilla voidaan määritellä paljonko
niiden muuttamiseen menee aikaa konfiguraatiosta
toiseen, ja tämä aika on pakollinen
bufferi eri konfiguraatiotyyppisten varausten
välillä. 

Huom. Bufferiajalla voi olla eri hinta kuin
itse varauksella. 

### Rajoitteiden vaikutus tilojen näkkyvyyteen

Aukioloaikojen näkyvyys käyttötarkoituksen mukaan?

Muuten kaikki tilat näkyvissä, vaikka ei pystyisikään
varausta tekemään. 