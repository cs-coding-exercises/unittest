import unittest

#webdriver imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

###=========================================================

class cars_com_make_dropdown_test(unittest.TestCase):
    ##======================================================
    ##UNITTEST Setup
    @classmethod
    def setUpClass(cls):
        print("******Running cars.com Tests #dropdown list**************")
        driver.get('https://www.cars.com/')
        #move out if starting points diversify
            
    @classmethod
    def tearDownClass(cls):
        #close browser
        driver.quit()

    @classmethod
    def setUp(self): #before every test
        print("\n")
        
    @classmethod
    def tearDown(self): #after every test
        print('....................\n')

    ##======================================================
    ## Common Method

    def get_makes(self, stock_type):
        #select stock_type (new, used, etc. ) from Dropdown
        stocktype_dd = Select( driver.find_element_by_name("stockType") )
        stocktype_dd.select_by_visible_text(stock_type)    

        #get items from make field ('All Makes', 'Acura' ... 'Volvo','Yugo')
        make_dd = Select( driver.find_element_by_name("makeId") )
        makes = [m.text for m in make_dd.options]

        return makes

    ##======================================================
    ##Test Cases
    def test01_new_and_used(self):
        print("test01_new_and_used")
        
        #Makes should include all new and used
        makes_exp = ['All Makes', 'Acura', 'Alfa Romeo', 'Am General',
                     'Aston Martin', 'Audi', 'Avanti Motors', 'Bentley',
                     'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet',
                     'Chrysler', 'Daewoo', 'Daihatsu', 'Dodge', 'Eagle',
                     'Ferrari', 'FIAT', 'Fisker', 'Ford', 'Genesis',
                     'Geo', 'GMC', 'Honda', 'Hummer', 'Hyundai',
                     'INFINITI', 'International', 'Isuzu', 'Jaguar',
                     'Jeep', 'Karma', 'Kia', 'Koenigsegg', 'Lamborghini',
                     'Land Rover', 'Lexus', 'Lincoln', 'Lotus', 'Maserati',
                     'Maybach', 'Mazda', 'McLaren', 'Mercedes-Benz', 'Mercury',
                     'MINI', 'Mitsubishi', 'Morgan', 'Nissan', 'Oldsmobile',
                     'Panoz', 'Peugeot', 'Plymouth', 'Pontiac', 'Porsche',
                     'Qvale', 'RAM', 'Rolls-Royce', 'Saab', 'Saleen', 'Saturn',
                     'Scion', 'smart', 'Spyker', 'Sterling', 'Subaru', 'Suzuki',
                     'Tesla', 'Toyota', 'Volkswagen', 'Volvo', 'Yugo']

        makes_act = self.get_makes("New & Used Cars")
        
        self.assertListEqual( makes_exp, makes_act)


    #-------------------------------------------------------        
    def test02_new(self):
        print("test02_new")

        #should only include makes currently in production
        #should exclude: Oldsmobile, Pontiac, Scion, Yugo, etc.
        makes_exp = ['All Makes', 'Acura', 'Alfa Romeo', 'Aston Martin',
                    'Audi', 'Bentley', 'BMW', 'Buick', 'Cadillac',
                    'Chevrolet', 'Chrysler', 'Dodge', 'Ferrari', 'FIAT',
                    'Ford', 'Genesis', 'GMC', 'Honda', 'Hyundai',
                    'INFINITI', 'Jaguar', 'Jeep', 'Karma', 'Kia',
                    'Lamborghini', 'Land Rover', 'Lexus', 'Lincoln',
                    'Lotus', 'Maserati', 'Mazda', 'McLaren',
                    'Mercedes-Benz', 'MINI', 'Mitsubishi', 'Nissan',
                    'Porsche', 'RAM', 'Rolls-Royce', 'smart', 'Subaru',
                    'Toyota', 'Volkswagen', 'Volvo']

        makes_act = self.get_makes("New Cars")

        self.assertListEqual( makes_exp, makes_act)


    #-------------------------------------------------------        
    def test03_used(self):
        print("test03_used")

        #should include makes that have used cars for sale
        #should include: Oldsmobile, Mercury, Scion, Yugo, etc.
        makes_exp = ['All Makes', 'Acura', 'Alfa Romeo', 'Am General',
                     'Aston Martin', 'Audi', 'Avanti Motors', 'Bentley',
                     'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet',
                     'Chrysler', 'Daewoo', 'Daihatsu', 'Dodge', 'Eagle',
                     'Ferrari', 'FIAT', 'Fisker', 'Ford', 'Genesis',
                     'Geo', 'GMC', 'Honda', 'Hummer', 'Hyundai',
                     'INFINITI', 'International', 'Isuzu', 'Jaguar',
                     'Jeep', 'Karma', 'Kia', 'Koenigsegg', 'Lamborghini',
                     'Land Rover', 'Lexus', 'Lincoln', 'Lotus', 'Maserati',
                     'Maybach', 'Mazda', 'McLaren', 'Mercedes-Benz','Mercury',
                     'MINI', 'Mitsubishi', 'Morgan', 'Nissan', 'Oldsmobile',
                     'Panoz', 'Peugeot', 'Plymouth', 'Pontiac', 'Porsche',
                     'Qvale', 'RAM', 'Rolls-Royce', 'Saab', 'Saleen', 'Saturn',
                     'Scion', 'smart', 'Spyker', 'Sterling', 'Subaru', 'Suzuki',
                     'Tesla', 'Toyota', 'Volkswagen', 'Volvo', 'Yugo']
        
        makes_act = self.get_makes("Used Cars")

        self.assertListEqual( makes_exp, makes_act)

###Global variables ==========================================
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 30)
driver.implicitly_wait(20)

if __name__ == '__main__':
    unittest.main()


''' Issue: =========================================

TITLE:
Karma does not appear in the used cars make list.

DESCRIPTION:
When user selects "used" from the stock type dropdown list,
Karma does not appear.  When user selects "New and Used",
both new and used Karma Revero's appear in search results.

STEPS TO REPRODUCE:
- Navigate to Home Page
- Select "New & Used Cars" from stock type dropdown
- Select Karma and click Search button
(both new and used car should appear in results)
- Navigate back to Home Page
- Select "Used Cars"

EXPECTED RESULTS:
The Make dropdown list should include Karma on the items

ACTUAL RESULTS:
Karma does not appear on the Make dropdown list

COMMENTS:
URL for used car
https://www.cars.com/for-sale/searchresults.action/?mkId=36365359&rd=99999&searchSource=QUICK_FORM&zc=02420

error text:
    self.assertListEqual( makes_exp, makes_act)
AssertionError: Lists differ: ['All[347 chars]', 'Karma', 'Kia', 'Koenigsegg', 'Lamborghini'[389 chars]ugo'] != ['All[347 chars]', 'Kia', 'Koenigsegg', 'Lamborghini', 'Land R[380 chars]ugo']

First differing element 33:
'Karma'
'Kia'
'''
