import discord
from discord.ext import commands
import os
import aiohttp
import hashlib
from datetime import datetime
from models.db import _Sessao, AvatarSalvo

AVATAR_DIR = "imagens_avatars"  # Diretório para salvar os avatares
os.makedirs(AVATAR_DIR, exist_ok=True)  # Cria o diretório se não existir

async def save_avatar_locally(url: str, user_id: str) -> str:
    """Baixa e salva o avatar localmente."""
    avatar_filename = f"{user_id}_{hashlib.md5(url.encode()).hexdigest()}.png"
    avatar_path = os.path.join(AVATAR_DIR, avatar_filename)

    if os.path.exists(avatar_path):
        return avatar_path  # Retorna o caminho se o arquivo já existir

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(avatar_path, 'wb') as f:
                    f.write(await response.read())
                return avatar_path
            else:
                raise Exception(f"Erro ao baixar imagem: status {response.status}")

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
            # Verifica se o avatar já foi salvo
            avatar_existente = sessao.query(AvatarSalvo).filter_by(
                id_discord=user_id, hash_avatar=avatar_hash
            ).first()

            if avatar_existente:
                # Avatar já salvo, envia o existente
                embed = discord.Embed(
                    title=f"Avatar de {membro.name}",
                    description=f"Avatar já salvo em: {avatar_existente.data_arquivo.strftime('%d/%m/%Y')}"
                )
                embed.set_image(url=f"attachment://{os.path.basename(avatar_existente.caminho_arquiv)}")
                avatar_file = discord.File(avatar_existente.caminho_arquiv)
                await ctx.send(embed=embed, file=avatar_file)
                return

            # Salva o avatar localmente e no banco de dados
            avatar_path = await save_avatar_locally(avatar_url, user_id)
            novo_avatar = AvatarSalvo(
                id_discord=user_id,
                caminho_arquiv=avatar_path,
                hash_avatar=avatar_hash,
                data_arquivo=datetime.utcnow()
            )
            sessao.add(novo_avatar)
            sessao.commit()

            # Envia o novo avatar salvo
            embed = discord.Embed(
                title=f"Avatar de {membro.name}",
                description="Avatar salvo com sucesso!"
            )
            embed.set_image(url=f"attachment://{os.path.basename(avatar_path)}")
            avatar_file = discord.File(avatar_path)
            await ctx.send(embed=embed, file=avatar_file)

async def setup(bot):
    await bot.add_cog(Avatar(bot))
