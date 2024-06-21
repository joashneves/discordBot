import discord
from discord.ext import commands
import json
import os
import sys

# Intents and client setup
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='$', intents=intents)

# Path to store data
DATA_FILE = os.path.join('memoria', 'game.json')
IMAGEM = os.path.join('memoria', 'game.json')

class AdicionarPersonagem():

    def __init__(self, client):
        self.client = client
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)

    async def processar_mensagem(self, mensagem):
        if mensagem.author == self.client.user:
            return

        try:
            if mensagem.content.startswith("$add"):
                if mensagem.attachments:
                    attachment = mensagem.attachments[0]
                    nome = mensagem.content.split("$add ", 1)[1]
                    if attachment.url:
                        self.data.append({"nome": nome, "imagem": attachment.url})
                        self.save_data()
                        await mensagem.channel.send(f'Nome "{nome}" e imagem adicionados com sucesso!')
                    else:
                        await mensagem.channel.send('Por favor, envie uma imagem válida (jpg, jpeg, png, gif).')
                else:
                    await mensagem.channel.send('Por favor, anexe uma imagem ao comando.')
        except Exception as ex:
            sys.stderr.write(f'Ocorreu um erro com comando $add: {ex}')




