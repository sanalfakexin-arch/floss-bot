import discord
from discord.ext import commands
from discord import ui, app_commands
from datetime import datetime
from flask import Flask
from threading import Thread
import os

# --- 7/24 AKTİF TUTMA (KEEP ALIVE) KODU ---
app = Flask('')

@app.route('/')
def home():
    return "Bot 7/24 Aktif!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ------------------------------------------

TOKEN = "MTUwMzQzMzI1ODgxNjM3Njg2Mw.GiWmfo.91YC5FEjPGG4dk4iQYGTuJsrW5yBp7gM9OTDSk"
LOG_KANAL_ID = 1503431572022624338  
FLOSS_ROL_ID = 1482533789321134133
SORUMLU_ROL_ID = 1503764470365819090

class OnaySistemi(ui.View):
    def __init__(self, basvuran_id):
        super().__init__(timeout=None)
        self.basvuran_id = basvuran_id

    @ui.button(label="Onay", style=discord.ButtonStyle.green, emoji="✅")
    async def onay(self, interaction: discord.Interaction, button: ui.Button):
        guild = interaction.guild
        member = guild.get_member(self.basvuran_id)
        role = guild.get_role(FLOSS_ROL_ID)
        if member and role:
            await member.add_roles(role)
            await interaction.response.send_message(f"✅ {member.mention} onaylandı!", ephemeral=False)
            await interaction.message.edit(view=None)

    @ui.button(label="Red", style=discord.ButtonStyle.red, emoji="❌")
    async def red(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("❌ Başvuru reddedildi.", ephemeral=False)
        await interaction.message.edit(view=None)

class BasvuruFormu(ui.Modal, title='Floss Family | Başvuru Formu'):
    isim_yas = ui.TextInput(label='İsim / Yaş', required=True)
    aktiflik = ui.TextInput(label='Aktiflik Saatleri', required=True)
    fivem_saat = ui.TextInput(label='FiveM Saati', required=True)
    neden_biz = ui.TextInput(label='Neden Floss?', style=discord.TextStyle.paragraph, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        kanal = interaction.client.get_channel(LOG_KANAL_ID)
        embed = discord.Embed(title="📩 Yeni Başvuru", color=discord.Color.blue(), timestamp=datetime.now())
        embed.add_field(name="Başvuran", value=f"{interaction.user.mention}", inline=False)
        embed.add_field(name="İsim / Yaş", value=self.isim_yas.value)
        embed.add_field(name="Aktiflik", value=self.aktiflik.value)
        embed.add_field(name="Saati", value=self.fivem_saat.value)
        embed.add_field(name="Neden?", value=self.neden_biz.value)
        
        await kanal.send(content=f"🔔 Yeni Başvuru! <@&{SORUMLU_ROL_ID}>", embed=embed, view=OnaySistemi(interaction.user.id))
        await interaction.response.send_message("✅ Başvurunuz iletildi!", ephemeral=True)

class BasvuruButonuView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label='Ekip İçi Başvuru', style=discord.ButtonStyle.primary, custom_id='basvuru_butonu')
    async def basvuru_yap(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(BasvuruFormu())

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True 
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.add_view(BasvuruButonuView())
        await self.tree.sync()

    async def on_ready(self):
        print(f"✅ Bot {self.user} aktif!")

bot = MyBot()

@bot.tree.command(name="kurulum", description="Başvuru panelini kurar")
async def kurulum(interaction: discord.Interaction):
    embed = discord.Embed(title="🔗 Floss Family Başvuru", description="Katılmak için butona tıkla!", color=discord.Color.greyple())
    await interaction.channel.send(embed=embed, view=BasvuruButonuView())
    await interaction.response.send_message("Panel kuruldu.", ephemeral=True)

if __name__ == "__main__":
    keep_alive() # Bu satır Render'da uyumamayı sağlar
    bot.run(TOKEN)