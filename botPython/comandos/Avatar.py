import discord
from discord.ext import commands
import os
import aiohttp
import hashlib
from datetime import datetime
from models.db import _Sessao, AvatarSalvo

AVATAR_DIR = "imagens_avatars"
os.makedirs(AVATAR_DIR, exist_ok=True)  # Cria o diretório se não existir

async def save_avatar_locally(url: str, user_id: str) -> str:
    """Baixa e salva o avatar localmente."""
    avatar_filename = f"{user_id}_{hashlib.md5(url.encode()).hexdigest()}.png"
    avatar_path = os.path.join(AVATAR_DIR, avatar_filename)

    if os.path.exists(avatar_path):
        return avatar_path

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(avatar_path, 'wb') as f:
                    f.write(await response.read())
                return avatar_path
            else:
                raise Exception(f"Erro ao baixar imagem: status {response.status}")

class AvatarView(discord.ui.View):
    """Interface para navegar pelos avatares."""
    def __init__(self, avatares, membro):
        super().__init__(timeout=60)  # Tempo limite de 60 segundos
        self.avatares = avatares
        self.membro = membro
        self.index = 0

    async def update_message(self, interaction):
        """Atualiza a mensagem com o avatar atual."""
        avatar = self.avatares[self.index]
        embed = discord.Embed(
            title=f"Avatar de {self.membro.name}",
            description=f"Data: {avatar.data_arquivo.strftime('%d/%m/%Y')}"
        )
        embed.set_image(url=f"attachment://{os.path.basename(avatar.caminho_arquiv)}")
        avatar_file = discord.File(avatar.caminho_arquiv)

        await interaction.response.edit_message(embed=embed, attachments=[avatar_file], view=self)

    @discord.ui.button(label="Anterior", style=discord.ButtonStyle.primary)
    async def anterior(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = (self.index - 1) % len(self.avatares)
        await self.update_message(interaction)

    @discord.ui.button(label="Próximo", style=discord.ButtonStyle.primary)
    async def proximo(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = (self.index + 1) % len(self.avatares)
        await self.update_message(interaction)

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx: commands.Context, membro: discord.Member = None):
        membro = membro or ctx.author  # Usa o autor se nenhum membro for passado
        user_id = str(membro.id)
        avatar_url = membro.display_avatar.url
        avatar_hash = hashlib.md5(avatar_url.encode()).hexdigest()

        with _Sessao() as sessao:
            # Obtém o último avatar salvo para o usuário
            ultimo_avatar = sessao.query(AvatarSalvo).filter_by(id_discord=user_id).order_by(AvatarSalvo.id.desc()).first()

            if ultimo_avatar and ultimo_avatar.hash_avatar == avatar_hash:
                # Busca todos os avatares do usuário
                avatares = sessao.query(AvatarSalvo).filter_by(id_discord=user_id).all()
                 # Envia o primeiro avatar com a interface de navegação
                embed = discord.Embed(
                    title=f"Avatar de {membro.name}",
                    description=f"Data: {avatares[0].data_arquivo.strftime('%d/%m/%Y')}"
                )
                embed.set_image(url=f"attachment://{os.path.basename(avatares[0].caminho_arquiv)}")
                avatar_file = discord.File(avatares[0].caminho_arquiv)

                view = AvatarView(avatares, membro)
                await ctx.send(embed=embed, file=avatar_file, view=view)
                
            else:
                # Salva o novo avatar
                avatar_path = await save_avatar_locally(avatar_url, user_id)
                novo_avatar = AvatarSalvo(
                    id_discord=user_id,
                    caminho_arquiv=avatar_path,
                    hash_avatar=avatar_hash,
                    data_arquivo=datetime.utcnow()
                )
                sessao.add(novo_avatar)
                sessao.commit()

                # Busca todos os avatares do usuário para navegação
                avatares = sessao.query(AvatarSalvo).filter_by(id_discord=user_id).all()

                # Envia o primeiro avatar com a interface de navegação
                embed = discord.Embed(
                    title=f"Avatar de {membro.name}",
                    description="Avatar atualizado e salvo com sucesso!"
                )
                embed.set_image(url=f"attachment://{os.path.basename(avatar_path)}")
                avatar_file = discord.File(avatar_path)

                view = AvatarView(avatares, membro)
                await ctx.send(embed=embed, file=avatar_file, view=view)

async def setup(bot):
    await bot.add_cog(Avatar(bot))
