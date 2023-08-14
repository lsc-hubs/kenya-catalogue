# Kenya Land Soil Crop Catalogue

A catalogue for Kenyan LSC datasets, services and applications. The content of this catalogue is published at intervals at https://kenya.lsc-hubs.org. This repository is an experimental setup to research participatory content management in the land soil crop domain.

## Land Soil Crop Hubs project

The [DESIRA LSC](https://lsc-hubs.org/) project is a work in progress. The objective of this project is to develop sustainable land, soil, crop information hubs in national agricultural research organizations in East Africa to enhance the effectiveness of national Agricultural Knowledge and Innovation Systems (AKIS) and contribute to rural transformation and climate-smart agriculture. Read more on the [lsc-hubs website](https://lsc-hubs.org)

## Contribute to this repository

You can participate in [discussions](https://github.com/lsc-hubs/kenya-catalogue/discussions), or fork this repository and create [pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) to suggest content updates directly.

## Metadata as files

Each file in the repository represents a metadata record describing a resource.

Record files are clustered by source (portal) in a [portals](portals) folder, by spatial scope (Global, Africa, Country).

Records are stored in the [metadata control file](https://geopython.github.io/pygeometa/reference/mcf/) format (MCF). MCF is a subset of [ISO19139:2007](https://www.iso.org/standard/32557.html), encoded in [YAML](https://www.yaml.io/spec/). 

Use a text editor (preferably with YML validation/syntax highlighting) to edit YML files. Alternatively an online tool exists to create and edit MCF files at https://osgeo.github.io/mdme. Open the relevant file, update the form and save the yml file to the relevant folder.

Dataset metadata inherits from portal metadata, so you can for example describe a contact organisation at the portal level (index.yml), you then don't need to specify it anymore at the dataset level

## iso19139 metadata generation

The [pygeometa](https://github.com/geopython/pygeometa) library is used to generate iso19139 metadata from the mcf files. This iso19139 metadata is then uploaded into the catalogue at https://kenya.lsc-hubs.org.

The process of catalogue publication is triggered with every change on the github repository using github actions.

The Github action pushes the changes to a remote repository at Wageningen University, which is the location where the catalogue is currently hosted. Git Actions uses pygeodatacrawler to export iso19139 and [pycsw administration](https://docs.pycsw.org/en/latest/administration.html#loading-records) to load the content into the catalogue.

## pygeodatacrawler

[pygeodatacrawler](https://www.piwheels.org/project/geodatacrawler/) facilitates to work with pygeometa within a repository of mcf files.

### Generate MCF from data files

Run the init script for a folder, if no yml file exists, the script will create a yml file (using properties of the data file) for each data file.

```
crawl-metadata --mode=init --dir="/Projects/desira/dataset-inventarisation/portals/Africa/*"
```

### Import CSV

Import metadata from a index.csv, make sure a index.j2 exists mapping the sheet colums to a mcf property.

```
crawl-metadata --mode=import-csv --dir="/Projects/desira/dataset-inventarisation/portals/Africa/*"  --sep=";"
```

### Import from DOI or CSW

The above approach can be comibed with an option to import existing metadata from an online location. Provide the records to be imported as url in a csv. The url is mapped to the dataset-uri field in mcf, which is used to import external metadata by the `update` method.

```
crawl-metadata --mode=import-csv --dir="/Projects/desira/dataset-inventarisation/portals/Africa/*"  --sep=";"
crawl-metadata --mode=update --dir="/Projects/desira/dataset-inventarisation/portals/Africa/*" 

```
### Export to ISO

Export a repository to a series of iso documents

```
crawl-metadata --mode=export --dir="/Projects/desira/dataset-inventarisation/portals/*" --dir-out=/temp
```






