import discord
import ollama
import os
import json

IMAGE_CHANNELS_FILE = os.path.join('memoria', 'canais_imagem.json')

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

class messagensBotRespostas():
    def __init__(self, client):
        self.client = client
        # Carregar a lista de canais de imagem ao inicializar a classe
        self.canais_imagem = load_data(IMAGE_CHANNELS_FILE)

    async def processar_mensagem(self, mensagem):
        if mensagem.author == self.client.user:
            return
        if mensagem.content.endswith("que"):
            await mensagem.channel.send("JO!")
        if "s3nha" in mensagem.content:
            await mensagem.add_reaction('❤')
        if mensagem.content.startswith("$skalart"):
            try:
                prompt = mensagem.content.split('skalart', 1)[1].strip()
                print(f"prompt: {prompt}")
                stream = ollama.chat(
                    model='phi3',
                    messages=[{'role': 'user', 'content': f'Responda em portugues a mensagem em uma mensagem curta de no maximo 2 linhas: {prompt}'}],
                    stream=True,
                )
                mensagem_bot = ""
                for chunk in stream:
                    mensagem_bot += chunk['message']['content']
                await mensagem.channel.send(mensagem_bot)
            except:
                await mensagem.channel.send("não foi possivel acessar essa função")

# Verifica se a mensagem é em um canal de imagens e se contém anexos
        if mensagem.channel.id in  self.canais_imagem:
            if mensagem.attachments:
                attachment = mensagem.attachments[0]
                if attachment.url:
                    try:
                        # Pega a última mensagem do canal para adicionar reações
                        last_message = await mensagem.channel.fetch_message(mensagem.channel.last_message_id)
                        emoji_list = ['👍', '👎', '❤', '😂', '😲']
                        for emoji in emoji_list:
                            await last_message.add_reaction(emoji)
                    except Exception as e:
                        print(f"Erro ao adicionar reações: {e}")