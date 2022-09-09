# desira dataset inventarisation

At this repo we keep a listing of relevant portals and datasets for the desira project

The original [list](portals.csv) has been imported from an excel sheet created by Johan.

A crawl.py script is available which takes this list as a source and extracts as much info as possible from remote sources.

Users can then move into the generated metadata files to add relevant content.

Finally this content will be exported to a set of iso19139 xml files which are loaded in a catalog to provide a searchable interface

## file structure

Each portal is listed as a folder in [portals](portals) folder

Each dataset available via that portal is listed as a folder within the relevant portal folder

Metadata about other types such as scientific articles/reports, software applications/models is still unclear, I suggest to place them in 

- portals/xxx/documents/yyy
- portals/xxx/software/yyy

## metadata generation

Dataset metadata inherits from portal metadata, so you can for example describe a contact organisation at the portal level, you then don't need to specify it anymore at the dataset level

Metadata follows the [mcf](https://github.com/geopython/pygeometa/blob/master/sample.yml) syntax, a yaml based flavour of iso19139

the [pygeometa](https://github.com/geopython/pygeometa) library is used to generate iso19139 metadata from the mcf files.

