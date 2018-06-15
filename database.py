#webdriver imports
import unittest
import sqlite3
import filecmp

###=========================================================

class Building_Engines_Assignment(unittest.TestCase):
    ##======================================================
    ##UNITTEST Setup
    @classmethod
    def setUpClass(cls):
        #drop tables if they exist (in case of prior abend)
        c.execute('''DROP TABLE if exists offices;''')
        c.execute('''DROP TABLE if exists agents;''')
        c.execute('''DROP TABLE if exists rentals;''')

        #create tables
        c.execute('''CREATE TABLE offices(
            OID int,
            name text);
            ''')
        c.execute('''CREATE TABLE agents(
            AID int,
            last text,
            first text,
            office int);
            ''')
        c.execute('''CREATE TABLE rentals(
            RID int,
            date int,
            time int,
            address text,
            agent int,
            fee real);
            ''')

        #insert data
        c.execute('''INSERT INTO offices VALUES
            (1, "Davis"),
            (2, "Porter");
            ''')
        
        c.execute('''INSERT INTO agents VALUES
            (1, "Melios", "Mandy", 1),
            (2, "Melios", "Irving", 2),
            (3, "Puffton", "Mitchel", 1),
            (4, "Mikna", "Joeseph", 1),
            (5, "Haskel", "Leonard", 2),
            (6, "Melios", "Maura", 2),
            (7, "Redd", "Tara", 1);
            ''')

        c.execute('''INSERT INTO rentals VALUES
            (1, 20180601, 132519, "200 Highland Ave #56", 1 , 1600),
            (2, 20180604, 091029, "91 Central Ave apt 2", 3 , 750),
            (3, 20180605, 161641, "163a Albion", 5 , 2000),
            (4, 20180605, 125926, "39 Benton Rd #1", 6 , 1500),
            (5, 20180605, 104132, "9 Chester St apt11", 1 , 800),
            (6, 20180607, 100013, "68.2 Alpine", 2 , 1900),
            (7, 20180607, 151632, "220 Cedar 3", 5 , 2000),
            (8, 20180608, 093510, "24 Foskett st", 5 , 1100),
            (9, 20180609, 130156, "16 Blake apt 1", 5 , 1150),
            (10, 20180610, 164601, "9 Chester St apt G", 3 , 1750),
            (11, 20180610, 132038, "39 Benton Rd #3", 4 , 2100),
            (12, 20180610, 171143, "10A Day street", 3 , 1300),
            (13, 20180611, 121919, "18 Shea Rd", 4 , 1000),
            (14, 20180612, 105521, "85 Grafton street", 6 , 950),
            (15, 20180614, 140257, "9 Chester St #8", 3, 1075);
            ''')


    @classmethod
    def tearDownClass(cls):
        #Drop tables
        c.execute('''Drop table if exists rentals;''')
        c.execute('''Drop table if exists agents;''')
        c.execute('''Drop table if exists offices;''')

        #Close Connection
        conn.close()
        

    @classmethod
    def setUp(self): #before every test
        print('\n....................')
        
        
    @classmethod
    def tearDown(self): #after every test
        print('....................\n')

    ##======================================================
    ## Common Methods

    def verify_results(self, results, file):
        print("___results_______")
        for result in results:
            print(result)

        
        #Generate filenames based on input
        exp = file + "_exp.txt"
        act = file + "_act.txt"

        #Write results to actual output file
        f= open(act,"w+")
        for result in results:
            f.write( str(result) + "\n" )
        f.close()

        #Compare actual results file to expected
        files_equal = filecmp.cmp(exp, act)
        self.assertTrue(files_equal, "\n\n!! %s does not match %s" % (act, exp) )
        
    ##======================================================
    ##Test Cases
    def test01_basic_query(self):
        print("test01_basic_query")

        c.execute('''
            SELECT date, fee, address
            FROM rentals
            WHERE fee >= 1000 and fee < 2000
            ORDER BY date ASC, fee DESC;
        ''')

        #get rows returned and verify output                    
        rows_returned = c.fetchall()
        self.verify_results(rows_returned, "test01")


    #-------------------------------------------------------        
    def test02_inner_join(self):
        print("test02_inner_join")

        #join agents and offices
        c.execute('''
            SELECT a.last, a.first, o.name
            FROM agents AS a
            JOIN offices AS o
            ON a.office = o.OID;
        ''')

        #get rows returned and verify output                    
        rows_returned = c.fetchall()
        self.verify_results(rows_returned, "test02")

    #-------------------------------------------------------        
    @unittest.skip("Directional and Outer Joins not supported by sqlite3")
    def test03_directional_join(self):
        print("test03_directional_join")

        c.execute('''
            SELECT r.date, r.time, r.address, a.last, a.first
            FROM agents AS a
            LEFT JOIN rentals AS r
            ON a.AID = r.agent;
        ''')
        
        #get rows and verify output
        rows_returned = c.fetchall()
        self.verify_results(rows_returned, "test03")

    #-------------------------------------------------------        
    def test04_count_group_by_agent(self):
        print("test04_count_group_by_associate")

        c.execute('''
            SELECT a.last, a.first, COUNT()
            FROM rentals AS r
            JOIN agents AS a
            ON r.agent = a.AID
            GROUP BY r.agent;
            ''')

        #get rows returned and verify output                    
        rows_returned = c.fetchall()
        self.verify_results(rows_returned, "test04")


    #-------------------------------------------------------        
    def test05_sum_rental_fees_group_by_office(self):
        print("test05_sum_rental_fees_group_by_office")

        c.execute('''
            SELECT o.name, SUM(fee)
            FROM rentals AS r
            JOIN agents  AS a
            ON r.agent = a.AID
            JOIN offices AS o
            ON a.office = o.OID
            GROUP BY office;
            ''')

        rows_returned = c.fetchall()
        self.verify_results(rows_returned, "test05")


###Global variables ==========================================
conn = sqlite3.connect('melios_rentals.db')
c = conn.cursor()
        
if __name__ == '__main__':
    unittest.main()

