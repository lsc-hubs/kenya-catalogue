# Kenya Land Soil Crop Catalogue

A catalogue for Kenyan LSC datasets, services and applications. The content of this catalogue is published at intervals at https://kenya.lsc-hubs.org.

## Work in progress
The [DESIRA LSC](https://lsc-hubs.org/) project is a work in progress. This repository is an experimental setup to research participatory content management in the land soil crop domain.

## Contribute to this repository

You can participate in [discussions](https://github.com/lsc-hubs/kenya-catalogue/discussions), or fork this repository and create [pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) to suggest content updates directly.

## Metadata control file
Records on this repository are stored in the [metadata control file](https://geopython.github.io/pygeometa/reference/mcf/) format (MCF). MCF is a subset of [ISO19139:2007](https://www.iso.org/standard/32557.html), encoded in [YAML](https://www.yaml.io/spec/). 

## LSC Hubs
The objective of this project is to develop sustainable land, soil, crop information hubs in national agricultural research organizations in East Africa to enhance the effectiveness of national Agricultural Knowledge and Innovation Systems (AKIS) and contribute to rural transformation and climate-smart agriculture. Read more on the [lsc-hubs website](https://lsc-hubs.org)

## File structure

Datasets are clustered by source (portal) in a [portals](portals) folder.

Metadata about other types such as scientific articles/reports, software applications/models is still unclear, I suggest to place them in 

- portals/xxx/documents/yyy
- portals/xxx/software/yyy

## Metadata generation

Dataset metadata inherits from portal metadata, so you can for example describe a contact organisation at the portal level (index.yml), you then don't need to specify it anymore at the dataset level

The [pygeometa](https://github.com/geopython/pygeometa) library is used to generate iso19139 metadata from the mcf files.

The [pyGeoDataCrawler](https://www.piwheels.org/project/geodatacrawler/) scripts facilitates to work with pygeometa on folders of files

Run the import-csv script for a folder, if no yml file exists, the script will create a yml file (using properties of the data file) for each data file.

```
crawl-metadata --mode=init --dir="/Projects/desira/dataset-inventarisation/portals/Africa/*"
```

## MDME

Alternatively you can create the file manually. An online tool exists to create mcf files at https://osgeo.github.io/mdme. Populate the form and save the yml file to the relevant folder.

## Import CSV

Import metadata from a {file}.csv, make sure a {file}.j2 exists mapping the sheet colums to a mcf property.

```
crawl-metadata --mode=import-csv --dir="/Projects/desira/dataset-inventarisation/portals/Africa/*"  --sep=";"

```

## Import from DOI or CSW

The above approach can be comibed with an option to import existing metadata from an online location. Provide the records to be imported as url in a csv. The url is mapped to the datasetuir field in mcf, which is used to import external metadata by the `update` method.

```
crawl-metadata --mode=import-csv --dir="/Projects/desira/dataset-inventarisation/portals/Africa/*"  --sep=";"
crawl-metadata --mode=update --dir="/Projects/desira/dataset-inventarisation/portals/Africa/*" 

```
## Export to ISO and import to pycsw

A ci-cd process has been set up to export mcf to iso19139 and load the iso19139 records into pycsw (or any other catalogue).

## Identification and interlinking

Portals are identified by there domain name. A limitation is that multiple portals at a single domain can not be distinguished. Consider that search engines apply a similar convention. The portal folder name is considered the identification of the portal.

The dataset folder name is the identification of a dataset.
Datasets are usually identified by a UUID, if the crawler was unable to fetch the uuid, it will generate a uuid from the portal and dataset name. 

Linking from a dataset to another dataset (or other described resource) within the current repository can be done by referencing the dataset folder name (identifier). It means that dataset identifiers should be unique. A mechanism should be introduced to warn about duplication of identifiers. Such a warning can mean 2 things:

- a dataset is provided by multiple portals
- 2 datasets share a identifier

## Prevent overwriting manual contributions by the crawler

Mind that the crwaler currently does not have a mechanism to prevent overwriting of manual contributions. 
One idea could be to use GIT branches to rebase manual contributions to the latest crawler results.

## Catalogue publication

The process of catalogue publication is triggered at pushes to github using github actions.

Github actions pushes the changes to a remote repository at Wageningen University, which is the location where the catalogue is currently hosted. 

