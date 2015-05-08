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

def make_table(data):
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    try:
        #con = mdb.connect(**dbdata);
        cur.execute("""DROP TABLE IF EXISTS PPI""")
        cur.execute("""CREATE TABLE PPI (EP CHAR(30), EA CHAR(20), EB CHAR(20))""")




        # Insert new employee
        #cursor.execute(add_entry, d)


        for d in data:
            #cur.execute("""INSERT INTO PPI VALUES (%s,%s)""" %(d[0],d[1]))
            cur.execute("""INSERT INTO PPI VALUES (%s, %s, %s)""" %(d[0], d[1],d[2]))
            con.commit()



    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:

        if con:
            con.close()

def make_table3(data):
    con = mdb.connect('localhost', 'asd223', '5NKEAP', 'ASD223_db')
    cur = con.cursor()
    try:
        #con = mdb.connect(**dbdata);
        cur.execute("""DROP TABLE IF EXISTS PPI""")
        cur.execute("""CREATE TABLE PPI (EP VARCHAR(20) PRIMARY KEY NOT NULL, EA VARCHAR(10), EB VARCHAR(10), GA VARCHAR(20), GB VARCHAR(20))""")





        #cur.execute("""INSERT INTO PPI VALUES (%s,%s)""",('188','90'))
        # Insert new employee
        #cursor.execute(add_entry, d)


        for d in data:
            #x = ("%s %s") %(d[0], d[1])
            cur.execute("""INSERT INTO PPI VALUES (%s, %s, %s, %s, %s)""" %(d[0], d[1],d[2], d[3], d[4]))
            con.commit()



    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)

    finally:

        if con:
            con.close()

connect()

#make_table(prs)
make_table3(data_pairs)


#make_table(prs)