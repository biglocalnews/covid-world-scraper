# COVID World Scrapers

- [Overview](#overview)
- [Install](#install)
- [Use](#use)
- [Data sources](#data-sources)

## Overview

This project provides a command-line tool for scraping COVID-19 data
from countries around the world.

The scrapers target the subset of countries that offer coronavirus data at the level
of administrative units (provinces, states, territories *within a country*).

Organizations such as [Johns Hopkins University][] are a better resource for
comprehensive country-wide figures.

[Johns Hopkins University]: https://coronavirus.jhu.edu/data

## Install

Download [Geckodriver](https://github.com/mozilla/geckodriver/releases) to a location on the PATH (or update PATH env variable to include it's location).

Install the `covid-world-scraper` command-line tool.

```
pip install git+https://github.com/biglocalnews/covid-world-scraper#egg=covid-world-scraper
```

## Use

The `covid-world-scraper` command-line tool lets you download the
current data for a country by supplying one or more 3-letter [ISO country codes][].

[ISO country codes]: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3

```
# Brazil, Germany, Pakistan
covid-world-scraper bra deu pak
```

By default, data for each country is stored in `/tmp/covid-world-scraper`.

For each country, scrapers download and store one or more file artifacts in a `raw`
directory. These files may be screenshots, HTML, Excel files, etc. Data
extracted from these raw sources are stored in a `processed` directory
for each country. Files in both directories are named based on the
UTC runtime of the scraper.

Below is an example showing file artifacts generated by the Pakistan scraper
on two consecutive days in June 2020.

> The types of `raw` files saved for a given country vary
> widely and reflect the different ways each country posts it data.

```
covid-world-scraper/pak
├── processed
│   ├── 20200627T0126Z.csv
│   └── 20200628T1705Z.csv
└── raw
    ├── 20200627T0126Z.html
    ├── 20200627T0126Z.png
    ├── 20200627T0126Z.txt
    ├── 20200628T1705Z.html
    ├── 20200628T1705Z.png
    └── 20200628T1705Z.txt
```
