import hashlib
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

# Hash algoritması
hash_alg = hashlib.sha512()

# FIM klasörü yolunu belirleyin
fim_path = "FIM"

# Hash değerlerinin kaydedileceği dosya adı
output_file = "hashes.txt"

# Dosya açma modu: "wb" (write binary)
with open(output_file, "wb") as output:

    # FIM klasöründeki dosyaların hash değerlerini hesaplayan işlev
    def calculate_hashes(filename=None):
        # Dosyanın adı verildiyse sadece o dosyanın hash değerini hesaplayın
        if filename:
            file_path = os.path.join(fim_path, filename)
            try:
                # Dosya içeriğini okuyun ve hash değerini hesaplayın
                with open(file_path, "rb") as f:
                    file_data = f.read()
                    hash_alg.update(file_data)
                # Hash değerini dosyaya yazın
                output.write(f"{filename}: {hash_alg.hexdigest()}\n".encode())
            except IOError:
                pass
        else:
            # Tüm dosyaların hash değerlerini hesaplayın
            for dirpath, dirnames, filenames in os.walk(fim_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    try:
                        # Dosya içeriğini okuyun ve hash değerini hesaplayın
                        with open(file_path, "rb") as f:
                            file_data = f.read()
                            hash_alg.update(file_data)
                        # Hash değerini dosyaya yazın
                        output.write(f"{filename}: {hash_alg.hexdigest()}\n".encode())
                        print(f"\033[32m{filename} dosyası oluşturuldu.\033[0m")
                    except IOError:
                        pass

    # Dosya sistemindeki değişiklikleri işleyen sınıf
    class FileChangeHandler(FileSystemEventHandler):
        def on_any_event(self, event: FileSystemEvent):
            if event.is_directory:
                pass
            else:
                if event.event_type == 'created':
                    print(f"\033[32m{event.src_path} dosyası oluşturuldu.\033[0m")
                elif event.event_type == 'modified':
                    print(f"\033[31m{event.src_path} dosyası değiştirildi.\033[0m")
                elif event.event_type == 'deleted':
                    print(f"\033[31m{event.src_path} dosyası silindi.\033[0m")
                calculate_hashes(os.path.basename(event.src_path))

    # Dosya sistemi olay gözlemcisi
    observer = Observer()
    event_handler = FileChangeHandler()
    observer.schedule(event_handler, fim_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
