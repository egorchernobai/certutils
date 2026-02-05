import subprocess
import sys
import os
import requests

def is_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
def download_certificate(url):
    temp_dir = os.environ.get("TEMP")
    save_path = os.path.join(temp_dir, "tls.crt")
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, "wb") as f:
        f.write(response.content)
    return save_path


if not is_admin():
    print("❌ Запустите скрипт от имени администратора")
    input("Нажмите Enter для выхода...")
else:
    try:
        save_path = download_certificate('https://cdp.rospotrebnadzor.ru/cdp/cdp/tls.crt')
    except Exception as e:
        print("Ошибка загрузки сертификата:", e)
        input("Нажмите Enter для выхода...")
        sys.exit(1)
        
    try:
        if save_path:
            subprocess.check_call([
                "certutil",
                "-addstore",
                "Root",
                save_path
            ])
            os.system("cls")
            print("✅ Корневой сертификат успешно установлен")
            print("Перезапустите браузер, чтобы изменения вступили в силу.")
            input("Нажмите Enter для выхода...")
    except Exception as e:
        print("Ошибка установки:", e)
        input("Нажмите Enter для выхода...")