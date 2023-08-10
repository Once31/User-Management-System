import json

class Address:
    def __init__(self, address_line_1, city, state, pin):
        print('init',city)
        self.address_line_1 = address_line_1
        self.city = city
        self.state = state
        self.pin = pin
        

    def to_json(self):
        return self.__dict__
        # return json.dumps(self, default= lambda o: o.__dict__, sort_keys=True, indent=4)
    

    @staticmethod
    def from_json(json_dict):
        print('from_json',json_dict['city'])
        return Address(
            json_dict['address_line_1'],
            json_dict['city'],
            json_dict['state'],
            json_dict['pin']
        )