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

class SubscriptionRule:
    
    def __init__(self, _kv, _operator):
        self.kv = _kv
        self.operator = _operator
        
    def __str__(self):
        if self.kv.type == 'date':
            return f'({self.kv.name}, {self.operator}, {datetime.datetime.strftime(self.kv.value, "%d.%m.%Y")})'
        elif self.kv.type == 'string':
            return f'({self.kv.name}, {self.operator}, "{self.kv.value}")'
        elif self.kv.type == 'double':
            return f'({self.kv.name}, {self.operator}, {self.kv.value:.2f})'
        return f'({self.kv.name}, {self.operator}, {self.kv.value})'

    def evaluate(self, against):
        pass

class Subscription:

    def __init__(self):
        self.rules = []

    def __str__(self):
        return  '{' + ';'.join(str(x) for x in self.rules) + '}'
        
    def add_rule(self, rule):
        self.rules.append(rule)

class SubscriptionGenerator:

    def __init__(self, config):
        self.number_of_subscriptions = config['number_of_subscriptions']
        self.keys = [k for k in config_dict['keys']]

    def generate_subscriptions(self):

        subscriptions_left = self.number_of_subscriptions

        key_data = {}

        for key in self.keys:
            data = {}

            rules = config_dict['keys'][key]['subscription_rules']

            data['percentage'] = rules['key_percentage']
            
            if data['percentage'] == 0:
                data['remaining'] = -1
                data['subtract'] = 0
            else:
                data['remaining'] = subscriptions_left
                data['subtract'] = subscriptions_left/data['percentage']

            operators = {}
            op_total_percentage = 0

            for op in rules['operator_percentages']:
                op_data = {'percentage': rules['operator_percentages'][op]}
                
                if op_data['percentage'] == 0:
                    op_data['remaining'] = -1
                    op_data['subtract'] = 0
                else:
                    op_data['remaining'] = subscriptions_left
                    op_data['subtract'] = subscriptions_left/data['percentage']
                operators[op] = op_data

                op_total_percentage += op_data['percentage']

            if op_total_percentage < 100:
                op_data = {
                    'percentage': 100 - op_total_percentage,
                    'remaining': subscriptions_left,
                    'subtract': subscriptions_left/(100 - op_total_percentage)
                }
                operators['?'] = op_data
            
            data['operators'] = operators
            key_data[key] = data

        subscriptions = []

        while subscriptions_left > 0:
            
            sub = Subscription()
            keys = []

            for k in key_data:

                kd = key_data[k]

                if kd['remaining'] >= subscriptions_left:
                    keys.append(k)
                    kd['remaining'] -= kd['subtract']

            for k in keys:

                kd = key_data[k]
                op_data = kd['operators']

                max_remaining = -1
                chosen_op = '?'

                for op in op_data:
                    if op_data[op]['remaining'] > max_remaining:
                        max_remaining = op_data[op]['remaining']
                        chosen_op = op
            
                op_data[chosen_op]['remaining'] -= op_data[chosen_op]['subtract']

                if chosen_op == '?':
                    key_type = config_dict['keys'][k]['type']
                    chosen_op = random.choice(config_dict['types'][key_type]['operators'])

                kv = KVPairGenerator(k, config_dict['keys'][k]).generate_pair()
                sub_rule = SubscriptionRule(kv, chosen_op)
                sub.add_rule(sub_rule)

            subscriptions.append(sub)
            subscriptions_left -= 1
        
        return subscriptions


if __name__ == '__main__':

    # pg = PublicationGenerator(config_dict['publication_generation'])

    # for p in pg.generate_all():
    #     print(p)

    sg = SubscriptionGenerator(config_dict['subscription_generation'])

    for s in sg.generate_subscriptions():
        print(s)