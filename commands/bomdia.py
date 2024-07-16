import json
import os
import sys
import discord
import datetime
import random
from commands.user import User

USUARIOS_BOM_DIA_FILE = os.path.join('memoria', 'dados_usuarios_bom_dia.json')
COINS_FILE = os.path.join('memoria', 'coins.json')

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def ganhar_coin(id, coinMAX=10):
    try:
        _coins_data = load_data(COINS_FILE)
        id = str(id)  # Certifique-se de que o ID do usuário é uma string
        print(f'Pessoa {id}')
        # Recompensar o jogador com moedas
        moedas_ganhas = random.randint(10, coinMAX)
        print(f'moedas ganhas: {moedas_ganhas}')
        print(f'moedas atuais: {_coins_data.get(id, 0)}')
        if id in _coins_data:
            _coins_data[id] += moedas_ganhas
        else:
            _coins_data[id] = moedas_ganhas
        print(f'moedas atualizadas: {_coins_data[id]}')
        print(f'Pessoa {_coins_data}')
        save_data(COINS_FILE, _coins_data)

    except Exception as e:
        print(f"Ocorreu um erro ao salvar as moedas: {e}")

class BomDia:
    def __init__(self, client):
        self.client = client
        self.lista_de_ids = load_data(USUARIOS_BOM_DIA_FILE)

    async def processar_mensagem(self, mensagem):
        if mensagem.author == self.client.user:
            return
        if mensagem.content.lower().startswith('bom dia'):
            data_atual = str(datetime.date.today())
            usuarioId = str(mensagem.author.id)

            if usuarioId not in self.lista_de_ids:
                self.lista_de_ids[usuarioId] = {'bomDia': 0, 'boaNoite': 0, 'horario': data_atual}

            # Verificar se a data registrada é diferente da data atual
            if self.lista_de_ids[usuarioId]['horario'] == data_atual:
                self.lista_de_ids[usuarioId]['horario'] = data_atual  # Atualizar a data registrada
                save_data(USUARIOS_BOM_DIA_FILE, self.lista_de_ids)
                await mensagem.channel.send(f"Olá <@{usuarioId}>, você já deu bom dia.")

            else:
                self.lista_de_ids[usuarioId]['bomDia'] += 1
                self.lista_de_ids[usuarioId]['horario'] = data_atual  # Atualizar a data registrada
                save_data(USUARIOS_BOM_DIA_FILE, self.lista_de_ids)
                ganhar_coin(usuarioId, 10)
                await mensagem.channel.send(f"Olá <@{usuarioId}>, você já deu {self.lista_de_ids[usuarioId]['bomDia']} bom dia(s) ate hoje.")


