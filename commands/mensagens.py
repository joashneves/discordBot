import asyncio

import discord
import ollama
import os
import json
from collections import deque

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
        self.message_history = deque(maxlen=10)  # Mantém as últimas 10 mensagens
        self.response_task = None
        # Carregar a lista de canais de imagem ao inicializar a classe
        self.canais_imagem = load_data(IMAGE_CHANNELS_FILE)

    async def processar_mensagem(self, mensagem):
        if mensagem.author == self.client.user:
            return
        if mensagem.content.endswith("que"):
            await mensagem.channel.send("JO!")
        if "s3nha" in mensagem.content:
            await mensagem.add_reaction('❤')

        # Responder quando o bot for mencionado
        if self.client.user in mensagem.mentions:
            content_after_mention = mensagem.content.split(' ', 1)[-1].strip()
            if content_after_mention:
                self.message_history.append(f"Usuário: {content_after_mention}")

                response = await self.generate_response(content_after_mention)
                await mensagem.channel.send(response)

                # Adiciona a resposta do bot ao histórico
                self.message_history.append(f"Bot: {response}")

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

    async def generate_response(self, prompt):
        try:
            context = " ".join(self.message_history)
            full_prompt = f"{context}\nUsuário: {prompt}\nBot:"

            stream = ollama.chat(
                model='phi3',
                messages=[{'role': 'user', 'content': full_prompt}],
                stream=True,
            )
            mensagem_bot = ""
            for chunk in stream:
                mensagem_bot += chunk['message']['content']
            return mensagem_bot
        except Exception as e:
            print(f"Erro ao processar a mensagem com ollama: {e}")
            return "Não foi possível acessar essa função."