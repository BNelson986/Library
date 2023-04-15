from faker import Faker
import faker.providers.address.en
import random
import uszipcode

faker = Faker()

'''
    EACH CUSTOMER WILL HAVE THE FOLLOWING:
    -   NAME
    -   EMAIL
    -   ADDRESS
    -   CHECKED BOOKS
'''

def makeAddress():
    #   Address broken down into:
    #   Street Address
    #   City
    #   State
    #   Zipcode    

    streetAddress = faker.street_address()
    zip = faker.postcode()
    result = search.by_zipcode(zip)
    if result:
        city = result.city
        state = result.state_abbr
        address = {'street': streetAddress, 'city': city, 'state': state, 'zipcode': zip}
        return address
    else:
        makeAddress()    


search = uszipcode.SearchEngine()

for i in range(100000):
    first = faker.first_name()
    last = faker.last_name()

    name = f"{first} {last}"
    email = f"{first[:2]}.{last}@{faker.free_email_domain()}"

    address = makeAddress()

    customer = {'name': name, 'email': email, 'address': address}

    print(customer)