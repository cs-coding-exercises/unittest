import unittest
import requests     
import json
import filecmp

###=========================================================
### Updates since 6/15:
# -separated response tests into response types (200 & 404)
# -updated basic query to include pagination
# (will update test04 to use the same mechanism for gathering info)

class API_tests(unittest.TestCase):

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
    def test01a_basic_call_response_200(self):
        print("test01_responses_200s")
        self.verify_call_response('https://swapi.co/api/',200)
        self.verify_call_response('https://swapi.co/api/people/88/',200)

    def test01b_basic_call_response_404(self):
        print("test01b_responses_404s")
        self.verify_call_response('https://swapi.co/api/people/89/',404)
        

    #-------------------------------------------------------        
    def test02_simple_query(self):
    #iterates through all pages and gets character info
        print("test02_basic_query")
        act = 'swapi_test02_act'
        exp = 'swapi_test02_exp'
        next_page='https://swapi.co/api/people/'

        #access swapi
        response = requests.get(next_page)

        #if proper response, open file for comparison
        if response.status_code == 200:
            file = open(act,"w+")

            # iterate through pages, get data until there is
            # a null value for the next page
            while next_page != None:
                response = requests.get(next_page)
                print("====next_page: " + next_page)
                json_data = json.loads(response.content.decode('utf-8'))

                ### get page data and write to file
                for jd in json_data['results']:
                    file.write("%s|%s|%s|%s|%s|%s|%s\n" %
                    (jd['name'],jd['height'],jd['mass'],jd['hair_color'],
                     jd['skin_color'], jd['eye_color'],jd['birth_year'])
                    )
                    
                    #print("%s|%s|%s|%s|%s|%s|%s\n" %
                    (jd['name'],jd['height'],jd['mass'],jd['hair_color'],
                     jd['skin_color'], jd['eye_color'],jd['birth_year'])
                    )

                # get value of next page
                next_page = json_data['next']
                
            file.close()              

        #Compare act(ual) to exp(ected)
        self.assertTrue(filecmp.cmp(act, exp))
        
    #-------------------------------------------------------        
    def test03_verify_number_of_records(self):
        print("test03_verify_number_of_records")
        # Verifies that the record count is accurate
        # This API paginates results.  So we iterate :)

        url='https://swapi.co/api/people/'
        response = requests.get(url)
        if response.status_code == 200:

            #get expected number of records from API (87 in this case)
            jd = json.loads(response.content.decode('utf-8'))
            total_people_exp = jd['count']
            
            # iterate through records until either the 
            # total number of records found exceeds expected
            # or there are 20 missing records in a row
            records_found = 0
            r404s   = 0
            idx     = 0

            while records_found < (total_people_exp + 1) and r404s < 20:
                idx += 1
                response = requests.get('https://swapi.co/api/people/%s/' % (idx))
                print('https://swapi.co/api/people/%s/' % (idx))
                if response.status_code == 200:
                    print("found: " + str(records_found))
                    records_found += 1
                    r404s = 0
                else:
                    r404s += 1
                    print("r404s: " + str(r404s))
                    
            #verify records_found = expected
            self.assertEqual(records_found, total_people_exp)

    #-------------------------------------------------------        
    def test_04_specific_data_query(self):
        print("test04_specific_data_query")
        # iterate through all SW characters, populate the array with
        # all male characters who were in both Star Wars and
        # Empire Strikes Back

        a_new_hope          = 'https://swapi.co/api/films/1/'
        empire_strikes_back = 'https://swapi.co/api/films/2/'

        names_exp = ['Luke Skywalker', 'Darth Vader', 'Obi-Wan Kenobi',
                     'Chewbacca', 'Han Solo', 'Wedge Antilles']
        names_act = []


        # iterate through all people and get all male characters
        # from both Star Wars and empire
        for i in range(1,89):
            call = 'https://swapi.co/api/people/%s/' % str(i)

            response = requests.get(call)
            resp_code = response.status_code

            if response.status_code == 200:
                jd = json.loads(response.content.decode('utf-8'))

                if (jd['gender'] == 'male' and
                    a_new_hope in jd['films'] and
                    empire_strikes_back in jd['films']):
                    #print(str(i), jd['name'],jd['gender'])
                    
                    names_act.append(str(jd['name']))

        self.assertNotIn('Leia Organa', names_act)  #gender != 'male'
        self.assertNotIn('Greedo', names_act)       #not in Empire
        self.assertNotIn('Bossk', names_act)        #not in New Hope

        self.assertListEqual(names_act, names_exp,
                         "!! names_act does not match names_exp")

###Global variables ==========================================
if __name__ == '__main__':
    unittest.main()

