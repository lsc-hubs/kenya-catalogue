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

Run the import-csv script for a folder

```

```

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