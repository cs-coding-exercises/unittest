import unittest
import sys
import requests     
import json
import filecmp

###=========================================================

class Building_Engines_Assignment(unittest.TestCase):

    ##======================================================
    ##UNITTEST Setup
    @classmethod
    def setUpClass(cls):
        print("****** Death Star Coming in!!!**************")
        # Yes, He's quoting the video game
            
    @classmethod
    def tearDownClass(cls):
        print('\n***May the Force be with you #always *******\n')
        
    @classmethod
    def setUp(self): #before every test
        print("\n----------------------")

    @classmethod
    def tearDown(self): #after every test
        print("")


    ##======================================================
    ## Common Methods
    def verify_call_response(self, call, exp_resp):
        response = requests.get(call)
        resp_code = response.status_code
        self.assertEqual(resp_code,exp_resp,
                         "!! expected %d; got %d" % (exp_resp, resp_code) )

    ##======================================================
    ##Test Cases
    #@unittest.skip("testing skipping")
    def test01_basic_call_response(self):
        print("test01_responses")

        self.verify_call_response('https://swapi.co/api/',200)
        self.verify_call_response('https://swapi.co/api/people/88/',200)
        self.verify_call_response('https://swapi.co/api/people/89/',404)
        self.verify_call_response('https://swapi.co/api/people/1000/',404)
        

    #-------------------------------------------------------        
    #@unittest.skip("testing skipping")
    def test02_simple_query(self):
        print("test02_basic_query")
        act = 'swapi_test02_act'
        exp = 'swapi_test02_exp'

        url='https://swapi.co/api/people/'
        response = requests.get(url)
        if response.status_code == 200:
            jd = json.loads(response.content.decode('utf-8'))

        print("__data___")
        print(jd)

        #verify pagination fields
        self.assertEqual(jd['previous'], None)
        self.assertEqual(jd['next'], 'https://swapi.co/api/people/?page=2')

        #Write results to act(ual)
        f = open(act,"w+")
        for j in jd['results']:
            f.write("%s|%s|%s|%s|%s|%s|%s\n" %
                 (j['name'],j['height'],j['mass'],j['hair_color'],
                  j['skin_color'], j['eye_color'],j['birth_year'])
                )
        f.close()

        #Compare act(ual) to exp(ected)
        self.assertTrue(filecmp.cmp(act, exp))
        

        
    #-------------------------------------------------------        
    #@unittest.skip("testing skipping")
    def test03_verify_number_of_records(self):
        print("test03_verify_number_of_records")
        # Verifies that the record count is accurate
        # This API paginates result.  So we iterate :)

        records = 0
        r404s = 0
        idx = 0

        url='https://swapi.co/api/people/'
        response = requests.get(url)

        if response.status_code == 200:

            #get expected number of records from API
            jd = json.loads(response.content.decode('utf-8'))
            total_people = jd['count']
            
            # iterate through records until either the 
            # either the total number of records found
            # and 20 missing records in a row
            while records < (total_people + 1) and r404s < 20:
                idx += 1
                response = requests.get('https://swapi.co/api/people/%s/' % (idx))
                print('https://swapi.co/api/people/%s/' % (idx))
                if response.status_code == 200:
                    records += 1
                    print("found: " + str(records))
                    r404s = 0
                else:
                    r404s += 1
                    print("r404s: " + str(r404s))
                    
            #Verify that:   total records n
            self.assertTrue(records == total_people and r404s == 20)

    #-------------------------------------------------------        
    @unittest.skip("testing skipping")
    def test04_basic_query(self):
        print("test04_simple_query")

        act = 'swapi_test04_act.json'
        exp = 'swapi_test04_exp.json'

        response = requests.get('https://swapi.co/api/people/1/')
        
        if response.status_code == 200:
            jd = json.loads(response.content.decode('utf-8'))
           
            print("__jd_______\n" + str(jd))

            results = [jd['name'], jd['height'], jd['mass'], jd['gender'] ]
            print(str(results))

            #with open(act, 'w+') as outfile:
            #    json.dump(jd['name'], outfile)
            #    json.dump(jd['height'], outfile)
            #    json.dump(jd['mass'], outfile)
            #    json.dump(jd['gender'], outfile)

            f = open(act,"w+")
            f.write( str(results) )
            f.close()
            
            #verify act == exp
            files_equal = filecmp.cmp(act, exp)
            print("************")
            print("files_equal: " + str(files_equal))
            self.assertTrue(files_equal, "\n\n!! %s does not match %s" % (act, exp) )
        else:
            sys.exit(print("!! Status Code not 200"))
            fail


    #-------------------------------------------------------        
    #@unittest.skip("testing skipping")
    def test_05_specific_data_query(self):
        # iterate through all characters, poulate the array with
        # all male characters who were in both Star Wars and
        # Empire Strikes Back
        print("test05_api_query")

        a_new_hope          = 'https://swapi.co/api/films/1/'
        empire_strikes_back = 'https://swapi.co/api/films/2/'

        names_exp = ['Luke Skywalker', 'Darth Vader', 'Obi-Wan Kenobi',
                     'Chewbacca', 'Han Solo', 'Wedge Antilles']
        names_act = []

        call = 'https://swapi.co/api/people/'
        response = requests.get(call)

        #get expected number of people
        if response.status_code == 200:
            jd = json.loads(response.content.decode('utf-8'))
            total_people = jd['count']
            print("total_people: " + str(total_people))

        # iterate through all people and get all male characters
        # from both Star Wars and empire
        for i in range(1,90):
            call = 'https://swapi.co/api/people/%s/' % str(i)

            response = requests.get(call)
            resp_code = response.status_code

            if response.status_code == 200:
                jd = json.loads(response.content.decode('utf-8'))

                if (jd['gender'] == 'male' and
                    a_new_hope in jd['films'] and
                    empire_strikes_back in jd['films']):
                    print(str(i), jd['name'],jd['gender'])
                    
                    names_act.append(str(jd['name']))

        self.assertNotIn('Leia Organa', names_act)  #gender != 'male'
        self.assertNotIn('Greedo', names_act)       #not in Empire
        self.assertNotIn('Bossk', names_act)        #not in New Hope

        self.assertEqual(names_act, names_exp,
                         "!! names_act does not match names_exp")

###Global variables ==========================================
if __name__ == '__main__':
    unittest.main()

