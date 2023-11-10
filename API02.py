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
    },
    {
        'id': 4,
        'name': 'Quadro',
        'descriptions': 'Uma pintura ou foto',
        'location': 'Parede'
    },
    {
        'id': 5,
        'name': 'Camera',
        'descriptions': 'Usado para tirar fotos',
        'location': 'Guardado pela casa'
    },
    {
        'id': 6,
        'name': 'Isqueiro',
        'descriptions': 'Faz uma chama',
        'location': 'Dentro do bolso'
    },
    {
        'id': 7,
        'name': 'Celular',
        'descriptions': 'Um aparelho eletronico',
        'location': 'Dentro do bolso, ou na mesa'
    },
    {
        'id': 8,
        'name': 'Video-game',
        'descriptions': 'Use para executar jogos',
        'location': 'Chao'
    }
]


def get_one(id):
    try:
        id = int(id)
        for item in items:
            if item.get('id') == id:
                return json.dumps(item, indent=2)
    except:
        return False
    

def get_data():
    input_id = input('Digite o id do item: ')

    view = get_one(input_id)

    if view:
        print(view)
    else:
        print('Algo de errado não deu certo!')
    

def get_all():
    return json.dumps(items, indent=2)

#print(get_all())

#get_data()

my_json ='''
{
        "name": "Blusa",
        "descriptions": "Uma peça de roupa",
        "location": "Guarda-Roupas"
}
'''
def new(json_data):
    #print(json_data)
    max_id = max(item["id"] for item in items)
    print('max →', max_id + 1)
    return

new(my_json)