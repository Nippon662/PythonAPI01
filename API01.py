import json

items = [
    {
        'id': 1,
        'name': 'Bagulho',
        'description': 'Apenas um bagulho',
        'location': 'Em uma caixa'
        
    },
    {
        'id': 2,
        'name': 'Traqueira',
        'description': 'Apenas uma tranqueira qualquer',
        'location': 'Em um gaveteiro'
    },
    {
        'id': 3,
        'name': 'Katana',
        'description': 'Uma arma cortante',
        'location': 'Pendurada na parede'
    }
]

def get_all():
    return json.dumps(items, indent=2)

#print(get_all())

def get_one(id):
    return json.dumps(items[id], indent=2)
    

print(get_one(2))