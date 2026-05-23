import requests
from PyQt5 import QtWidgets, QtGui


def get_ip_info(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
        response = requests.get(url)
        data = response.json()
        if data.get("status") == "fail":
            raise ValueError("Ошибка получения информации о IP.")
        return data
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Ошибка сети: {e}")
    except ValueError as e:
        raise e
    except Exception as e:
        raise ValueError(f"Неизвестная ошибка: {e}")


def get_exact_location(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        response = requests.get(url)
        data = response.json()
        if data.get("address"):
            return data["address"]
        else:
            return None
    except Exception as e:
        return None


class IPInfoApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Поиск информации по IP")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setGeometry(100, 100, 500, 500)

        layout = QtWidgets.QVBoxLayout()

        self.label_ip = QtWidgets.QLabel("Введите IP-адрес:", self)
        self.label_ip.setFont(QtGui.QFont("Arial", 12))
        layout.addWidget(self.label_ip)

        self.entry_ip = QtWidgets.QLineEdit(self)
        self.entry_ip.setFont(QtGui.QFont("Arial", 12))
        self.entry_ip.setPlaceholderText("например, 8.8.8.8")
        layout.addWidget(self.entry_ip)

        self.btn_get_info = QtWidgets.QPushButton("Получить информацию", self)
        self.btn_get_info.setFont(QtGui.QFont("Arial", 12))
        self.btn_get_info.clicked.connect(self.show_ip_info)
        self.btn_get_info.setStyleSheet("background-color: #4CAF50; color: white;")
        layout.addWidget(self.btn_get_info)

        self.result_text = QtWidgets.QTextEdit(self)
        self.result_text.setFont(QtGui.QFont("Arial", 10))
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("background-color: #f0f0f0;")
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def show_ip_info(self):
        ip = self.entry_ip.text()
        if ip:
            try:
                ip_info = get_ip_info(ip)
                result = (f"Страна: {ip_info['country']}\n"
                          f"Код страны: {ip_info['countryCode']}\n"
                          f"Регион: {ip_info['regionName']}\n"
                          f"Город: {ip_info['city']}\n"
                          f"Почтовый индекс: {ip_info['zip']}\n"
                          f"Широта: {ip_info['lat']}\n"
                          f"Долгота: {ip_info['lon']}\n"
                          f"Часовой пояс: {ip_info['timezone']}\n"
                          f"Поставщик интернета (ISP): {ip_info['isp']}\n"
                          f"Организация: {ip_info['org']}\n"
                          f"AS номер: {ip_info['as']}\n"
                          f"IP адрес: {ip_info['query']}")

                location = get_exact_location(ip_info['lat'], ip_info['lon'])
                if location:
                    result += f"\nТочное местоположение: {location.get('road', '')}, {location.get('city', '')}, {location.get('country', '')}"

                self.result_text.setText(result)
            except ValueError as e:
                self.result_text.setText(f"Ошибка: {e}")
            except Exception as e:
                self.result_text.setText(f"Произошла ошибка: {e}")
        else:
            self.result_text.setText("Пожалуйста, введите корректный IP-адрес.")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = IPInfoApp()
    window.show()
    app.exec_()