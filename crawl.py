import datetime
import numpy as np
import pandas as pd
import os, yaml, json, re, owslib
import requests as req
from yaml.loader import SafeLoader
from lxml import html

source = "."
target = "./portals"

def create_initial(path,id,label,desc,author,url):
    cnf = {
        "identifier": id,
        "url": url,
        "name": label,
        "abstract": desc,
        "contact": {
            "name": "",
            "organisation": author,
            "email": ""
        },
        "license": ""
    }
    if 'doi' in url:
        cnf['datasetidentifier'] = url
    try:
        with open(path, 'w') as f:
            yaml.dump(cnf, f)
    except Exception as e:
        print('file '+ path +' can not be written, check it; '+ str(e))
   

myPortals = pd.read_csv(source+os.sep+'portals.csv',sep=';')
for index, row in myPortals.iterrows():
    print(row['url'], row['label'])
    
    headers = {"Accept":"application/json, text/xml, text/html", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Python/3.9 pgdc/1.1" }

    # we should check the url, maybe the url is forwarded (from doi, or no longer existing location)
    try:
        resp = req.get(row['url'],headers=headers,verify=False)
    except Exception as e:
        print('request to ' + row['url'] + ' failed');
        continue
    if resp.status_code > 299:
        print('request to ' + row['url'] + ' has status code: ' + str(resp.status_code));
        continue

    # then check resp.url
    # get domain as identifier for the catalogue (if multiple catalogues live in a domain, they are merged)
    domain = row['country'] +os.sep+ resp.url.split('//')[1].split('/')[0]

    # check if domain-folder exists, else create it
    if os.path.isdir(target+os.sep + domain):
        # already exits; update metadata
        print(target+os.sep+domain+' already exits')
        try:
            with open(os.path.join(target+os.sep+domain+os.sep, 'index.yml')) as f:
                portalMD = yaml.load(f, Loader=SafeLoader)
        except FileNotFoundError:  # filenotfound, create it
            create_initial(os.path.join(target+os.sep+domain+os.sep, 'index.yml'),domain,row.get('label'),row.get('description'),"",row['url'])
        except Exception as e:
            print('file '+ os.path.join(target+os.sep+domain+os.sep, 'index.yml') +' can not be read, check it; '+ e)
    else:
         os.makedirs(target+os.sep+domain)
         create_initial(os.path.join(target+os.sep+domain+os.sep, 'index.yml'),domain,row.get('label'),row.get('description'),"",row['url'])

    ## FETCH PORTAL METADATA
    #try:
    abs = ""
    content_type = resp.headers['content-type'].split(';')[0]
        # if website, check title/abstract, schema-org or similar
    if (content_type == 'text/html'):
        tree = html.fromstring(resp.content)
        ttl = tree.xpath('//title/text()')
        if len(ttl) == 0:
            ttl = str(row.get('label'))
        else:
            ttl = str(ttl[0])
        abs = tree.xpath('//meta[@name="description"]/@content/text()')
        if len(abs) == 0:
            abs = str(tree.xpath('//meta[@name="og:description"]/@content/text()'))
        if len(abs) > 0:
            abs=str(abs[0])
        else:
            abs=str(row.get('description'))
        author = tree.xpath('//meta[@name="author"]/@content/text()')
        if len(author) > 0:
            author = str(author[0])
        else:
            author = ""
        schemaorg = tree.xpath('//script[@type="application/ld+json"]/text()')
        try:
            if len(schemaorg) > 0:
                schemaorg = json.loads(schemaorg[0])
                ttl = str(schemaorg.get('name',ttl))
                abs = str(schemaorg.get('description',abs))
        except Exception as e:
            print('fail parsing schema.org '+ str(e) + ', json: '+ str(schemaorg))
        print(ttl, abs, author) 
    elif (content_type == 'application/json'):    # if API, identify the type of API, if it is OPENAPI, CSW, OAI-PMH, Dataverse, CKAN, WMS/WFS fetch metadata from conventions
        print('json')
        # see if it is openapi, json-ld, odata, ...
        ttl=resp.url.split('/index')[0].split('?')[0].split('#')[0].strip("/").split('/')[-1].split('.')[0]
        if not ttl:
            ttl = str(row.get('label'))
    elif (content_type in ['text/xml','application/xml']):
        print('xml')
        # see if it is wms/wfs/iso/wcs/csw etc
        ttl=resp.url.split('/index')[0].split('?')[0].split('#')[0].strip("/").split('/')[-1].split('.')[0]
        if not ttl:
            ttl = row.get('label')
    else:
        ttl=resp.url.split('/index')[0].split('?')[0].split('#')[0].strip("/").split('/')[-1].split('.')[0]
        if not ttl:
            ttl = row.get('label')
        print('other: '+ content_type)
    
    ## Parse the datasets in this portal

    ds_folder = target+os.sep+domain+os.sep+'datasets'+os.sep

    # what is the portal type, act accordingly
    # portal endpoint is in row['alt-url'], api type is in row['api']

    if row['api'] == "CSW":
        print("start CSW harvest: " + row['alt-url'])
        from owslib.csw import CatalogueServiceWeb
        from owslib.fes import PropertyIsEqualTo, PropertyIsLike, BBox
        try:
            csw = CatalogueServiceWeb(row['alt-url'])
            qry = PropertyIsEqualTo('csw:AnyText', 'dataset')
            csw.getrecords2(constraints=[qry], outputschema='http://www.isotc211.org/2005/gmd', maxrecords=20)
            for r in csw.records:
                rec=csw.records[r]
                if len(rec.identifier) > 0:
                    if not os.path.isdir(ds_folder+rec.identifier):
                        os.makedirs(ds_folder+rec.identifier)
                    with open(ds_folder + rec.identifier + os.sep + rec.identifier + ".xml", 'w') as f:
                        try:
                            f.write(str(rec.xml.decode("utf8")))
                        except:
                            f.write(str(rec.xml))
        except Exception as e:
            print("Harvest from CSW " + row['alt-url'] + " failed. " + str(e))
            
    elif row['api'] == "OAI":
        print ("harvest oai")
        try:
            from oaipmh.client import Client
            from oaipmh.metadata import MetadataRegistry, oai_dc_reader
            registry = MetadataRegistry()
            registry.registerReader('oai_dc', oai_dc_reader)
            client = Client(row['alt-url'].split('?')[0], registry)
            for record in client.listRecords(metadataPrefix='oai_dc'): #set=xxx to filter on set
                id=record[1]._map.get('identifier',[''])[0].replace("https://","").replace("/","_").replace("www.","")
                if len(id) > 0:
                    if not os.path.isdir(ds_folder+id):
                        os.makedirs(ds_folder+id)
                    with open(ds_folder + id + os.sep + id + ".yml", 'w') as f:
                        yaml.dump(record[1]._map,f)
        except Exception as e:
            print("Harvest from OAI " + row['alt-url'] + " failed. " + str(e))

    elif row['api'] == "sitemap":
        print ("sitemap, not yet implemented")
    elif row['api'] == "WMS": #WMS, WFS, WCS, WMTS ...
        print("start WMS harvest: " + row['alt-url'])
        from owslib.wms import WebMapService
        try:
            wms = WebMapService(row['alt-url'],version='1.3.0')
        except:
            try:
                wms = WebMapService(row['alt-url'], version='1.1.1')
            except Exception as e:
                print("Harvest from WMS " + row['alt-url'] + " failed. " + str(e))
        if (wms):
            print ('version:',wms.identification.version)
            idf = wms.identification
            default = { 'title': idf.title,
                      'abstract': idf.abstract,
                      'keywords': idf.keywords,
                      'accessconstraints': idf.accessconstraints,
                      'fees': idf.fees }

            contact = {
                          'pointOfContact': {
                             'organization': wms.provider.name,
                             'url': wms.provider.url,
                             'individualname': wms.provider.name,
                             'email': wms.provider.contact.email,
                             'address': wms.provider.contact.address,
                             'city':wms.provider.contact.city,
                             'administrativearea': wms.provider.contact.region,
                             'postalcode': wms.provider.contact.postcode,
                             'country':wms.provider.contact.country,
                             'positionname': wms.provider.contact.position
                          }}

            for i, (k, layer) in enumerate(wms.contents.items()):
                lyrmd = default.copy()

                lyrmd['name'] = layer.name
                lyrmd['abstract'] = layer.abstract or lyrmd['abstract']
                lyrmd['title'] = layer.title or lyrmd['name']
                lyrmd['keywords'] = {'default': {'keywords': layer.keywords}}
                lyrmd['extents'] = {'spatial': [{'bbox': list(layer.boundingBoxWGS84) }]}
                # todo: if 'metadataUrls', fetch metadata, get identifier
                # todo: on owslib, extract identifier

                distribution = { id : { 'url': row['alt-url'], 'type': 'OGC:WMS', 'name': layer.name } }

                id = layer.name # (better use code, seems not on owslib)
                # todd: fetch image from wms as thumbnail
                # todo: fetch identifier, create folder
                # todo: add wms url
                if not os.path.isdir(ds_folder + id):
                    os.makedirs(ds_folder + id)
                with open(ds_folder + id + os.sep + id + ".yml", 'w') as f:
                    yaml.dump({'mcf':1.0,
                        'distribution': distribution,
                        'metadata':{ 'identifier':id,'hierarchylevel':'dataset',
                        'datestamp': datetime.datetime.now()
                        }, 'contact':contact,'identification':lyrmd}, f)
    elif row['api'] == "OWS": #WMS, WFS, WCS, WMTS ...
        print ("ows, not yet implemented")
    else: # now loop though the various url's act as resources

        # create safe folder name (or use identifier, if we know it)

        fldrnm = "".join([c for c in ttl if re.match(r'\w', c)])
        fldr = ds_folder+os.sep+fldrnm

        if os.path.isdir(fldr):
            print('folder '+ fldr +' exists')
        else:
            os.makedirs(fldr)
            if (schemaorg):
                with open(os.path.join(fldr+os.sep, 'index.yml'), 'w') as f:
                    yaml.dump(schemaorg, f)
            else:
                create_initial(os.path.join(fldr+os.sep, 'index.yml'),fldrnm,ttl,abs,author,row['url'])

            # see if the row includes a doi, if so fetch the doi metadata (datacite)

            ## Maybe the row has a dataset on an existing portal, always add a dataset folder, initially and next for second, third

        

    #except Exception as e:
    #        print(e)
    
