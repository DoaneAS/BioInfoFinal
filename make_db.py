from __future__ import print_function
import mysql.connector
from mysql.connector import MySQLConnection, Error, errorcode


network_file = "CervBinaryHQ_HT.txt"
cols = ['ORF_A', 'ORF_B', 'Gene_A', 'Gene_B', 'Pubmedid,EvidenceCode,HT']
with open(network_file) as f:
    header = f.readline()
    netw = [(l.strip().split('\t')) for l in f]

network = {}


for p in netw:
    orfPair = (p[0], p[1])
    genePair = (p[2], p[3])
    if len(p) == 4:
        ann = None
    else:
        ann = p[4:]

    if orfPair not in network:
        network[orfPair] = {'genePair': genePair,
                            'ann': ann
                            #'pmid' : ann[0],
                            #'psi-mi': ann[1],
                            #'HT': ann[2]
                           }


##individual gene lookup
orf_key = set()
for p in netw:
    orfA = p[0]
    orfB = p[1]
    geneA = p[2]
    geneB = p[3]
    A = (orfA, geneA)
    B = (orfB, geneB)
    orf_key.add(A)
    orf_key.add(B)



orfs = [i for i in orf_key]

ppi_key = set()
for p in netw:
    orfA = p[0]
    orfB = p[1]
    geneA = p[2]
    geneB = p[3]
    ppi_key.add(tuple(sorted([p[0], p[1]])))
ppi_key

#ppi_rec = [[[i for i in p], [i for i in p][0], [i for i in p][1]] for p in ppi_key]
ppi_rec=[(i, i[0], i[1]) for i in ppi_key]

ppi_tab = [i for i in ppi_key]

db_conf = {'host': 'localhost',
           'database' : 'adtest',
           'user' : 'ashleysdoane',
           'password' : '6194'
           }

from mysql.connector import errorcode

DB_NAME = 'adtest'

TABLES = {}

TABLES['ppi'] = (
    "CREATE TABLE `ppi` ("
    "  `orfA` varchar(30) NOT NULL DEFAULT '',"
    "  `orfB` varchar(30) NOT NULL DEFAULT '',"
    "  PRIMARY KEY (`orfA`,`orfB`),"
    "  KEY `pindex` (`orfA`,`orfB`) USING BTREE,"
    "  KEY `orfB` (`orfB`),"
    "  FOREIGN KEY (`orfA`) REFERENCES `genes` (`orfid`),"
    "  FOREIGN KEY (`orfB`) REFERENCES `genes` (`orfid`)"
    ") ENGINE=InnoDB")

TABLES1 = {}
TABLES1['genes'] = (
    "CREATE TABLE `genes` ("
    "  `geneid` varchar(30) DEFAULT NULL,"
    "  `orfid` varchar(30) NOT NULL DEFAULT '',"
    "  PRIMARY KEY (`orfid`)"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        conn = MySQLConnection(**db_data)
        cursor = conn.cursor()
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def create_table(tables, db_data):
    try:
        dbconfig = db_data
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        for name, ddl in tables.iteritems():
            cursor.execute(ddl)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

create_table(TABLES1, db_conf)
create_table(TABLES, db_conf)

from mysql.connector import MySQLConnection, Error
def connect(db_data):
    """ Connect to MySQL database """

    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_data)

        if conn.is_connected():
            print('connection established.')
        else:
            print('connection failed.')

    except Error as error:
        print(error)

    finally:
        conn.close()
        print('Connection closed.')


def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def query_with_fetchmany(db_data):
    try:
        dbconfig = db_data
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM CervBin")

        for row in iter_row(cursor, 10):
            print(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

def insert_genes(genes, db_data):
    query = "INSERT INTO genes(orfid,geneid) " \
            "VALUES(%s,%s)"
    try:
        conn = MySQLConnection(**db_data)

        cursor = conn.cursor()
        cursor.executemany(query, genes)

        conn.commit()
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()


def insert_ppi(ppis, db_data):
    query = "INSERT INTO ppi(orfA,orfB) " \
            "VALUES(%s,%s)"
    try:
        conn = MySQLConnection(**db_data)

        cursor = conn.cursor()
        cursor.executemany(query, ppis)

        conn.commit()
    except Error as e:
        print('Error:', e)

    finally:
        cursor.close()
        conn.close()

##below works- do not rerun or will make dups?
insert_genes(orfs, db_conf)

connect(db_conf)

insert_ppi(ppi_tab, db_conf)
