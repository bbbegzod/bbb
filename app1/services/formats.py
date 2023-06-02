from app1.models import Ishchi

def ishchi_format(data: Ishchi):
    return {
        'id': data.id,
        'ism': data.ism,
        'familiya': data.familya,
        'jins': "Erkak" if data.jins else 'Ayol',
        'birth_date': data.birth_date.__str__(),
        'lavozim': data.lavozim,
        'oylik': data.oylik,
    }