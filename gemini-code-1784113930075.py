  elif data == "format_unban":
        format_teks = (
            "📋 **FORMAT PENGADUAN UNMUTE/UNBAN**\n\n"
            "Silakan salin (klik) teks di bawah ini:\n\n"
            "`Nama Akun: \n"
            "Username/ID: \n"
            "Alasan Terkena Banned/Mute: \n"
            "Penjelasan Mengapa Harus Dibuka: `\n\n"
            "Setelah diisi, kirimkan langsung di sini ya!"
        )
        await callback_query.message.reply_text(format_teks)
        await callback_query.answer()

    elif data == "format_lapor":
        format_teks = (
            "📢 **FORMAT LAPORAN PELANGGARAN**\n\n"
            "Silakan salin (klik) teks di bawah ini:\n\n"
            "`Nama Pelaku: \n"
            "Username/ID Pelaku: \n"
            "Jenis Pelanggaran: \n"
            "Bukti (Screenshot/Link): `\n\n"
            "Setelah diisi, kirimkan langsung di sini ya!"
        )
        await callback_query.message.reply_text(format_teks)
        await callback_query.answer()          
