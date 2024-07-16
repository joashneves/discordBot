import discord
import os
import json

prefix = '$'
DATA_FILE = os.path.join('memoria', 'game.json')
GAME_FILE = os.path.join('memoria', 'dados_personagem.json')
COINS_FILE = os.path.join('memoria', 'coins.json')

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

class ViewInfo(discord.ui.View):
    def __init__(self, embeds, jogador_id, dados_personagem):
        super().__init__()
        self.embeds = embeds
        self.current = 0
        self.jogador_id = jogador_id
        self.dados_personagem = dados_personagem

    @discord.ui.button(label='<<<', style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current = (self.current - 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

    @discord.ui.button(label='>>>', style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current = (self.current + 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

class Wikilist:
    def __init__(self, client):
        self.client = client
        self.dados_personagem = load_data(GAME_FILE)
        self.todos_personagens = load_data(DATA_FILE)

        # Listas para armazenar personagens encontrados e não encontrados
        self.personagens_encontrados = []
        self.personagens_nao_encontrados = []

        # Preencher as listas de personagens encontrados e não encontrados
        self.preencher_listas()

    def preencher_listas(self):
        personagens_game = load_data(DATA_FILE)
        for jogador_id, personagens in self.dados_personagem.items():
            for personagem in personagens:
                if any(p['nome'] == personagem['nome'] for p in personagens_game):
                    self.personagens_encontrados.append(personagem)
                else:
                    self.personagens_nao_encontrados.append(personagem)

    async def processar_mensagem(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith(prefix + 'pesc'):
            await self.procurar_personagem(message)
        elif message.content.startswith(prefix + 'wikilist'):
            await self.mostrar_lista_personagens(message)
        elif message.content.startswith(prefix + 'wiki'):
            await self.mostrar_personagens_encontrados(message)

    async def procurar_personagem(self, message):
        self.dados_personagem = load_data(GAME_FILE)
        self.todos_personagens = load_data(DATA_FILE)  # Carrega todos os personagens (descobertos e não descobertos)

        termo_busca = message.content[len(prefix + 'pesc'):].strip().lower()
        if not termo_busca:
            await message.channel.send("Você precisa fornecer um nome para procurar.")
            return

        resultados_descobertos = []
        # Primeiro, procura entre todos os personagens descobertos
        for jogador_id, personagens in self.dados_personagem.items():
            for personagem in personagens:
                if termo_busca in personagem['nome'].lower():
                    print(f'Personagem descoberto encontrado: {personagem["nome"]}!')
                    resultados_descobertos.append(personagem)

        if resultados_descobertos:
            embeds = self.criar_embeds_resultados(resultados_descobertos)
            await message.channel.send(embed=embeds[0])
        else:
            # Se não encontrou personagens descobertos, procura personagens não descobertos
            resultados_nao_descobertos = []
            for personagem in self.todos_personagens:
                if 'data' not in personagem and termo_busca in personagem['nome'].lower():
                    print(f'Personagem não descoberto encontrado: {personagem["nome"]}!')
                    resultados_nao_descobertos.append(personagem)

            if resultados_nao_descobertos:
                embeds = self.criar_embeds_resultados(resultados_nao_descobertos)
                await message.channel.send(embed=embeds[0])
            else:
                await message.channel.send(f"Nenhum personagem encontrado com o nome '{termo_busca}'.")

    async def mostrar_personagens_encontrados(self, message):
        embeds = self.criar_embeds_resultados(self.personagens_encontrados)
        if embeds:
            view = ViewInfo(embeds, message.author.id, self.dados_personagem)
            await message.channel.send(embed=embeds[0], view=view)
        else:
            await message.channel.send("Nenhum personagem foi encontrado até o momento.")

    async def mostrar_lista_personagens(self, message):
        personagens = load_data(DATA_FILE)

        if not personagens:
            await message.channel.send("Nenhum personagem disponível no momento.")
            return

        lista_nomes = [personagem['nome'] for personagem in personagens]
        lista_nomes_chunks = [lista_nomes[i:i + 10] for i in
                              range(0, len(lista_nomes), 10)]  # Dividindo em chunks de 10

        current_page = 0
        total_pages = len(lista_nomes_chunks)

        embeds = await self.criar_embeds_paginados(lista_nomes_chunks, current_page, total_pages)
        view = ViewInfo(embeds, message.author.id, self.dados_personagem)
        await message.channel.send(embed=embeds[current_page], view=view)

    async def criar_embeds_paginados(self, lista_nomes_chunks, current_page, total_pages):
        embeds = []
        for i, chunk in enumerate(lista_nomes_chunks):
            embed = discord.Embed(
                title=f"Lista de todos os personagens - Página {i + 1}/{total_pages}",
                description="\n".join(chunk)
            )
            embeds.append(embed)
        return embeds

    def criar_embeds_resultados(self, resultados):
        embeds = []
        for item in resultados:
            if 'descricao' in item and item['descricao']:
                # Personagem com descrição (considerado descoberto)
                embed = discord.Embed(
                    title=f'Personagem: {item["nome"]}',
                    description=f'Descrição: {item["descricao"]}'
                )
                embed.set_image(url=item['imagem'])
                embed.add_field(name='De(Franquia):', value=item['serie'], inline=False)
                embed.add_field(name='Data de descoberta', value=item['data'], inline=False)
                descobridores = self.encontrar_descobridores(item['nome'])
                if descobridores:
                    embed.set_footer(text=f'Descoberto por: {", ".join(descobridores)}')
            else:
                # Personagem sem descrição (considerado não descoberto)
                embed = discord.Embed(
                    title=f'Personagem: {item["nome"]}',
                    description='Este personagem ainda não foi descoberto!'
                )
                embed.set_image(url=item['imagem'])
                embed.add_field(name='De(Franquia):', value=item.get('serie', 'Desconhecida'), inline=False)

            embeds.append(embed)
        return embeds

    def encontrar_descobridores(self, nome_personagem):
        descobridores = []
        for jogador_id, personagens in self.dados_personagem.items():
            for personagem in personagens:
                if personagem['nome'].lower() == nome_personagem.lower():
                    descobridores.append(jogador_id)

        return descobridores
