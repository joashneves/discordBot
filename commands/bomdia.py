import json
import os
import sys
import discord
import datetime

from commands.user import User

class BomDia():
    global lista_de_ids
    try:
        caminho_bom_dia = os.path.join('memoria', 'dados_usuarios.json')
        with open(caminho_bom_dia, 'r') as file:
            try:
                lista_de_ids = json.load(file)
            except json.JSONDecodeError:
                lista_de_ids = {}  # Cria um dicionário vazio se o JSON não for válido
    except Exception as ex:
        sys.stderr.write(f'não foi possivel carregar dados: {ex}')

    def __init__(self, client):
        self.client = client

    async def processar_mensagem(self, mensagem):
        if mensagem.author == self.client.user:
            return
        if mensagem.content.lower().startswith('bom dia'):  # Se a pessoa escrever bom dia
            # Pega o ID do usuario
            usuarioId = str(mensagem.author.id)
            if usuarioId not in lista_de_ids:
                lista_de_ids[usuarioId] = User(user_id=usuarioId, bomDia=0, boaNoite=0, mensagens=0, comandos=0, capturados=0, xp=0, level=0)
                # Adicione o ID à lista
                lista_de_ids[usuarioId].bomDia
            else:
                lista_de_ids[usuarioId].bomDia += 1
            print(lista_de_ids[usuarioId].bomDia)
            # Obter a data atual
            data_atual = str(datetime.date.today())

            # se a id do usuario não estiver em Usuario ou tiver e tiver com
            await mensagem.channel.send(f"Olá <@{usuarioId}>, você já deu {lista_de_ids[usuarioId].bomDia} bom dia(s).")
