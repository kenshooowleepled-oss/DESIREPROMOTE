import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# === KONFIGURASI BOT ===
BOT_TOKEN = "8637397466:AAHydzLtKp90TGtkwWsmhawkPYUlTrHfo1Q"
API_ID = 1234567        # Pastikan Anda isi dengan angka API_ID Anda
API_HASH = "your_api_hash_here" # Pastikan isi dengan API_HASH Anda

ADMIN_GROUP_ID = -1004468794471 

app = Client("desire_report_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

reports_db = {}

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    teks = (
        "✨ **Selamat datang di Bot Pengaduan DESIREPROMOTE!** ✨\n\n"
        "Silakan pilih menu di bawah untuk mendapatkan format pengaduan:"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔓 Format Unmute/Unban", callback_data="format_unban")],
        [InlineKeyboardButton("🚨 Format Lapor Pelanggaran", callback_data="format_lapor")]
    ])
    await message.reply_text(teks, reply_markup=keyboard)

@app.on_callback_query()
async def handle_callback(client, callback_query: CallbackQuery):
    data = callback_query.data
    
    if data == "format_unban":
        format_teks = (
            "📋 **FORMAT PENGADUAN UNMUTE/UNBAN**\n\n"
            "Klik teks di bawah untuk menyalin:\n\n"
            "`Nama Akun: \n"
            "Username/ID: \n"
            "Alasan Terkena Banned/Mute: \n"
            "Penjelasan Mengapa Harus Dibuka: `\n\n"
            "Setelah disalin dan diisi, kirimkan langsung di sini ya!"
        )
        await callback_query.message.reply_text(format_teks)
        await callback_query.answer()

    elif data == "format_lapor":
        format_teks = (
            "📢 **FORMAT LAPORAN PELANGGARAN**\n\n"
            "Klik teks di bawah untuk menyalin:\n\n"
            "`Nama Pelaku: \n"
            "Username/ID Pelaku: \n"
            "Jenis Pelanggaran: \n"
            "Bukti (Screenshot/Link): `\n\n"
            "Setelah disalin dan diisi, kirimkan langsung di sini ya!"
        )
        await callback_query.message.reply_text(format_teks)
        await callback_query.answer()

    # Logika untuk tombol admin (Reply/Resolve)
    elif data.startswith("reply_"):
        await callback_query.answer("Ketik balasannya dengan membalas (reply) pesan laporan ini di grup!", show_alert=True)
    elif data.startswith("resolve_"):
        await callback_query.answer("Laporan ditandai selesai!")

# Logika penerimaan laporan tetap sama agar masuk ke grup Admin
@app.on_message(filters.private & ~filters.command("start"))
async def handle_report(client, message):
    user = message.from_user
    # ... (Logika kirim laporan ke grup admin tetap sama seperti sebelumnya)
    # Anda bisa menyalin kembali bagian handle_report dari kode Anda yang lama di sini
    await message.reply_text("✅ Laporan Anda telah diterima staff kami.")

if __name__ == "__main__":
    app.run()
