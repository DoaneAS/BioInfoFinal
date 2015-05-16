import MySQLdb as mdb
import sys


def import_data():
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

        cur.execute("""LOAD DATA LOCAL INFILE "data/sql/gene2pubmed" INTO TABLE gene2pubmed""")

    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:

        if con:
            con.close()
import_data()