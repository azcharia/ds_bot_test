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

    # Cek apakah pesan datang dari DM
    is_dm = isinstance(message.channel, discord.DMChannel)

    print(f"Pesan dari {message.author}: {message.content} di {'DM' if is_dm else f'channel {message.channel} server {message.guild}'}")

    # Logika respons: Bot akan merespons semua pesan yang diterimanya
    # (baik di DM maupun di channel server)
    user_message_cleaned = message.content # Pesan asli, tidak perlu membersihkan mention lagi

    try:
        # Di sini kamu akan memanggil API chatbotmu
        # response_text = panggil_api_chatbot(user_message_cleaned, CHATBOT_API_KEY)
        
        if not user_message_cleaned: # Jika pesan kosong
             await message.channel.send(f"Halo {message.author.mention if not is_dm else ''}! Kamu mengirim pesan kosong?".strip())
        else:
            # Gantilah ini dengan logika chatbotmu yang sebenarnya
            # Pastikan CHATBOT_API_KEY sudah di-setting dengan benar di environment variables
            if not CHATBOT_API_KEY:
                print("Warning: CHATBOT_API_KEY tidak diset. Bot akan mengirim respons default.")
                response_text = f"Kamu bilang: '{user_message_cleaned}'. (CHATBOT_API_KEY tidak diset, ini respons default)."
            else:
                # Contoh pemanggilan (sesuaikan dengan API-mu)
                # response_text = panggil_api_chatbot(user_message_cleaned, CHATBOT_API_KEY)
                response_text = f"Respons untuk '{user_message_cleaned}'. (Logika chatbotmu di sini)." # Respons lebih umum

            await message.channel.send(f"{response_text}") # Tidak perlu mention author lagi kecuali diinginkan

    except Exception as e:
        print(f"Error saat memproses pesan: {e}")
        await message.channel.send(f"Maaf, terjadi kesalahan saat memproses permintaanmu.")

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