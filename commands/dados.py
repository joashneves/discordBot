import json
import os
import discord
import datetime
import random

from commands.user import User

r = random
class Dados():
    def __init__(self, client):
        self.client = client

    async def processar_mensagem(self, mensagem):
        if mensagem.author == self.client.user:
            return

        conteudo = mensagem.content.lower()

        if conteudo.startswith('r'):
            # Dividir a mensagem nos espaços para obter os parâmetros
            parametros = conteudo.split()

            # Se não houver parâmetros suficientes, sair
            if len(parametros) < 2:
                await mensagem.channel.send("Por favor, forneça parâmetros válidos. Exemplo: r 2d20")
                return

            # Obter a quantidade e a quantidade de lados do dado
            quantidade, lados = map(int, parametros[1].split('d'))

            # Simular os lançamentos dos dados
            resultados = [r.randint(1, lados) for _ in range(quantidade)]

            # Enviar os resultados de volta ao canal
            await mensagem.channel.send(f"Resultados do dado de {quantidade}d{lados}: {resultados}")
