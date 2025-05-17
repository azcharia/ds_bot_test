import discord
import os # Untuk mengambil token dari environment variable
import requests # Untuk memanggil API eksternal

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

# --- Fungsi untuk memanggil API chatbotmu (Google Gemini API) ---
def panggil_api_chatbot(input_text, api_key):
    # Model bisa disesuaikan jika kamu menggunakan model Gemini lain yang tersedia
    # Pastikan model yang dirujuk di URL valid. Contoh di screenshot mungkin "gemini-2.0-flash"
    # atau bisa jadi "gemini-1.5-flash-latest" atau "gemini-1.0-pro"
    # Sebaiknya periksa dokumentasi terbaru Google AI Studio untuk model yang valid.
    # Untuk contoh ini, kita gunakan placeholder yang mirip dari screenshot.
    # Mari kita asumsikan modelnya adalah "gemini-1.5-flash-latest" untuk contoh ini, karena lebih umum.
    model_name = "gemini-1.5-flash-latest" # GANTI JIKA PERLU SESUAI MODEL YANG KAMU GUNAKAN
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{
            "parts": [{"text": input_text}]
        }]
    }

    try:
        print(f"Mengirim permintaan ke Gemini API: URL={api_url[:80]}... Payload={str(payload)[:100]}...")
        response = requests.post(api_url, headers=headers, json=payload, timeout=45) # Timeout 45 detik
        response.raise_for_status()  # Akan raise exception untuk status HTTP 4xx/5xx
        
        response_data = response.json()
        print(f"Respons mentah dari Gemini API: {str(response_data)[:200]}...")

        # Struktur respons Gemini (biasanya):
        # {
        #   "candidates": [
        #     {
        #       "content": {
        #         "parts": [
        #           {"text": "Respons dari AI di sini"}
        #         ],
        #         "role": "model"
        #       }, 
        #       ... (info lain seperti finishReason, safetyRatings)
        #     }
        #   ]
        # }
        # Kita perlu mengambil teks dari parts pertama dari kandidat pertama.
        
        candidates = response_data.get("candidates")
        if candidates and len(candidates) > 0:
            content = candidates[0].get("content")
            if content and content.get("role") == "model":
                parts = content.get("parts")
                if parts and len(parts) > 0:
                    actual_reply = parts[0].get("text")
                    if actual_reply:
                        print(f"Sukses mendapatkan balasan dari Gemini: {actual_reply[:100]}...")
                        return actual_reply.strip()
        
        # Jika struktur tidak sesuai atau tidak ada teks balasan
        print("Error: Struktur respons Gemini tidak sesuai atau tidak ada teks balasan.")
        return "Maaf, saya menerima respons yang tidak terduga dari layanan AI."

    except requests.exceptions.Timeout:
        print(f"Error: Timeout saat memanggil Gemini API setelah 45 detik.")
        return "Maaf, layanan AI sedang lambat merespons. Coba lagi nanti."
    except requests.exceptions.RequestException as e:
        print(f"Error saat memanggil API Gemini: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json() # Coba dapatkan detail error dari JSON respons
                print(f"Detail error dari API: {error_detail}")
                # Bisa jadi ada pesan error spesifik di response_data.error.message
                api_error_message = error_detail.get("error", {}).get("message", "")
                if api_error_message:
                    return f"Maaf, terjadi kesalahan dari layanan AI: {api_error_message}"
            except ValueError: # Jika respons error bukan JSON
                print(f"Respons error dari API (bukan JSON): {e.response.text}")
        return "Maaf, ada masalah saat menghubungi layanan AI."
    except Exception as e:
        print(f"Error tidak terduga saat memproses respons API Gemini: {e}")
        return "Maaf, terjadi kesalahan internal saat memproses balasan AI."

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
    user_message_cleaned = message.content # Pesan asli

    try:
        if not user_message_cleaned: # Jika pesan kosong
             await message.channel.send(f"Halo {message.author.mention if not is_dm else ''}! Kamu mengirim pesan kosong?".strip())
        else:
            # Pastikan CHATBOT_API_KEY sudah di-setting dengan benar di environment variables
            if not CHATBOT_API_KEY:
                print("Warning: CHATBOT_API_KEY tidak diset. Bot akan mengirim respons default.")
                response_text = f"Kamu bilang: '{user_message_cleaned}'. (CHATBOT_API_KEY tidak diset, ini respons default)."
            else:
                # Panggil fungsi API chatbotmu yang sebenarnya
                response_text = panggil_api_chatbot(user_message_cleaned, CHATBOT_API_KEY)
                if response_text is None or response_text == "": # Jika API gagal atau tidak mengembalikan apa-apa
                    response_text = "Maaf, saya tidak bisa mendapatkan respons saat ini atau responsnya kosong."
            
            # Logika baru untuk mengirim pesan panjang dalam beberapa bagian
            if len(response_text) > 2000:
                print(f"Respons dari Gemini terlalu panjang ({len(response_text)} karakter). Membaginya menjadi beberapa pesan.")
                parts = []
                current_pos = 0
                while current_pos < len(response_text):
                    # Tentukan batas potong, usahakan tidak memotong di tengah kalimat/kata jika memungkinkan
                    # Batas ideal adalah 2000, tapi kita ambil sedikit lebih kecil untuk aman
                    end_pos = min(current_pos + 1990, len(response_text))
                    
                    # Jika kita belum mencapai akhir teks dan masih bisa mencari pemisah yang baik
                    if end_pos < len(response_text):
                        # Coba cari newline atau spasi terdekat dari belakang
                        best_split = -1
                        # Cari newline dulu dalam rentang tertentu dari end_pos
                        temp_split_nl = response_text.rfind('\n', current_pos, end_pos)
                        if temp_split_nl != -1 and temp_split_nl > current_pos : # Pastikan newline bukan di awal chunk
                            best_split = temp_split_nl + 1 # Ambil setelah newline
                        else:
                            # Jika tidak ada newline, cari spasi
                            temp_split_sp = response_text.rfind(' ', current_pos, end_pos)
                            if temp_split_sp != -1 and temp_split_sp > current_pos: # Pastikan spasi bukan di awal chunk
                                best_split = temp_split_sp + 1 # Ambil setelah spasi
                        
                        if best_split != -1 and best_split > current_pos: # Pastikan kita benar-benar memotong
                            end_pos = best_split
                        # Jika tidak ada pemisah yang baik, potong paksa di 1990 atau akhir teks

                    part_to_send = response_text[current_pos:end_pos].strip()
                    if part_to_send: # Hanya kirim jika ada isinya
                        parts.append(part_to_send)
                    current_pos = end_pos
                
                for part in parts:
                    await message.channel.send(part)
                    # import asyncio # Jika ingin delay, uncomment dan import di atas file
                    # await asyncio.sleep(0.3) # Delay kecil antar pesan jika perlu
            else:
                # Jika respons tidak terlalu panjang, kirim seperti biasa
                await message.channel.send(f"{response_text}")

    except Exception as e:
        print(f"Error saat memproses pesan: {e}")
        await message.channel.send(f"Maaf, terjadi kesalahan saat memproses permintaanmu.")

# Jalankan bot
client.run(DISCORD_BOT_TOKEN) 