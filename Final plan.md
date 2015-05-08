
link to Bisque?

tables to link iDs/ ID mapping
-Affy
-entrez id
-gene symbol

data tables in mysql:
-new pp hum


cgi scripts go in cgi-bin in final

chmod cgi-bin/ 755 (or 777)

744 for read permissions folders
644 for files


tail -25 /var/log/httpd/error\_log



for matplotlib:

import tempfile
import os
os.environ[‘MPLCONFIGDIR’][1] = tempfile.mkdtemp()





## think about way to use the pathway info:
- networks colored by pathway
- networks limited to selected pathways (checkbox which ones)


## ways to incorporate GO data


## Two types of queries.
1. Individual genes, returns detailed information on interacting proteins
2. Up to x many genes, to return and analyze network

## include selection for different gene ID types


## To show individual interactions:
first get interacting genes from each int reference 
-for each interacting gene make a dict, tracking what datasets had it and giving annotation information.
-could present each query gene seperately or as one combined table.
-allow user to select which databased to search

[1]:	%20