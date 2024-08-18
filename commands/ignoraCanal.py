import json
import discord
import os

IMAGE_CHANNELS_FILE = os.path.join('memoria', 'canais_imagem.json')
GAMEOFF_CHANNELS_FILE = os.path.join('memoria', 'canais_gameoff.json')

def load_data(file):
    try:
        if os.path.exists(file):
            with open(file, 'r') as f:
                data = json.load(f)
                # Certifica-se de que o retorno é uma lista se o arquivo contiver uma lista
                if isinstance(data, dict) and 'canais_imagem' in data:
                    return data['canais_imagem']
                elif isinstance(data, dict) and 'canais_gameoff' in data:
                    return data['canais_gameoff']
                return []
    except Exception as e:
        print(f"Erro ao carregar dados do arquivo {file}: {e}")
    return []

def save_data(file, data):
    try:
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar dados no arquivo {file}: {e}")

class colocarCanalDeImagens():
    def __init__(self, client):
        self.client = client
        self.canais_imagem = load_data(IMAGE_CHANNELS_FILE)
        self.canais_gameoof = load_data(GAMEOFF_CHANNELS_FILE)

    async def processar_mensagem(self, mensagem):
        if mensagem.author == self.client.user:
            return

        if mensagem.content.endswith("$adicionarCanal"):
            if mensagem.author.guild_permissions.administrator:
                if mensagem.channel.id not in self.canais_imagem:
                    self.canais_imagem.append(mensagem.channel.id)  # Adiciona o canal à lista
                    save_data(IMAGE_CHANNELS_FILE, {"canais_imagem": self.canais_imagem})
                    await mensagem.channel.send(
                        f"Canal {mensagem.channel.mention} adicionado à lista de canais de imagens!")
                else:
                    await mensagem.channel.send(
                        f"O canal {mensagem.channel.mention} já está na lista de canais de imagens.")

        elif mensagem.content.endswith("$removerCanal"):
            if mensagem.author.guild_permissions.administrator:
                if mensagem.channel.id in self.canais_imagem:
                    self.canais_imagem.remove(mensagem.channel.id)  # Remove o canal da lista
                    save_data(IMAGE_CHANNELS_FILE, {"canais_imagem": self.canais_imagem})
                    await mensagem.channel.send(
                        f"Canal {mensagem.channel.mention} removido da lista de canais de imagens!")
                else:
                    await mensagem.channel.send(
                        f"O canal {mensagem.channel.mention} não está na lista de canais de imagens.")

        elif mensagem.content.endswith("$adicionarCanalGameOff"):
            if mensagem.author.guild_permissions.administrator:
                if mensagem.channel.id not in self.canais_gameoof:
                    self.canais_gameoof.append(mensagem.channel.id)  # Adiciona o canal à lista
                    save_data(GAMEOFF_CHANNELS_FILE, {"canais_gameoff": self.canais_gameoof})
                    await mensagem.channel.send(
                        f"Canal {mensagem.channel.mention} adicionado à lista de canais para ignorar!")
                else:
                    await mensagem.channel.send(
                        f"O canal {mensagem.channel.mention} já está na lista de canais para ignorar.")

        elif mensagem.content.endswith("$removerCanalGameOff"):
            if mensagem.author.guild_permissions.administrator:
                if mensagem.channel.id in self.canais_gameoof:
                    self.canais_gameoof.remove(mensagem.channel.id)  # Remove o canal da lista
                    save_data(GAMEOFF_CHANNELS_FILE, {"canais_gameoff": self.canais_gameoof})
                    await mensagem.channel.send(
                        f"Canal {mensagem.channel.mention} removido da lista de canais para ignorar!")
                else:
                    await mensagem.channel.send(
                        f"O canal {mensagem.channel.mention} não está na lista de canais para ignorar.")