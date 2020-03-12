import time
import json
import random
import datetime

config_dict = json.loads(open("config.json").read())

class KVPair:

    def __init__(self, _name, _value, _type='default'):
        self.name = _name
        self.value = _value
        self.type = _type

    def __str__(self):
        if self.type == 'date':
            return f'({self.name}, {datetime.datetime.strftime(self.value, "%d.%m.%Y")})'
        elif self.type == 'string':
            return f'({self.name}, "{self.value}")'
        elif self.type == 'double':

            return f'({self.name}, {self.value:.2f})'
        return f'({self.name}, {self.value})'

    def load(self):
        return

    def evaluate_rule(self):
        return

class KVPairGenerator:

    def __init__(self, name, config):
        self.name = name
        self.type = config['type']
        self.possible_values = []
        self.rules = None
        self.possible_values = None

        if 'rules' in config:
            self.rules = config['rules']
            if 'possible_values' in self.rules:
                self.possible_values = self.rules['possible_values']
        
    def generate_pair(self):
        value = None
        if self.possible_values:
            value = random.choice(self.possible_values)
        elif self.rules:
            if self.type == 'double':
                min_val = float(self.rules["min"])
                max_val = float(self.rules["max"])
                prec = self.rules["precision"]
                value = random.randrange(min_val * (10**prec), max_val* (10**prec)) / (10**prec)
            if self.type == 'date':
                start_time = datetime.datetime.strptime(self.rules["start_date"], self.rules["start_format"])
                end_time = datetime.datetime.strptime(self.rules["end_date"], self.rules["end_format"])

                delta = end_time - start_time
                
                value = start_time + datetime.timedelta(days=random.randrange(delta.days))
        
        return KVPair(self.name, value, self.type)

class Publication:

    def __init__(self):
        self.pairs = []

    def __str__(self):
        return  '{' + ';'.join(str(x) for x in self.pairs) + '}'
        
    def add_pair(self, pair):
        self.pairs.append(pair)

class PublicationGenerator:

    def __init__(self, config):
        self.number_of_publications = config['number_of_publications']
        self.keys = [k for k in config_dict['keys']]

    def generate_publication(self):

        pub = Publication()

        for key_name in config_dict['keys']:
            key_config = config_dict['keys'][key_name]

            pair = KVPairGenerator(key_name, key_config).generate_pair()
            pub.add_pair(pair)

        return pub

    def generate_all(self):

        publication_list = []

        for i in range(self.number_of_publications):
            publication_list.append(self.generate_publication())

        return publication_list


if __name__ == '__main__':

    pg = PublicationGenerator(config_dict['publication_generation'])

    for p in pg.generate_all():
        print(p)