# %load make_ltdb.py
#!/usr/bin/python


#adapt for lit-bm13
import MySQLdb as mdb
import sys
network_file = "data/Lit-BM-13.tsv"



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

efile = "data/entrez_human2longest_uniprot.txt"
with open(efile) as f:
    e2u = [l.strip().split('\t') for l in f]


uniD = {}
for r in e2u:
    uniD[r[0]] = r[1]
uniD

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
    uniA = uniD.get(d[0])
    uniB = uniD.get(d[2])
    ua = ("'%s'") %(uniA)
    ub = ("'%s'") %(uniB)
    #unit = (ep, d[0], d[2], d[1], d[3])
    unit = (ep, d[0], d[2], ga, gb, ua, ub)
    data_pairs.append(unit)

def connect():
    con = mdb.connect('127.0.0.1', 'asd223', '5NKEAP', 'ASD223_db')
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

#make master ppi table and insert data
def make_master_ppi(data):
    con = mdb.connect('127.0.0.1', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    try:
        #con = mdb.connect(**dbdata);


        cur.execute("""DROP TABLE IF EXISTS MASTER_P""")
        cur.execute("""CREATE TABLE MASTER_P (`primary_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
            entrezPair VARCHAR(20) NOT NULL,
            entrezA VARCHAR(10), entrezB VARCHAR(10), symbolA VARCHAR(20),
            symbolB VARCHAR(20), uniprotA VARCHAR(20), uniprotB VARCHAR(20),
            PPDB VARCHAR(10),
            PRIMARY KEY (`primary_id`),
            KEY `MAP_index_entrezPair` (`entrezPair`),
            KEY `MAP_index_entrezA` (`entrezA`),
            KEY `MAP_index_entrezB` (`entrezB`),
            KEY `MAP_index_symbolA` (`symbolA`),
            KEY `MAP_index_PPDB` (`PPDB`),
            KEY `MAP_index_symbolB` (`symbolB`)) ENGINE=MyISAM DEFAULT CHARSET=latin1""")



        for d in data:
            #x = ("%s %s") %(d[0], d[1])
            cur.execute("""INSERT INTO MASTER_P(entrezPair, entrezA, entrezB, symbolA, symbolB, uniprotA, uniprotB) VALUES (%s, %s, %s, %s, %s, %s, %s)""" %(d[0], d[1],d[2], d[3], d[4], d[5], d[6]))
            con.commit()



    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:

        if con:
            con.close()
make_master_ppi(data_pairs)
#make_table(prs)
#make_table3(data_pairs)

