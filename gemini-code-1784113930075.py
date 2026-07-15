import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# === KONFIGURASI BOT ===
BOT_TOKEN = "8637397466:AAG1LdUrAjQjsDcqzilvibVRxe4bt3AFv-s"
API_ID = 1234567        
API_HASH = "your_api_hash_here" 

# ID Grup Admin Anda (Sudah ditambahkan -100)
ADMIN_GROUP_ID = -1004468794471 

app = Client("desire_report_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

reports_db = {}

@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    teks = (
        "✨ **Selamat datang di Bot Pengaduan DESIREPROMOTE!** ✨\n\n"
        "Bot ini berfungsi khusus untuk melayani aduan member mengenai:\n"
        "• Pengajuan Unmute / Unban\n"
        "• Melaporkan member yang melanggar rules di LPM\n"
        "• Kendala teknis lainnya\n\n"
        "Silakan ketik dan kirimkan aduan/laporan Anda langsung di sini. "
        "Sertakan bukti berupa username/ID pelaku atau screenshot jika ada."
    )
    await message.reply_text(teks)

@app.on_message(filters.private & ~filters.command("start"))
async def handle_report(client, message):
    user = message.from_user
    user_info = f"👤 **Pengadu:** {user.mention} (ID: `{user.id}`)\n"
    if user.username:
        user_info += f"🔗 **Username:** @{user.username}\n"
    
    report_text = f"🚨 **LAPORAN BARU MASUK - DESIREPROMOTE** 🚨\n\n{user_info}\n"
    
    if message.text:
        report_text += f"📝 **Isi Aduan:**\n{message.text}"
    else:
        report_text += f"📝 **Isi Aduan:** (Mengirimkan Media/Gambar - Lihat di bawah)"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Balas Pengadu 💬", callback_data=f"reply_{user.id}"),
            InlineKeyboardButton("Selesai ✅", callback_data=f"resolve_{user.id}")
        ]
    ])

    if message.text:
        sent_msg = await client.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=report_text,
            reply_markup=keyboard
        )
    else:
        sent_msg = await message.copy(
            chat_id=ADMIN_GROUP_ID,
            caption=report_text,
            reply_markup=keyboard
        )

    reports_db[sent_msg.id] = user.id

    await message.reply_text(
        "✅ **Laporan Anda telah terkirim ke Staff DESIREPROMOTE.**\n"
        "Mohon tunggu sebentar, staff kami akan segera memeriksa aduan Anda."
    )

@app.on_callback_query()
async def handle_callback(client, callback_query: CallbackQuery):
    data = callback_query.data
    admin = callback_query.from_user
    
    if data.startswith("reply_"):
        await callback_query.answer("Ketik balasannya dengan membalas (reply) pesan laporan ini di grup!", show_alert=True)
        
    elif data.startswith("resolve_"):
        target_user_id = int(data.split("_")[1])
        try:
            await client.send_message(
                chat_id=target_user_id,
                text="📢 **Aduan Anda di DESIREPROMOTE telah selesai diproses oleh Staff/Admin.**\nTerima kasih!"
            )
        except Exception:
            pass
            
        await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"Selesai oleh {admin.first_name} ✅", callback_data="done")]
            ])
        )
        await callback_query.answer("Laporan ditandai selesai!")

@app.on_message(filters.chat(ADMIN_GROUP_ID) & filters.reply)
async def reply_to_member(client, message):
    reply_to_msg_id = message.reply_to_message.id
    
    if reply_to_msg_id in reports_db:
        member_id = reports_db[reply_to_msg_id]
        try:
            if message.text:
                await client.send_message(
                    chat_id=member_id,
                    text=f"💬 **Balasan dari Admin DESIREPROMOTE:**\n\n{message.text}"
                )
            else:
                await message.copy(chat_id=member_id)
                
            await message.reply_text("✅ Balasan berhasil terkirim ke member di chat pribadi.")
        except Exception as e:
            await message.reply_text(f"❌ Gagal mengirim balasan. Eror: {e}")

if __name__ == "__main__":
    print("Bot DESIREPROMOTE Pengaduan sedang berjalan...")
    app.run()