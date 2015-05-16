import MySQLdb as mdb
import sys

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




    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:

        if con:
            con.close()
make_pub()