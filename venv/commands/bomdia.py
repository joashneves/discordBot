import json
import os
import discord
import datetime

from commands.user import User

class BomDia():
    global lista_de_ids_bom_dia

    def __init__(self, client):
        self.client = client

    with open('json/bom_dia.json', 'r') as file:
        try:
            lista_de_ids_bom_dia = json.load(file)
        except json.JSONDecodeError:
            lista_de_ids_bom_dia = {}  # Cria um dicionário vazio se o JSON não for válido

    def salvador_dados(self):
        with open('json/bom_dia.json', 'w') as file:
            json.dump(lista_de_ids_bom_dia,file)

    async def processar_mensagem(self, mensagem):
        if mensagem.author == self.client.user:
            return

        if mensagem.content.lower().startswith('bom dia'):  # Se a pessoa escrever bom dia
            # Pega o ID do usuario
            usuarioId = str(mensagem.author.id)
            #Obter a data atual
            data_atual = str(datetime.date.today())
            if usuarioId not in lista_de_ids_bom_dia or lista_de_ids_bom_dia[usuarioId] != data_atual :
                usuario = User(user_id=usuarioId, bomDia=0, boaNoite=0, mensagens=0, comandos=0, capturados=0, xp=0, level=0)
                lista_de_ids_bom_dia[usuarioId] = data_atual
                # Adicione o ID à lista
                self.salvador_dados()
                await mensagem.channel.send(f"Olá <@{usuarioId}>, bom dia.")
            elif lista_de_ids_bom_dia[usuarioId] != data_atual:
                lista_de_ids_bom_dia[usuarioId] = data_atual
                self.salvador_dados()
                # se a id do usuario não estiver em Usuario ou tiver e tiver com
                await mensagem.channel.send(f"Olá <@{usuarioId}>, bom dia.")
            else:
                await mensagem.channel.send(f"Olá <@{usuarioId}>, você já deu bom dia hoje.")