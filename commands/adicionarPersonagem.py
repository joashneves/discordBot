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

# ID do servidor onde o comando é permitido
ALLOWED_GUILD_ID = 1252065347016593488
TIME_LORD_CARGO_ID = 1252077541460672613

class AdicionarPersonagem:

    def __init__(self, client):
        self.client = client
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)

    async def processar_mensagem(self, mensagem):
        if mensagem.author == self.client.user:
            return
        if mensagem.content.startswith("$add"):
            try:
                # Verificar se a mensagem é do servidor permitido
                if mensagem.guild and mensagem.guild.id == ALLOWED_GUILD_ID:
                    # Verificar se o usuário tem o cargo TIME_LORD_CARGO_ID
                    if any(role.id == TIME_LORD_CARGO_ID for role in mensagem.author.roles):
                        if mensagem.attachments:
                            attachment = mensagem.attachments[0]
                            nome = mensagem.content.split("$add ", 1)[1].strip()
                            # Verificar se o nome do personagem já existe
                            if any(personagem['nome'] == nome for personagem in self.data):
                                await mensagem.channel.send(f'Um personagem com o nome "{nome}" já existe.')
                            else:
                                if attachment.url:
                                    self.data.append({"nome": nome, "imagem": attachment.url})
                                    self.save_data()
                                    await mensagem.channel.send(f'Nome "{nome}" e imagem adicionados com sucesso!')
                                else:
                                    await mensagem.channel.send('Por favor, envie uma imagem válida (jpg, jpeg, png, gif).')
                        else:
                            await mensagem.channel.send('Por favor, anexe uma imagem ao comando.')
                    else:
                        await mensagem.channel.send('Você não tem permissão para usar este comando.')
                else:
                    await mensagem.channel.send('Este comando só pode ser usado no servidor permitido.')
            except Exception as ex:
                sys.stderr.write(f'Ocorreu um erro com comando $add: {ex}')

