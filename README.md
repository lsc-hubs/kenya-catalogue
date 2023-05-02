# Desira dataset inventarisation

At this repo we keep a listing of relevant portals and datasets for the desira project

The original [list](portals.csv) has been imported from an excel sheet created by Johan.

A crawl.py script is available which takes this list as a source and extracts as much info as possible from remote sources.

Users can then move into the generated metadata files to add relevant content.

Finally this content will be exported to a set of iso19139 xml files which are loaded in a catalog to provide a searchable interface

## File structure

Each portal is listed as a folder in [portals](portals) folder

Each dataset available via that portal is listed as a folder within the relevant portal folder

Metadata about other types such as scientific articles/reports, software applications/models is still unclear, I suggest to place them in 

- portals/xxx/documents/yyy
- portals/xxx/software/yyy

## Metadata generation

Dataset metadata inherits from portal metadata, so you can for example describe a contact organisation at the portal level, you then don't need to specify it anymore at the dataset level

Metadata follows the [mcf](https://github.com/geopython/pygeometa/blob/master/sample.yml) syntax, a yaml based flavour of iso19139

the [pygeometa](https://github.com/geopython/pygeometa) library is used to generate iso19139 metadata from the mcf files.

The pyGeoDataCrawler scripts facilitates to work with pygeometa on folders of files

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

