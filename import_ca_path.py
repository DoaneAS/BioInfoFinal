import MySQLdb as mdb
import sys

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