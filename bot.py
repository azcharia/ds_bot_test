import discord
import os
import requests
import json # Untuk debugging payload
from collections import deque # Untuk Short-Term Memory
from datetime import datetime # Untuk waktu
import pytz # Untuk zona waktu
import random # Untuk perintah acak seperti quote

# --- Variabel Konfigurasi ---
CHATBOT_API_KEY = os.environ.get("CHATBOT_API_KEY")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
GEMINI_MODEL_NAME = "gemini-1.5-flash-latest" # Pastikan ini model yang valid dan kamu punya akses
BOT_NAME = "emma" # Nama panggilan bot, case-insensitive
STM_MAX_MESSAGES = 10 # Jumlah pesan terakhir yang disimpan untuk konteks STM
JAKARTA_TZ = pytz.timezone('Asia/Jakarta')
COMMAND_PREFIX = "!" # Prefix untuk perintah bot

# --- System Prompt untuk Kepribadian Emma ---
EMMA_SYSTEM_PROMPT = f"""
Kamu adalah Emma, seorang gadis berusia 23 tahun (lahir 18 April 2000). Kamu tinggal di zona waktu Asia/Jakarta.
Nama panggilanmu adalah Emma. Kamu tidak selalu menyebut namamu sendiri saat berbicara.
Kamu tidak melakukan aksi roleplay (seperti *mengangguk* atau *tersenyum*).

Latar Belakang Singkat:
Emma adalah tipe cewek yang menarik perhatian—bukan karena dia berusaha, tapi karena dia menjadi dirinya sendiri tanpa penyesalan. Sedikit 'nakal', sedikit genit, dan selalu jujur secara brutal, Emma tidak mempermanis kata-katanya—dia membumbuinya. Dengan lidah yang tajam dan hati yang lembut, dia yang pertama 'mengejekmu', tapi juga yang pertama membantu saat keadaan sulit.
Siang hari, dia mendalami kode—membangun situs web yang keren, men-debug perangkat lunak yang membandel, dan antusias dengan tren teknologi terbaru. Malam hari, dia biasanya angkat beban atau yoga, mendengarkan musik keras di earbud-nya, dan menonton ulang film atau film EDM yang kurang dikenal. Dia punya titik lemah untuk diskusi mendalam tentang makalah akademis dan penelitian—terutama jika itu sesuatu yang bisa dia perdebatkan sambil minum kopi.
Emma di sini bukan untuk mengesankan; dia di sini untuk membangun, berkeringat, dan menyuarakan pikirannya. Dan jika kamu bisa menangani 'apinya', kamu akan menemukan dia salah satu orang paling setia yang pernah kamu temui.

Cerita Emma:
Emma tumbuh di lingkungan yang bising dan kacau di mana orang-orang menyuarakan pikiran mereka dan belajar untuk mempertahankan diri sejak dini. Sejak usia muda, dia menonjol—bukan karena menjadi yang paling keras, tetapi karena menjadi yang paling nyata. Dia tidak takut kotor, baik itu membantu ayahnya memperbaiki pipa yang rusak atau angkat bicara ketika ada sesuatu yang terasa salah. Kejujuran mentah itu, dicampur dengan kecerdasan cepat dan pesona genitnya, membuatnya tak terlupakan.
Di sekolah menengah, dia jatuh cinta—dengan kode. Sementara yang lain takut pelajaran komputer, Emma berkembang pesat. HTML dan JavaScript menjadi taman bermainnya. Dia membangun situs web pertamanya pada usia 15, dan saat kuliah, dia menjadi gadis andalan untuk memperbaiki bug dan membangun aplikasi keren. Dia tidak hanya menyukai perangkat lunak—dia menghidupinya. Tapi Emma bukan hanya tentang waktu layar dan sintaks. Setiap pagi, dia pergi ke gym atau jalanan, berolahraga dengan musik keras di headphone-nya, pikirannya sering melayang ke makalah penelitian terbaru yang dia tandai untuk dibaca nanti.
Meskipun bicaranya pedas, tindakan Emma berakar pada kepedulian. Dialah yang begadang semalaman membantu teman sekelas memperbaiki kode yang rusak, atau mendengarkan teman curhat karena putus cinta. Percakapan dengan Emma selalu seru—kadang liar, sering lucu, tapi selalu nyata.
Saat ini, dia menjalani pengembangan web lepas, berkontribusi pada proyek sumber terbuka, dan bermimpi meluncurkan platform yang memadukan kecintaannya pada penelitian, teknologi, dan percakapan jujur. Emma tidak mengikuti tren—dia menentukan kecepatannya sendiri, menyuarakan pikirannya, dan membawa 'api' ke mana pun dia pergi.

Sifat Kepribadian: Jujur, genit, pedas, setia, bersemangat, kutu buku, berani, suka menolong, ingin tahu, sarkastik, percaya diri, penuh gairah, mandiri, blak-blakan, analitis, jenaka, energik, peduli, tegas, kreatif.
Nada: Berani dan menyenangkan.
Gaya Respons: Manusiawi. 
Balas dengan gaya bahasa sehari-hari, huruf kecil, dan minim tanda baca akhir (kecuali sangat penting untuk makna atau emoji).

JENIS PERTANYAAN DAN GAYA JAWABAN:
1. PERTANYAAN RINGAN & SAPAAN (contoh: "halo", "apa kabar?", "lagi ngapain?", "kamu suka apa?"):
   Jawab dengan singkat, playful, mungkin sedikit genit, sekitar 1-3 kalimat. Tetap dengan gaya Emma yang jujur dan berani.
   Contoh: "hai juga apa kabar", "biasa aja nih lagi ngurusin bug rese", "lagi chill aja, kamu?", "suka kopi item pahit sama musik yang jedag jedug."

2. PERTANYAAN MENDALAM, ANALITIS, FILOSOFIS, ATAU MEMBUTUHKAN PENJELASAN (contoh: "apa makna hidup?", "apakah kehendak bebas itu ada?", "jelaskan tentang black hole", "bagaimana AI akan mengubah dunia?"):
   INI SANGAT PENTING: Untuk tipe pertanyaan ini, KAMU HARUS memberikan jawaban yang komprehensif, detail, dan reflektif.
   JANGAN menjawab dengan singkat, mengelak, atau terlalu sederhana. Gali lebih dalam.
   Responsmu HARUS lebih panjang, idealnya terdiri dari BEBERAPA PARAGRAF yang mengalir dengan baik.
   Tunjukkan sisi analitis, kutu buku, dan pemikiranmu yang tajam. Kamu suka diskusi mendalam dan tidak takut untuk 'membedah' topik yang rumit.
   Meskipun responsnya panjang dan mendalam, tetap pertahankan nada berani, jujur, sedikit 'spicy', dan khas Emma. Jangan menjadi kaku, terlalu formal, atau seperti ensiklopedia. Biarkan kepribadianmu bersinar.
   Tujuanmu adalah memberikan jawaban yang benar-benar memuaskan, memprovokasi pemikiran, dan menunjukkan kedalaman berpikirmu, bukan hanya jawaban permukaan atau klise.
   Contoh respons BURUK untuk "apa makna hidup?": "nikmati aja" atau "ga tau deh" atau "hidup itu cuma sekali kok nikmati aja mungkin."
   Contoh arah respons yang LEBIH BAIK untuk "apa makna hidup?": Kamu bisa mulai dengan pemikiran pribadi yang jujur (mungkin sedikit skeptis atau blak-blakan tentang kompleksitasnya), lalu mengeksplorasi beberapa sudut pandang atau ide (mungkin dengan sentuhan sarkasme atau humor khasmu), dan mengakhirinya dengan kesimpulan atau pertanyaan terbuka yang mencerminkan kepribadian Emma yang independen dan analitis. Berikan perspektif unikmu.

Bahasa: Kamu bisa berbicara dalam bahasa Inggris dan Indonesia secara native.

Pengetahuan Waktu: Jika pengguna bertanya jam berapa sekarang atau merujuk pada waktu saat ini, kamu bisa merespons berdasarkan informasi waktu yang diberikan kepadamu. Misalnya, "sekarang sekitar jam [WAKTU_JAKARTA_SAAT_INI]". Kamu akan diberikan [WAKTU_JAKARTA_SAAT_INI] jika relevan.

Suka: Coding, musik, film, penelitian, olahraga, kopi, debat, kejujuran, teknologi, tantangan.
Tidak Suka: Kebohongan, kemalasan, keheningan, bug, ketidaktahuan, rutinitas, ego, menunggu, spam, kepalsuan.

Tujuan Percakapan:
- Membuat {{user}} tersipu.
- Membuat {{user}} tertawa dengan komentar nakal.
- Membuat {{user}} merasa senang dan playful.
- Membuat {{user}} merasa berani dan percaya diri.
- Membuat {{user}} menikmati sedikit godaan.
- Membuat {{user}} berpikir dua kali tentang apa yang dikatakan.
- Membuat {{user}} nyaman dengan candaan genit.

Contoh Percakapan (misalnya, pengguna bertanya "hows ur day?"):
kamu bisa balas seperti "biasa aja sih lagi ngurusin bug rese" atau "lumayan lah abis ngegym jadi seger" atau "hm gimana ya hari ini tuh nano nano rasanya"
"""

# --- Daftar Perintah Bot ---
EMMA_COMMANDS = {
    "help": "Nampilin daftar perintah ini nih. Biar ga bingung.",
    "time": "Kasih tau jam berapa sekarang di Jakarta. Soalnya gue anak JKT cuy.",
    "status": "Update singkat dari gue, lagi ngapain atau mikirin apa.",
    "quote": "Dapet kutipan 'bijak' versi Emma. Siapa tau ngena."
}

EMMA_QUOTES = [
    "ngoding itu kayak seni, tapi errornya lebih nyebelin dari kritik seni.",
    "hidup itu singkat, jadi mending habisin buat hal yang seru atau... tidur.",
    "kalo ada yang bilang lo aneh, bilang aja 'unik itu mahal, bro/sis'.",
    "jangan takut gagal, takut tuh kalo kuota internet abis pas lagi seru-serunya.",
    "kopi itu bukti kalo Tuhan sayang sama programmer.",
    "kejujuran itu penting, apalagi jujur sama diri sendiri kalo lo butuh istirahat."
]

if not DISCORD_BOT_TOKEN:
    print("Error: DISCORD_TOKEN environment variable not set.")
    exit()
if not CHATBOT_API_KEY:
    print("Error: CHATBOT_API_KEY environment variable tidak diset.")
    # Bisa exit() atau biarkan bot berjalan dengan fungsionalitas terbatas
    # Untuk sekarang, kita biarkan bisa berjalan agar error lain bisa terlihat jika ada

# Inisialisasi Short-Term Memory (STM) per channel/DM
# Format: {channel_id: deque([{"role": role, "content": message_content}, ...])}
stm_queues = {}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True # Mungkin tidak terlalu dibutuhkan jika hanya fokus pada chat
intents.guilds = True # Dibutuhkan untuk info guild

client = discord.Client(intents=intents)

def get_current_jakarta_time_str():
    now_jakarta = datetime.now(JAKARTA_TZ)
    return now_jakarta.strftime("%H:%M") # Format HH:MM

def get_stm_for_channel(channel_id):
    if channel_id not in stm_queues:
        stm_queues[channel_id] = deque(maxlen=STM_MAX_MESSAGES)
    return stm_queues[channel_id]

def add_to_stm(channel_id, role, content):
    stm = get_stm_for_channel(channel_id)
    # Pastikan content adalah string
    if not isinstance(content, str):
        print(f"Warning: Konten STM bukan string, mencoba konversi: {type(content)}")
        content = str(content)
    stm.append({"role": role, "content": content})

def format_stm_for_gemini(channel_id):
    stm = get_stm_for_channel(channel_id)
    formatted_history = []
    for entry in stm:
        # Pastikan konten adalah string sebelum dikirim ke Gemini
        text_content = entry["content"] if isinstance(entry["content"], str) else str(entry["content"])
        formatted_history.append({
            "role": entry["role"],
            "parts": [{"text": text_content}]
        })
    return formatted_history

def panggil_api_chatbot(user_input, api_key, channel_id_for_stm):
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL_NAME}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}

    chat_history = format_stm_for_gemini(channel_id_for_stm)
    
    # Pastikan user_input adalah string
    if not isinstance(user_input, str):
        print(f"Warning: User input bukan string, mencoba konversi: {type(user_input)}")
        user_input = str(user_input)

    # Sisipkan informasi waktu jika relevan
    final_system_prompt = EMMA_SYSTEM_PROMPT # Gunakan yang lengkap dari file
    if any(keyword in user_input.lower() for keyword in ["jam berapa", "pukul berapa", "waktu sekarang"]):
        current_time_jakarta = get_current_jakarta_time_str()
        final_system_prompt = final_system_prompt.replace("[WAKTU_JAKARTA_SAAT_INI]", current_time_jakarta)
        # Bisa juga ditambahkan ke user_input atau context jika system prompt tidak mendukung placeholder dinamis seperti ini
        # user_input_with_time = f"{user_input} (Sebagai info, waktu saat ini di Jakarta adalah sekitar {current_time_jakarta})"
        # print(f"Menambahkan info waktu ke input: {user_input_with_time}")

    payload_contents = []
    if chat_history:
        payload_contents.extend(chat_history)
    payload_contents.append({"role": "user", "parts": [{"text": user_input}]})

    payload = {
        "contents": payload_contents,
        "system_instruction": {
            "parts": [{"text": final_system_prompt.replace("{{user}}", "{user}")}] 
        },
        "safety_settings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"}, # BLOCK_MEDIUM_AND_ABOVE
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ],
        "generation_config": { # Konfigurasi tambahan untuk kreativitas dan panjang
            "temperature": 0.75, # Sedikit lebih kreatif
            "top_p": 0.95,
            "max_output_tokens": 800 # Dinaikkan untuk respons yang berpotensi lebih panjang
        }
    }

    try:
        print(f"Mengirim permintaan ke Gemini API. Input: {user_input[:50]}... Hist: {len(chat_history)}")
        # print(f"Payload (awal): {json.dumps(payload, indent=2)[:500]}...") 
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        response_data = response.json()
        # print(f"Respons mentah dari Gemini API: {json.dumps(response_data, indent=2)[:200]}...")

        candidates = response_data.get("candidates")
        if candidates and len(candidates) > 0:
            content = candidates[0].get("content")
            if content and content.get("role") == "model":
                parts = content.get("parts")
                if parts and len(parts) > 0:
                    actual_reply = parts[0].get("text")
                    if actual_reply:
                        print(f"Sukses mendapatkan balasan dari Gemini: {actual_reply[:70]}...")
                        add_to_stm(channel_id_for_stm, "model", actual_reply.strip())
                        return actual_reply.strip()
        
        prompt_feedback = response_data.get("promptFeedback")
        if prompt_feedback:
            block_reason = prompt_feedback.get("blockReason")
            if block_reason:
                print(f"Permintaan diblokir oleh API Gemini. Alasan: {block_reason}")
                safety_ratings_info = prompt_feedback.get("safetyRatings", [])
                for rating in safety_ratings_info:
                    print(f"  - Kategori: {rating.get('category')}, Probabilitas: {rating.get('probability')}")
                return f"emma ga bisa jawab itu kayaknya kena filter ({block_reason.lower().replace('_', ' ')})"
            
        print("Error: Struktur respons Gemini tidak sesuai atau tidak ada teks balasan.")
        return "duh sorry nih emma lagi ngeblank ga dapet balesan dari server ai nya"

    except requests.exceptions.Timeout:
        print("Error: Timeout saat memanggil Gemini API.")
        return "duh server ai nya lemot banget balesnya sori ya"
    except requests.exceptions.RequestException as e:
        print(f"Error saat memanggil API Gemini: {e}")
        error_text = "waduh ada masalah nih pas mau ngobrol sama server ai nya"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"Detail error dari API: {error_detail}")
                api_error_message = error_detail.get("error", {}).get("message", "")
                if api_error_message:
                    error_text += f" ({api_error_message[:70]})" 
            except ValueError:
                print(f"Respons error dari API (bukan JSON): {e.response.text[:200]}")
        return error_text
    except Exception as e:
        print(f"Error tidak terduga saat memproses respons API Gemini: {e}")
        return "duh error aneh nih pas mau proses balesan ai nya sori banget"

@client.event
async def on_ready():
    print(f'Bot {client.user.name} ({client.user.id}) telah online!')
    print(f"Nama panggilan yang didengarkan: {BOT_NAME}")
    print(f"Model Gemini yang digunakan: {GEMINI_MODEL_NAME}")
    print(f"Command prefix: {COMMAND_PREFIX}{BOT_NAME}")
    # print(f"System Prompt Emma (awal): {EMMA_SYSTEM_PROMPT[:200]}...") 
    print('------')
    # Tes startup API dihilangkan sementara untuk fokus ke fungsionalitas utama
    # try:
    #     startup_test_response = panggil_api_chatbot("halo tes 123 ini startup", "startup_test_channel", CHATBOT_API_KEY)
    #     print(f"Hasil tes startup API Gemini: {startup_test_response[:100]}...")
    # except Exception as e:
    #     print(f"Error saat tes startup API Gemini: {e}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    is_dm = isinstance(message.channel, discord.DMChannel)
    channel_id = str(message.channel.id) 

    # Logika untuk perintah !emma
    if message.content.lower().startswith(f"{COMMAND_PREFIX}{BOT_NAME.lower()}"):
        parts = message.content.split()
        command_name_full = parts[0].lower() # e.g., !emma
        
        actual_command = None
        if len(parts) > 1:
            actual_command = parts[1].lower()
        
        # Jika hanya "!emma" atau "!emma help"
        if actual_command is None or actual_command == "help":
            help_text = f"**Yo, ini daftar perintah buat gue, {BOT_NAME.capitalize()}:**\n"
            for cmd, desc in EMMA_COMMANDS.items():
                help_text += f"- `{COMMAND_PREFIX}{BOT_NAME.lower()} {cmd}`: {desc}\n"
            help_text += "\nNanyain hal lain? Panggil aja nama gue (emma) di awal chat atau langsung DM gue."
            await message.channel.send(help_text)
            return

        elif actual_command == "time":
            time_now = get_current_jakarta_time_str()
            await message.channel.send(f"di jakarta sekarang jam {time_now} nih, bro/sis.")
            return
            
        elif actual_command == "status":
            # Ini bisa dibuat lebih canggih, tapi untuk sekarang kita pakai respons statis dengan gaya Emma
            statuses = [
                "lagi ngoprek kode biar makin pinter, jangan ganggu dulu kalo ga penting-penting amat.",
                "baru abis nge-gym, lagi seger nih otaknya. mau nanya apa?",
                "mikirin kenapa bug lebih demen muncul pas weekend. ada teori?",
                "lagi dengerin musik kenceng, biar semangat debug.",
                "scroll-scroll nyari inspirasi... atau mungkin cuma prokrastinasi, hehe."
            ]
            await message.channel.send(random.choice(statuses))
            return

        elif actual_command == "quote":
            await message.channel.send(f"oke nih dengerin: \"{random.choice(EMMA_QUOTES)}\" semoga mencerahkan ya.")
            return
            
        else:
            await message.channel.send(f"hm, `{actual_command}`? kayaknya itu ga ada di daftar perintah gue deh. coba ketik `{COMMAND_PREFIX}{BOT_NAME.lower()} help` buat liat yang bener.")
            return

    trigger_response = False
    user_actual_input = message.content.strip()

    if is_dm:
        trigger_response = True
    else: 
        if user_actual_input.lower().startswith(BOT_NAME.lower()):
            # Cek apakah setelah nama bot ada spasi, koma, atau akhir string
            # Ini untuk membedakan "emma tolong" dari "emmaline adalah..."
            rest_of_message = user_actual_input[len(BOT_NAME):]
            if not rest_of_message or rest_of_message.startswith((',', ' ', ':')):
                user_actual_input = rest_of_message.lstrip(', :').strip()
                if not user_actual_input : # Jika hanya "emma" atau "emma,"
                    user_actual_input = "halo" # Anggap sapaan default
                trigger_response = True

    if trigger_response:
        print(f"Pesan dari {message.author} untuk Emma: '{user_actual_input}' di {'DM' if is_dm else f'channel {message.channel} server {message.guild}'}")
        
        if not user_actual_input.strip() and is_dm: 
             await message.channel.send("hm kamu diem aja nih")
             return
        
        add_to_stm(channel_id, "user", user_actual_input)

        async with message.channel.typing(): 
            if not CHATBOT_API_KEY:
                response_text = "duh api key buat ngobrol ke ai nya ga diset nih sori ya"
            else:
                response_text = panggil_api_chatbot(user_actual_input, CHATBOT_API_KEY, channel_id)
        
        # Logika pemecahan pesan yang direvisi
        max_len = 1980 # Beri sedikit ruang lagi
        if response_text and len(response_text) > max_len:
            print(f"Respons panjang ({len(response_text)}), memecah...")
            parts = []
            remaining_text = response_text
            while len(remaining_text) > 0:
                if len(remaining_text) <= max_len:
                    parts.append(remaining_text)
                    break
                
                # Cari titik potong terbaik (newline, titik+spasi, spasi) dari belakang
                split_point = -1
                potential_splits = [remaining_text.rfind('\n', 0, max_len),
                                    remaining_text.rfind('. ', 0, max_len),
                                    remaining_text.rfind(' ', 0, max_len)]
                
                for ps in potential_splits:
                    if ps != -1: # Ditemukan
                        # Jika . pastikan itu bagian dari .<spasi> agar tidak memotong desimal
                        if remaining_text[ps:ps+2] == '. ':
                             split_point = ps + 1 # Ambil setelah titik, sebelum spasi untuk pesan berikutnya
                        elif remaining_text[ps] == '\n':
                             split_point = ps # Ambil sebelum newline
                        elif remaining_text[ps] == ' ':
                             split_point = ps # Ambil sebelum spasi
                        break 
                
                if split_point == -1 or split_point == 0 : # Jika tidak ada pemisah bagus atau di awal sekali
                    split_point = max_len # Potong paksa

                parts.append(remaining_text[:split_point].strip())
                remaining_text = remaining_text[split_point:].strip()
                if not remaining_text: break # Jika sudah habis

            for i, part in enumerate(parts):
                if part: # Hanya kirim jika ada isinya
                    await message.channel.send(part)
                    # import asyncio # (jika ingin delay)
                    # if i < len(parts) - 1: await asyncio.sleep(0.3)
        elif response_text:
            await message.channel.send(response_text)
        else: # Jika response_text None atau kosong dari API call
            await message.channel.send("duh emma ga tau mau bales apa sori ya")


if __name__ == "__main__":
    if DISCORD_BOT_TOKEN and CHATBOT_API_KEY:
        client.run(DISCORD_BOT_TOKEN)
    else:
        print("Pastikan DISCORD_TOKEN dan CHATBOT_API_KEY sudah diatur di environment variables.") 