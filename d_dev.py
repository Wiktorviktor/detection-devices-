import usb.core
import usb.util
import time
import socket

# Файл для логування підключених пристроїв
LOG_FILE = "device_log.txt"

# Список довірених клавіатур
trusted_devices = {
    "046d:c31c",  # Logitech Keyboard
    "04D9:0169",  # Generic Keyboard
    "1A2C:2124",  # Trust Keyboard
}

# Пароль для додавання нових пристроїв
ADMIN_PASSWORD = "secure123"

def log_device(device_id):
    """Записує підключення пристрою в лог-файл"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    ip_address = get_ip_address()

    with open(LOG_FILE, "a") as file:
        file.write(f"{timestamp} | VID:PID: {device_id} | IP: {ip_address}\n")

    print(f"[] Лог записано: {device_id} | {timestamp} | IP: {ip_address}")

def get_ip_address():
    """Отримує локальну IP-адресу"""
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except:
        ip = "Немає IP"
    return ip

def get_usb_keyboards():
    """Отримує список підключених клавіатур за VID:PID"""
    devices = usb.core.find(find_all=True)
    keyboard_list = []

    for device in devices:
        vid_pid = f"{device.idVendor:04X}:{device.idProduct:04X}"
        keyboard_list.append(vid_pid)

    return keyboard_list

def authorize_new_device(device_id):
    """Запитує пароль для дозволу нового пристрою"""
    user_input = input(f"[!] Виявлено нову клавіатуру {device_id}. Введіть пароль для дозволу: ")
    if user_input == ADMIN_PASSWORD:
        trusted_devices.add(device_id)
        print(f"[] Пристрій {device_id} додано до списку довірених!")
        log_device(device_id)  # Логування підключення
    else:
        print("[] Невірний пароль! Пристрій залишається заблокованим.")

def check_keyboards():
    """Перевіряє, чи є підозрілі клавіатури"""
    detected_keyboards = get_usb_keyboards()

    for keyboard in detected_keyboards:
        if keyboard not in trusted_devices:
            authorize_new_device(keyboard)
        else:
            print(f"[+] Довірена клавіатура знайдена: {keyboard}")
            log_device(keyboard)  # Логування підключення

def main():
    """Головна функція"""
    print(" Моніторинг клавіатури запущено. Натисніть Ctrl+C для виходу.")

    try:
        while True:
            check_keyboards()
            time.sleep(5)  # Оновлення кожні 5 секунд
    except KeyboardInterrupt:
        print("\n Моніторинг завершено.")

if __name__ == "__main__":
    main()
