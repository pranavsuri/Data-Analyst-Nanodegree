# P3: Wrangling OpenStreetMap Data
> OpenStreetMap data of San Francisco, California is audited, cleaned and stored in an SQLite database. The database is then queried to extract information related to users contributing to the database & the amenities in the region. The project also provides suggestions for improving the data quality.

## About
In this project, wrangling and cleaning of a large dataset (>50MB) are performed. The data is then imported to a database (SQLite) for querying. The data was extracted from [OpenStreetMap (OSM)](https://www.openstreetmap.org) with the area of choice being San Francisco, California.

#### The activities implemented in this project are:
1. For the area of study, download an XML-OSM raw dataset from [OpenStreetMap](https://www.openstreetmap.org).

2. Audit and clean your dataset, converting it from XML to CSV format.

3. Import the cleaned .csv files into a SQL database.

4. Explore the data using SQL queries.

5. Report the findings.

Since the size of the original data was very large (1.42 GB), steps 2-4 were performed on a subset of the original data. After the code was checked, it was checked on the original data.

## Learning Outcome
The project helped me learn to write code to assess the quality of data for validity, accuracy, completeness, consistency, and uniformity. Also, this was my first experience for using sampling to test the code before applying on the more extensive dataset.

## Files
- `audit.py:` This script contains the auditing and cleaning functions. This file is a dependency of `shaping_csv.py`.

- `shaping_csv.py`: The main script which creates the CSV files from the OSM data.

- `creating_database.py`: This script creates databases and tables and, then inserts the relevant data into it.

- `query_on_database.py`: This script contains all the SQL queries.

- `sample.osm`: This file contains a sample data from the
original San Francisco database.

- `sampler.py`: This script samples the original OSM file by taking every 'k' observations.

- `Report.html`: Report summarizing the project workflow.

- All other files in this directory are helper scripts, mostly from the Case Study Quizzes during the lessons.

## Requirements
To download the dataset, use the [Overpass API](http://overpass-api.de/query_form.html) to download a custom square area. The following query is used in general:

`(node(minimum_latitude, minimum_longitude, maximum_latitude, maximum_longitude);<;);out meta;`

For a specific area, you can use the Open Street Map Export Tool to find the coordinates of your bounding box. For San Francisco California, the query is

`(node(37.6392,-122.6637,37.8391,-122.2861);<;); out meta;`

This project requires **Python 3** and was developed using [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for data related projects.

## License
[Modified MIT License © Pranav Suri](/License.txt)
