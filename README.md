# COVID Worldwide Scrapers

- [Oveview](#overview)
- [Install](#install)
- [Use](#use)
- [Data sources](#data-sources)

## Overview

This repo contains web scrapers for COVID-19 data
from countries around the world.

These scrapers collect data for administrative units within countries
(provinces, states, territories) for coronavirus cases and deaths.

## Install

Download [Geckodriver](https://github.com/mozilla/geckodriver/releases) to a location on the PATH (or update PATH env variable to include it's location).

```
pip install git+https://github.com/biglocalnews/covid-world-scraper#egg=covid-world-scraper
```

## Use

```
# Provide one or more 3-letter ISO country codes to scrape
covid-world-scraper pak deu bra # Pakistan, Germany Brazil
```

By default, data for each country is stored in `/tmp/covid-world-scraper`.

For each country, scrapers download and store one or more file artifacts in a `raw`
directory. These files may be screenshots, HTML, Excel files, etc. Data
extracted from these raws sources are stored in a `processed` directory
for each country. Files in both directories are named based on the
UTC runtime of the scraper.

Here's an example:

```
covid-world-scraper/pak
├── processed
│   ├── 20200627T0124Z.csv
│   ├── 20200627T0126Z.csv
│   └── 20200628T1705Z.csv
└── raw
    ├── 20200627T0124Z.html
    ├── 20200627T0124Z.png
    ├── 20200627T0124Z.txt
    ├── 20200627T0126Z.html
    ├── 20200627T0126Z.png
    ├── 20200627T0126Z.txt
    ├── 20200628T1705Z.html
    ├── 20200628T1705Z.png
    └── 20200628T1705Z.txt
```

## Data sources

- [Brazil](https://covid.saude.gov.br/)
- [Germany](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html)
- [India](https://www.mohfw.gov.in/)
- [Nigeria](https://covid19.ncdc.gov.ng/)
- [Pakistan](http://covid.gov.pk/stats/pakistan)
- [South Africa](https://sacoronavirus.co.za/category/press-releases-and-notices/)

Countries that share PDFs:

- [Indonesia](https://covid19.kemkes.go.id/category/situasi-infeksi-emerging/info-corona-virus/#.XuGkb2pKiL_)
- [Mayanmar](https://mohs.gov.mm/page/9575)
- [Russia](https://xn--80aesfpebagmfblc0a.xn--p1ai/info/ofdoc/reports/)
- [Spain](https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm)
