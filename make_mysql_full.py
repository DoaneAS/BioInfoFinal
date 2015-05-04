import MySQLdb as mdb
import sys
network_file = "PPs/HI-II-14.tsv"

with open(network_file) as f:
    header = f.readline()
    netw = [(l.strip().split('\t')) for l in f]

with open(network_file) as f:
    header = f.readline()
    netw = [(l.strip().split('\t')) for l in f]

ppi_key = set()
for p in netw:
    entrezA = p[0]
    entrezB = p[2]
    geneA = p[1]
    geneB = p[3]
    ppi_key.add(tuple(sorted([p[0], p[2]])))
ppi_key

gene_key = set()
for p in netw:
    entrezA = p[0]
    entrezB = p[2]
    geneA = p[1]
    geneB = p[3]
    A = (entrezA, geneA)
    B = (entrezB, geneB)
    gene_key.add(A)
    gene_key.add(B)



genes = [i for i in gene_key]

#ppi_rec = [[[i for i in p], [i for i in p][0], [i for i in p][1]] for p in ppi_key]
ppi_rec=[(i, i[0], i[1]) for i in ppi_key]

ppi_tab = [i for i in ppi_key]

prs = []
for d in ppi_tab:
    x =  ("""'%s, %s'""") %(d[0], d[1])
    unit = (x, d[0], d[1])
    prs.append(unit)

data_pairs = []
for d in netw:
    ep =  ("""'%s, %s'""") %(d[0], d[2])
    gp = ("""%s, %s""") %(d[1], d[3])
    ga = ("'%s'") %(d[1])
    gb = ("'%s'") %(d[3])
    #unit = (ep, d[0], d[2], d[1], d[3])
    unit = (ep, d[0], d[2], ga, gb)
    data_pairs.append(unit)

def connect():
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    try:
        #con = mdb.connect(**dbdata);
        #con = mdb.connect('localhost', 'root', '6194', 'adtest')
        #cur = con.cursor()
        cur.execute("SELECT VERSION()")

        ver = cur.fetchone()

        print "Database version : %s " % ver

    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:

        if con:
            con.close()

connect()


# def make_table3(data):
#     con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
#     cur = con.cursor()
#     try:
#         #con = mdb.connect(**dbdata);
#         cur.execute("""DROP TABLE IF EXISTS genes""")
#         cur.execute("CREATE TABLE `genes` ("
#             "  `gene_id` varchar(30) DEFAULT NULL,"
#             "  `entrez_id` varchar(30) NOT NULL DEFAULT '',"
#             "  PRIMARY KEY (`entrez_id`))")

#         cur.execute("""DROP TABLE IF EXISTS PPI""")
#         cur.execute("""CREATE TABLE PPI (entrezPair VARCHAR(20) PRIMARY KEY NOT NULL,
#                     entrezA VARCHAR(10), entrezB VARCHAR(10), symbolA VARCHAR(20), symbolB VARCHAR(20))""")



#         for d in data:
#             #x = ("%s %s") %(d[0], d[1])
#             cur.execute("""INSERT INTO PPI VALUES (%s, %s, %s, %s, %s)""" %(d[0], d[1],d[2], d[3], d[4]))
#             con.commit()



#     except mdb.Error, e:

#         print "Error %d: %s" % (e.args[0],e.args[1])
#         sys.exit(1)

#     finally:

#         if con:
#             con.close()


def make_table4(data):
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    try:
        #con = mdb.connect(**dbdata);
        cur.execute("""DROP TABLE IF EXISTS genes""")
        cur.execute("CREATE TABLE `genes` ("
            "  `gene_id` varchar(30) DEFAULT NULL,"
            "  `entrez_id` varchar(30) NOT NULL DEFAULT '',"
            "  PRIMARY KEY (`entrez_id`))")

        cur.execute("""DROP TABLE IF EXISTS PPI""")
        cur.execute("""CREATE TABLE PPI (`primary_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
            entrezPair VARCHAR(20) NOT NULL,
            entrezA VARCHAR(10), entrezB VARCHAR(10), symbolA VARCHAR(20),
            symbolB VARCHAR(20),
            PRIMARY KEY (`primary_id`),
            KEY `PPI_index_entrezPair` (`entrezPair`),
            KEY `PPI_index_entrezA` (`entrezA`),
            KEY `PPI_index_entrezB` (`entrezB`),
            KEY `PPI_index_symbolA` (`symbolA`),
            KEY `PPI_index_symbolB` (`symbolB`)) ENGINE=MyISAM DEFAULT CHARSET=latin1""")



        for d in data:
            #x = ("%s %s") %(d[0], d[1])
            cur.execute("""INSERT INTO PPI(entrezPair, entrezA, entrezB, symbolA, symbolB) VALUES (%s, %s, %s, %s, %s)""" %(d[0], d[1],d[2], d[3], d[4]))
            con.commit()



    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:

        if con:
            con.close()
make_table4(data_pairs)
#make_table(prs)
#make_table3(data_pairs)


def make_pub():
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    try:
        #con = mdb.connect(**dbdata);
        cur.execute("""DROP TABLE IF EXISTS `gene2pubmed`""")
        cur.execute("""CREATE TABLE `gene2pubmed` (
                    `primary_id` bigint(20) NOT NULL,
                    `tax_id` int(11) DEFAULT NULL,
                    `gene_id` int(11) DEFAULT NULL,
                    `pubmed_id` varchar(30) DEFAULT NULL,
                    PRIMARY KEY (`primary_id`), KEY `gene2pubmed_index` (`gene_id`)) ENGINE=MyISAM DEFAULT CHARSET=latin1""")



        cur.execute("""DROP TABLE IF EXISTS `gene_info`""")

        cur.execute("""CREATE TABLE `gene_info` (
                    `primary_id` bigint(20) NOT NULL,
                    `tax_id` int(11) DEFAULT NULL,
                    `gene_id` int(11) DEFAULT NULL,
                    `symbol` varchar(50) DEFAULT NULL,
                    `locusTag` varchar(30) DEFAULT NULL,
                    `synonyms` text,
                    `dbXrefs` text,
                    `chromosome` text,
                    `map_location` text,
                    `description` text,
                    `type_of_gene` varchar(30) DEFAULT NULL,
                    `symbol_nomen` varchar(30) DEFAULT NULL,
                    `full_name_nomen` text,
                    `status_nomen` varchar(30) DEFAULT NULL,
                    `other_designations` text,
                    `mod_date` date DEFAULT NULL,
                    PRIMARY KEY (`primary_id`),
                    KEY `gene_info_indextax` (`tax_id`),
                    KEY `gene_info_indexsym` (`symbol_nomen`),
                    KEY `gene_info_index_symbol` (`symbol`),
                    KEY `gene_info_index` (`gene_id`)
                    ) ENGINE=MyISAM DEFAULT CHARSET=latin1""")

        cur.execute("""DROP TABLE IF EXISTS `gene2go`""")

        cur.execute("""CREATE TABLE `gene2go` (
                    `primary_id` bigint(20) NOT NULL,
                    `tax_id` int(11) DEFAULT NULL,
                    `gene_id` int(11) DEFAULT NULL,
                    `go_id` varchar(30) DEFAULT NULL,
                    `evidence` varchar(250) DEFAULT NULL,
                    `qualifier` varchar(250) DEFAULT NULL,
                    `go_term` varchar(250) DEFAULT NULL,
                    `pubmed_ids` varchar(250) DEFAULT NULL,
                    `category` varchar(100) DEFAULT NULL,
                    PRIMARY KEY (`primary_id`),
                    KEY `gene2go_index` (`gene_id`)
                    ) ENGINE=MyISAM DEFAULT CHARSET=latin1""")


    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:

        if con:
            con.close()

def import_data():
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    try:

        cur.execute("""LOAD DATA LOCAL INFILE "data/sql/gene2pubmed" INTO TABLE gene2pubmed""")
        cur.execute("""LOAD DATA LOCAL INFILE "data/sql/gene_info" INTO TABLE gene_info""")
        cur.execute("""LOAD DATA LOCAL INFILE "data/sql/gene2go" INTO TABLE gene2go""")

    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:

        if con:
            con.close()

print "Creating tables"
make_pub()

print "importing data"
import_data()

import csv
path_file = "data/Rolland/ca_pathways.csv"
ca_path = []
with open(path_file) as f:
    rec = csv.reader(f, delimiter=',')
    for e in rec:
        ca_path.append(tuple(e))
ca_path = ca_path[1:]

data_path = []
for d in ca_path:
    gid =  ("'%s'") %(d[0])
    sym = ("'%s'") %(d[1])
    path = ("'%s'") %(d[2])
    go = ("'%s'") %(d[3])
    #unit = (ep, d[0], d[2], d[1], d[3])
    unit = (gid, sym, path, go)
    data_path.append(unit)

def import_ca_data(data):
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    try:
        #con = mdb.connect(**dbdata);
        cur.execute("""DROP TABLE IF EXISTS `Ca_Pathways`""")
        cur.execute("""CREATE TABLE `Ca_Pathways` (
        `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
        `gene_id` VARCHAR(20) NOT NULL,
        `symbol` VARCHAR(20),
        `pathway` VARCHAR(30),
        `GO_ID` varchar(30),
        PRIMARY KEY (`id`),
        KEY `Ca_Pathways_index_gene` (`gene_id`)) ENGINE=MyISAM DEFAULT CHARSET=latin1""")

        for d in data:
            #x = ("%s %s") %(d[0], d[1])
            cur.execute("""INSERT INTO Ca_Pathways(gene_id, symbol, pathway, GO_ID)VALUES (%s, %s, %s, %s)""" %(d[0], d[1],d[2], d[3]))
            con.commit()
        #cur.execute("""LOAD DATA LOCAL INFILE "data/Rolland/ca_pathways2.txt" INTO TABLE Ca_Pathways""")

    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:

        if con:
            con.close()
import_ca_data(data_path)