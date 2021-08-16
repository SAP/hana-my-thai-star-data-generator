# My Thai Star Data Generator
A data generator that creates sample data for the SAP HANA use-cases of the [devonfw](http://www.devonfw.com/) reference application ([My Thai Star](https://github.com/devonfw/my-thai-star))

# Description

For the HANA-specific use cases of the [My Thai Star](https://github.com/devonfw/my-thai-star) reference application to work, some sample data must be present that can be used as the base data for the predictions and the geospatial analyses.

This data generator can be used to generate the required data.

# Requirements

- [Python 3.7](https://www.python.org/downloads/) or higher
- A [SAP HANA](https://developers.sap.com/topics/sap-hana-express.html) database instance
- A [Git](https://git-scm.com/downloads) client
- Installed and configured [My Thai Star](https://github.com/devonfw/my-thai-star) server

# Download and Installation

## Download

Clone or download the repository to your local computer. 

```
git clone https://github.com/SAP/hana-my-thai-star-data-generator.git
cd hana-my-thai-star-data-generator
```

## Installation

Use `pip` to install dependencies:

```
$ pip install -r requirements.txt
```

# Configuration

## Database access

Open the `config.sample.ini` file.

```
[hana]
host = localhost
port = 30015
user = OASP_TEST
password = Oa5p_test
express_edition = true
```

Set up your database connection data and credentials. The data must match the data used for your My Thai Star server. If you are using a SAP HANA express edition database you have to set `express_edition` to `true`. If you're using a different SAP HANA edition you can set it to `false` or omit it. This will speed up the generation at the cost of some more server processing time.

**Example**

```
[hana]
host = hxehost
port = 39015
user = MY_THAI_STAR_USER
password = My_Pa$$word
express_edition = true
```

Save the file as `config.ini`.

## Generation base data

Before you can run the data generator, some historical data must be placed into the `resources` directory. This data will be used as the basis for the data generation.

> **NOTE:** The sources of the data listed below are third-party web sites. In order to use the data from these web sites you must accept and comply with the respective terms of use.

### Weather data
Weather data can be obtained from the [DWD website](https://www.dwd.de/DE/leistungen/klimadatendeutschland/klarchivtagmonat.html). 

- On the climate data download page select a suitable weather station, for example, `Frankfurt/Main`
- Click on the download icon
- Save the file to your local computer
- Open the downloaded zip archive and extract the file starting with `produkt_klima_tag` (e.g. `produkt_klima_tag_20161229_20180701_05906.txt`) to the `resources` directory
- Rename the file to `weather.txt`.

### Holiday data
Holiday data can be obtained from [feiertagskalender.ch](https://www.feiertagskalender.ch/export.php?geo=3060&klasse=5&hl=en). 

- Review the [Terms of use](https://www.feiertagskalender.ch/tos.php?geo=3060&hl=en)
- If you agree to the terms of use, download the CSV file and save it to the `resources` directory
- Rename the file to `holidays.csv`.

### Address data
Address data can be obtained from [https://extract.bbbike.org](https://extract.bbbike.org/).

- In the option panel on the left, select "OSM XML 7z (xz)" as the format
- Enter your e-mail address
- Find an area on the map for which you want to get the addresses, either by moving the map or by searching for a city
- Create a bounding box via the button on the left
- Click on the button labeled "extract" to start the extraction
- Save the file to the `resources` directory
- Rename the file to `addresses.xml`

### Name data
Fake names for customer data can be generated at [https://www.fakenamegenerator.com](https://www.fakenamegenerator.com/order.php).

- Review the [Terms of service](https://www.fakenamegenerator.com/terms-of-service.php).
- If you agree to the terms of service, choose a name set and a country that matches the weather and address data
- Add "Given name" and "Surname" to the list of fields to be included
- Enter your e-mail address
- Confirm the CAPTCHA
- Click on the button labeled "Place your free order"
- Save the file to the `resources` directory
- Rename the file to `names.csv`

# Usage

After you have installed and configured the generator you have to first generate the consolidated address data by running the address generator from the generator's root directory.

```
$ python src/address_generator.py
```

Then you can run the main generator from the generator's root directory.

```
$ python src/main.py
```

While the generator is running it will display progress information. The output of a successful generator run looks like the following:

```
Clean up...
Insert users...
100% inserted...
Insert date info...
100% inserted...
Insert orders...
Dish 0: 100% inserted...
Dish 1: 100% inserted...
Dish 2: 100% inserted...
Dish 3: 100% inserted...
Dish 4: 100% inserted...
Dish 5: 100% inserted...
Dish 6: 100% inserted...
Finished.
```

# How to obtain support

If you have questions or find a bug, please open an issue in this project's bug tracker.

# Contributing

If you'd like to contribute to this project, please create an issue for the bug or improvement you want to submit.

Once the issue is open, please create a new pull request and reference the issue in the subject message.

# License

Copyright (c) 2018-2021 SAP SE or an SAP affiliate company and hana-my-thai-star-data-generator contributors. "Please see our [LICENSE](https://github.com/SAP/hana-my-thai-star-data-generator/blob/master/LICENSE) for copyright and license information. Detailed information including third-party components and their licensing/copyright information is available via the [REUSE tool](https://api.reuse.software/info/github.com/SAP/hana-my-thai-star-data-generator).
