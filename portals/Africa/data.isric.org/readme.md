# importing a csv of uuids from geonetwork

create a csv of identifier with a basic j2 template

on geonetwork, make a selection and open https://data.isric.org/geonetwork/srv/api/selections/s101 to get a list with current selection

```
poetry run crawl-metadata --mode=import-csv --dir=/mnt/c/Users/genuc003/Projects/desira/dataset-inventarisation/portals/Africa/data.isric.org/
poetry run crawl-metadata --mode=update --dir=/mnt/c/Users/genuc003/Projects/desira/dataset-inventarisation/portals/Afrika/data.isric.org/
```

