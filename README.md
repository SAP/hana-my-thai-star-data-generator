# My Thai Star Data Generator
A data generator that creates sample data for the SAP HANA use-cases of the [devonfw](http://www.devonfw.com/) reference application ([My Thai Star](https://github.com/devonfw/my-thai-star))

# Description

For the HANA-specific use cases of the [My Thai Star](https://github.com/devonfw/my-thai-star) reference application to work, some sample data must be present that can be used as the base data for the predictions and the geospatial analyses.

This data generator can be used to generate the required data.

# Requirements

- Python 3.7
- A SAP HANA database instance
- Installed and configured My Thai Star server

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
pip install -r requirements.txt
```

# Configuration

## Database Access

Open the `config.sample.ini` file.

```
[hana]
host = localhost
port = 30015
user = OASP_TEST
password = Oa5p_test
```

Set up your database connection data and credentials. The data must match the data used for your My Thai Star server.

**Example**

```
[hana]
host = hxehost
port = 39015
user = MY_THAI_STAR_USER
password = My_Pa$$word
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
Holiday data can be obtained from [feiertagskalender.ch](https://www.feiertagskalender.ch/export.php?geo=3060&jahr=2018&klasse=5&hl=en). 

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

# How to obtain support

If you have questions or find a bug, please open an issue in this project's bug tracker.

# Contributing

If you'd like to contribute to this project, please create an issue for the bug or improvement you want to submit.

Once the issue is open, please create a new pull request and reference the issue in the subject message.

# License

Copyright (c) 2018 SAP SE or an SAP affiliate company. All rights reserved.

This file is licensed under the Apache Software License, v. 2 except as noted otherwise in the [LICENSE](https://github.com/SAP/hana-my-thai-star-data-generator/blob/master/LICENSE) file.

