import discord
import os # Untuk mengambil token dari environment variable

# --- API KEY CHATBOT KAMU ---
# Ganti dengan cara kamu mengambil API key chatbot (misalnya, dari environment variable atau file konfigurasi)
CHATBOT_API_KEY = os.environ.get("CHATBOT_API_KEY") # Ambil CHATBOT_API_KEY dari environment variable
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_TOKEN") # Ambil token dari environment variable

if not DISCORD_BOT_TOKEN:
    print("Error: DISCORD_TOKEN environment variable not set.")
    exit()

if not CHATBOT_API_KEY:
    print("Error: CHATBOT_API_KEY environment variable not set.")
    # Kamu bisa memilih untuk keluar (exit()) atau menangani kasus ini secara berbeda
    # exit() 
    # Untuk saat ini, kita hanya print error tapi bot mungkin tetap jalan tanpa fungsionalitas penuh
    # jika CHATBOT_API_KEY penting untuk semua operasi.

# Tentukan intents yang dibutuhkan botmu
intents = discord.Intents.default()
intents.message_content = True # Penting untuk membaca isi pesan
intents.members = True # Jika butuh info member
# intents.presences = True # Jika butuh info status

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot {client.user} telah online!')
    print('------')

@client.event
async def on_message(message):
    # Jangan sampai bot merespons dirinya sendiri
    if message.author == client.user:
        return

    print(f"Pesan dari {message.author}: {message.content} di channel {message.channel} server {message.guild}")

    # Filter pesan: misalnya, bot hanya merespons jika di-mention atau ada kata kunci tertentu
    # Contoh: respons jika bot di-mention
    if client.user.mentioned_in(message):
        try:
            # Di sini kamu akan memanggil API chatbotmu
            # Misalnya:
            # response_text = panggil_api_chatbot(message.content, CHATBOT_API_KEY)
            
            # Untuk contoh ini, kita balas saja dengan pesan sederhana
            user_message_cleaned = message.content.replace(f'<@!{client.user.id}>', '').replace(f'<@{client.user.id}>', '').strip() # Hapus mention bot dari pesan
            
            if not user_message_cleaned: # Jika hanya mention tanpa pesan lain
                 await message.channel.send(f"Halo {message.author.mention}! Ada yang bisa saya bantu?")
            else:
                # Gantilah ini dengan logika chatbotmu yang sebenarnya
                response_text = f"Kamu bilang: '{user_message_cleaned}'. Ini respons dari bot (ganti dengan logikamu)."
                await message.channel.send(f"{message.author.mention} {response_text}")

        except Exception as e:
            print(f"Error saat memproses pesan: {e}")
            await message.channel.send(f"{message.author.mention} Maaf, terjadi kesalahan saat memproses permintaanmu.")

# --- Fungsi untuk memanggil API chatbotmu (CONTOH) ---
# def panggil_api_chatbot(input_text, api_key):
#     # Logika untuk mengirim permintaan ke API chatbotmu dan mendapatkan respons
#     # Misalnya menggunakan library `requests`
#     # import requests
#     # headers = {"Authorization": f"Bearer {api_key}"}
#     # payload = {"prompt": input_text}
#     # response = requests.post("URL_API_CHATBOTMU", headers=headers, json=payload)
#     # return response.json().get("response_text")
#     pass

# Jalankan bot
client.run(DISCORD_BOT_TOKEN) 