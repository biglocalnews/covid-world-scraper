# COVID Worldwide Scrapers

Country-specific data scrapers for COVID-19 stats.

In collaboration with Pitch and Google News Lab, Big Local News is collecting data from countries at the regional level for coronavirus cases and deaths. We are scraping websites daily for updates and collecting historical data when available.

Cheryl created a google spreadsheet with links to start with, [here](https://docs.google.com/spreadsheets/d/1cfrT2l5hdIRP582SnFV-8ZOlSsctX5x_YB-V6QmTylk/edit#gid=0).

Scrapers completed:

- [X] [Germany](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html)
- [X] [India](https://www.mohfw.gov.in/)
- [X] [Nigeria](https://covid19.ncdc.gov.ng/)
- [X] [South Africa](https://sacoronavirus.co.za/category/press-releases-and-notices/)
- [X] [Pakistan](http://covid.gov.pk/stats/pakistan)
- [X] [Brazil](https://covid.saude.gov.br/)

***A Note:*** Both the Brazil and Pakistan scrapers use Selenium and the Firefox geckodriver for the webscrapes. All other scrapers extract data with BeautifulSoup.

Countries that share PDFs:

- [X] [Spain](https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm)
- [ ] [Indonesia](https://covid19.kemkes.go.id/category/situasi-infeksi-emerging/info-corona-virus/#.XuGkb2pKiL_)
- [ ] [Russia](https://xn--80aesfpebagmfblc0a.xn--p1ai/info/ofdoc/reports/)
- [ ] [Mayanmar](https://mohs.gov.mm/page/9575)

* scraper to grab PDF created - however, a follow up process is needed to extract the data

Questions for our Meeting:

- What is the ideal format for the data?
- What is the plan for rolling the map out?
- Will we wait until we gather all of the data to publish it?
- What are the expectations in terms of scrapers?
- What is the minimum necessary to publish the map? (Hopefully we will far exceed an MVP - but we still need to define one)
- What are the questions PITCH has for us?



