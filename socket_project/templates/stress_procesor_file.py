import threading

def stress_cpu():
    while True:
        pass  # Бесконечная нагрузка на процессор

def stress_memory():
    large_list = []
    while True:
        large_list.append(" " * 10**6)  # Постоянное увеличение памяти

def file_bomb():
    i = 0
    while True:
        with open(f"test_file_{i}.txt", "w") as f:
            f.write("Очень много данных...\n" * 1000)  # Создает файл с большим объемом данных
        i += 1

threads = []

# Создание потоков для нагрузки на процессор
for _ in range(5):
    thread = threading.Thread(target=stress_cpu)
    threads.append(thread)
    thread.start()

# Создание потоков для нагрузки на память
for _ in range(2):
    thread = threading.Thread(target=stress_memory)
    threads.append(thread)
    thread.start()

# Создание отдельного потока для засорения файловой системы
file_thread = threading.Thread(target=file_bomb)
threads.append(file_thread)
file_thread.start()

# Ожидание завершения потоков (они никогда не завершатся)
for thread in threads:
    thread.join()