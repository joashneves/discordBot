import discord
import os
import json

prefix = '$'
DATA_FILE = os.path.join('memoria', 'game.json')
GAME_FILE = os.path.join('memoria', 'dados_personagem.json')
COINS_FILE = os.path.join('memoria', 'coins.json')
PROFILE_FILE = os.path.join('memoria', 'perfil.json')
CONQUISTAS_FILE = os.path.join('memoria', 'conquistas.json')

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

coins_data = load_data(COINS_FILE)
conquistas_data = load_data(CONQUISTAS_FILE)

##region
# Exemplos de Embeds de Conquistas
##region
conseguir_primeiro_personagem = discord.Embed(title="Primeiro personagem Capturado", color=0x7289DA)
conseguir_primeiro_personagem.add_field(name="Descrição", value="Você conseguiu seu primeiro personagem")
conseguir_primeiro_personagem.add_field(name="Emoji", value="1️⃣")
##endregion

##region
upar_perfil = discord.Embed(title="Perfil Upado", color=0x7289DA)
upar_perfil.add_field(name="Descrição", value="Você upou seu perfil pela primeira vez")
upar_perfil.add_field(name="Emoji", value="⭐")
##endregion

##region
editar_toda_colecao = discord.Embed(title="Coleção Completa", color=0x7289DA)
editar_toda_colecao.add_field(name="Descrição", value="Você editou toda a coleção de personagens")
editar_toda_colecao.add_field(name="Emoji", value="🏆")
##endregion

##region
editar_todo_perfil = discord.Embed(title="Perfil Completo", color=0x7289DA)
editar_todo_perfil.add_field(name="Descrição", value="Você completou todas as seções do seu perfil")
editar_todo_perfil.add_field(name="Emoji", value="🎨")
##endregion

##region
chegaro_ao_level_5 = discord.Embed(title="Level 5", color=0x7289DA)
chegaro_ao_level_5.add_field(name="Descrição", value="Você alcançou o nível 5")
chegaro_ao_level_5.add_field(name="Emoji", value="5️⃣")
##endregion

##region
doar_personagem = discord.Embed(title="Doação", color=0x7289DA)
doar_personagem.add_field(name="Descrição", value="Você doou um personagem para outro jogador")
doar_personagem.add_field(name="Emoji", value="❤️")
##endregion

##region
libertar_personagem = discord.Embed(title="Libertação", color=0x7289DA)
libertar_personagem.add_field(name="Descrição", value="Você libertou um personagem")
libertar_personagem.add_field(name="Emoji", value="🕊️")
##endregion

##region
adivinhar_10_personagem_em_seguida = discord.Embed(title="Mestre dos Personagens", color=0x7289DA)
adivinhar_10_personagem_em_seguida.add_field(name="Descrição", value="Você adivinhou 10 personagens seguidos corretamente")
adivinhar_10_personagem_em_seguida.add_field(name="Emoji", value="🎯")
##endregion

##region
conseguir_10000_moedas = discord.Embed(title="Riqueza", color=0x7289DA)
conseguir_10000_moedas.add_field(name="Descrição", value="Você conseguiu acumular 10,000 moedas")
conseguir_10000_moedas.add_field(name="Emoji", value="💰")
##endregion

# Adicione os embeds à lista de conquistas
conquistas_embeds = [
    conseguir_primeiro_personagem,
    upar_perfil,
    editar_toda_colecao,
    editar_todo_perfil,
    chegaro_ao_level_5,
    doar_personagem,
    libertar_personagem,
    adivinhar_10_personagem_em_seguida,
    conseguir_10000_moedas
]

##endregion
class ViewInfo(discord.ui.View):
    def __init__(self, embeds):
        super().__init__()
        self.embeds = embeds
        self.current = 0

    @discord.ui.button(label='<<<', style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current = (self.current - 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

    @discord.ui.button(label='>>>', style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current = (self.current + 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

class Conquistas:
    def __init__(self, client):
        self.client = client
        self.conquistas_data = load_data(CONQUISTAS_FILE)
        self.embeds = conquistas_embeds  # Use a lista de conquistas_embeds aqui
        self.coins_data = load_data(COINS_FILE)
        self.dados_personagem = load_data(GAME_FILE)
        self.perfil_data = load_data(PROFILE_FILE)
        self.acertos_consecutivos = {}

    async def adivinhar_10_personagens_seguidos(self,user_id):
        user_id = str(user_id)
        perfil_user = self.perfil_data.get(user_id, {})
        acertos_consecutivos = self.acertos_consecutivos

        if user_id not in conquistas_data:
            conquistas_data[user_id] = []

        if user_id not in acertos_consecutivos:
            acertos_consecutivos[user_id] = 0
        else:
            acertos_consecutivos[user_id] += 1

        if acertos_consecutivos[user_id] >= 10:
            if "🎯" not in conquistas_data[user_id]:
                conquistas_data[user_id].append("🎯")
                save_data(CONQUISTAS_FILE, conquistas_data)
                return True

        return False

    async def perfil_tem_todas_competencias(self, user_id, ):
        user_id = str(user_id)
        perfil_user = self.perfil_data.get(user_id, {})

        descricao = perfil_user.get("descricao")
        personagem_favorito = perfil_user.get("personagem_favorito")
        imagem_personalizada = perfil_user.get("imagem_personalizada")
        cor_embed = perfil_user.get("cor_embed")

        if descricao and personagem_favorito and imagem_personalizada and cor_embed:
            if "🎨" not in self.conquistas_data[user_id]:
                self.conquistas_data[user_id].append("🎨")
                save_data(CONQUISTAS_FILE, self.conquistas_data)
        else:
            return False

    async def atribuir_conquista(self, user_id):
        user_id = str(user_id)
        perfil_user = self.perfil_data.get(user_id, {})
        moedas_user = self.coins_data.get(user_id, 0)

        if user_id not in self.conquistas_data:
            self.conquistas_data[user_id] = []

        # Verificar se o usuário tem mais de 10.000 moedas
        mais_de_10000_moedas = moedas_user > 10000
        conquista_atribuida = False

        # Verificar se todas as descrições dos personagens não são "Descrição padrão"
        todas_descricoes_personalizadas = all(
            personagem.get("descricao") != "Descrição padrão"
            for personagem in perfil_user.get("personagens", [])
        )

        nivel_usuario = perfil_user.get("nivel", 1)
        if nivel_usuario >= 5:
            if "5️⃣" not in self.conquistas_data[user_id]:
                self.conquistas_data[user_id].append("5️⃣")
                save_data(CONQUISTAS_FILE, self.conquistas_data)

        if todas_descricoes_personalizadas:
            if "🏆" not in self.conquistas_data[user_id]:
                self.conquistas_data[user_id].append("🏆")
                save_data(CONQUISTAS_FILE, self.conquistas_data)

        if mais_de_10000_moedas:
            if "💰" not in self.conquistas_data[user_id]:
                self.conquistas_data[user_id].append("💰")
                conquista_atribuida = True

        if conquista_atribuida:
            save_data(CONQUISTAS_FILE, self.conquistas_data)
            return True

    # Funções para ações
    async def doar_personagem(self, user_id):
        if "❤️" not in self.conquistas_data[user_id]:
            self.conquistas_data[user_id].append("❤️")
            save_data(CONQUISTAS_FILE, self.conquistas_data)
    async def libertar_personagem(self, user_id):
        if "🕊️" not in self.conquistas_data[user_id]:
            self.conquistas_data[user_id].append("🕊️")
            save_data(CONQUISTAS_FILE, self.conquistas_data)
    async def upar_perfil(self, user_id):
        if "⭐" not in self.conquistas_data[user_id]:
            self.conquistas_data[user_id].append("⭐")
            save_data(CONQUISTAS_FILE, self.conquistas_data)
    async def primeiro_personagem(self, user_id):
        if "1️⃣" not in self.conquistas_data[user_id]:
            self.conquistas_data[user_id].append("1️⃣")
            save_data(CONQUISTAS_FILE, self.conquistas_data)
    async def processar_mensagem(self, mensagem):
        if mensagem.author == self.client.user:
            return

        if mensagem.content.startswith(prefix + "conquistas_lists"):
            view_info = ViewInfo(self.embeds)
            await mensagem.channel.send(embed=self.embeds[0], view=view_info)
