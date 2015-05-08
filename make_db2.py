network_file = "PPs/HI-II-14.tsv"

with open(network_file) as f:
    header = f.readline()
    netw = [(l.strip().split('\t')) for l in f]

with open(network_file) as f:
    header = f.readline()
    netw = [(l.strip().split('\t')) for l in f]
netw

ppi_key = set()
for p in netw:
    entrezA = p[0]
    entrezB = p[2]
    geneA = p[1]
    geneB = p[3]
    ppi_key.add(tuple(sorted([p[0], p[2]])))
ppi_key

#ppi_rec = [[[i for i in p], [i for i in p][0], [i for i in p][1]] for p in ppi_key]
ppi_rec=[(i, i[0], i[1]) for i in ppi_key]

ppi_tab = [i for i in ppi_key]
len(ppi_tab)



##individual gene lookup
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


import MySQLdb as mdb
import sys

def connect():
    try:
        #con = mdb.connect(**dbdata);
        con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
        cur = con.cursor()
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


try:
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')

    cur = con.cursor()
    #cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    #cur.execute("DROP TABLE IF EXISTS genes")
    cur = con.cursor()
    #cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    #cur.execute("DROP TABLE IF EXISTS `genes`")
    cur.execute("CREATE TABLE `genes` ("
        "  `geneid` varchar(30) DEFAULT NULL,"
        "  `entrezid` varchar(30) NOT NULL DEFAULT '',"
        "  PRIMARY KEY (`entrezid`))")


    #cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    #cur.execute("DROP TABLE IF EXISTS ppi")

    cur.execute("CREATE TABLE ppi ("
    "  `entrezA` varchar(30) NOT NULL DEFAULT '',"
    "  `entrezB` varchar(30) NOT NULL DEFAULT '',"
    "  PRIMARY KEY (`entrezA`,`entrezB`),"
    "  KEY `pindex` (`entrezA`,`entrezB`) USING BTREE,"
    "  KEY `entrezB` (`entrezB`),"
    "  FOREIGN KEY (`entrezA`) REFERENCES `genes` (`entrezid`),"
    "  FOREIGN KEY (`entrezB`) REFERENCES `genes` (`entrezid`))")


except mdb.Error, e:

    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)


finally:

    if con:
        con.close()


query = "INSERT INTO genes(entrezid,geneid) " \
        "VALUES(%s,%s)"

try:
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')

    cur = con.cursor()
    cur.executemany(query, genes)

except mdb.Error, e:

    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)


finally:

    if con:
        con.close()