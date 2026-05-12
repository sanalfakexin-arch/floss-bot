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
    return "Bot aktif!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT AYARLARI ---
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- BOT ÇALIŞTIĞINDA ---
@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user} olarak giriş yaptı!')
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} adet eğik çizgi komutu senkronize edildi.")
    except Exception as e:
        print(f"❌ Komutlar senkronize edilemedi: {e}")

# --- ÖRNEK KURULUM KOMUTU ---
@bot.tree.command(name="kurulum", description="Botun kurulumunu kontrol eder.")
async def kurulum(interaction: discord.Interaction):
    await interaction.response.send_message("✅ Floss Bot kurulumu başarıyla tamamlandı ve çalışıyor!", ephemeral=True)

# --- ÇALIŞTIRMA ---
keep_alive()

# Render panelindeki Environment kısmına yazdığın ismi kullanır
token = os.getenv("DISCORD_TOKEN")

if token:
    bot.run(token)
else:
    print("❌ HATA: DISCORD_TOKEN bulunamadı! Render Environment kısmını kontrol et.")
