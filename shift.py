import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QInputDialog

class Calisan:
    def __init__(self, isim, cinsiyet, pozisyon, izin_hakki=1, vardiya=None):
        self.isim = isim
        self.cinsiyet = cinsiyet
        self.pozisyon = pozisyon
        self.izin_hakki = izin_hakki
        self.vardiya = vardiya

class VardiyaUygulamasi(QWidget):
    def __init__(self):
        super().__init__()

        self.calisanlar = self.load_calisanlar()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Haftalık Vardiya Sistemi')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.label = QLabel('Çalışanlar:')
        self.layout.addWidget(self.label)

        self.calisan_table = QTableWidget()
        self.layout.addWidget(self.calisan_table)

        self.izın_ve_saat_ayarla_button = QPushButton('İzin ve Çalışma Saatleri Ayarla')
        self.izın_ve_saat_ayarla_button.clicked.connect(self.izin_ve_saat_ayarla)
        self.layout.addWidget(self.izın_ve_saat_ayarla_button)

        self.setLayout(self.layout)

        self.update_calisan_table()

    def load_calisanlar(self):
        try:
            with open('calisanlar.json', 'r') as file:
                calisanlar_data = json.load(file)
                return [Calisan(**calisan) for calisan in calisanlar_data]
        except FileNotFoundError:
            return []

    def update_calisan_table(self):
        self.calisan_table.setRowCount(len(self.calisanlar))
        self.calisan_table.setColumnCount(4)  # İsim, Cinsiyet, Pozisyon, İzin Hakkı

        header_labels = ['İsim', 'Cinsiyet', 'Pozisyon', 'İzin Hakkı']
        self.calisan_table.setHorizontalHeaderLabels(header_labels)

        for row, calisan in enumerate(self.calisanlar):
            self.calisan_table.setItem(row, 0, QTableWidgetItem(calisan.isim))
            self.calisan_table.setItem(row, 1, QTableWidgetItem(calisan.cinsiyet))
            self.calisan_table.setItem(row, 2, QTableWidgetItem(calisan.pozisyon))
            izin_hakki_item = QSpinBox()
            izin_hakki_item.setValue(calisan.izin_hakki)
            self.calisan_table.setCellWidget(row, 3, izin_hakki_item)

    def izin_ve_saat_ayarla(self):
        for calisan in self.calisanlar:
            vardiya_bilgileri = [['' for _ in range(8)] for _ in range(25)]  # 8 gün, 25 saat
            vardiya_secimi, ok_pressed = QInputDialog.getItem(self, 'Vardiya Seçimi', f'{calisan.isim} için vardiya seçimi:', 
                                                          ('Sabahçı', 'Akşamcı', 'Aracı', 'İzinli'))
        if ok_pressed:
            if vardiya_secimi == 'İzinli':
                vardiya_bilgileri[0][0] = 'İzinli'
            else:
                gunler = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
                saat_araligi = self.belirli_saat_araligi(calisan.pozisyon, vardiya_secimi)
                for gun_index, gun in enumerate(gunler):
                    vardiya_bilgileri[0][gun_index + 1] = gun
                    vardiya_bilgileri[1][gun_index + 1] = saat_araligi

            calisan.vardiya = vardiya_bilgileri

        self.update_calisan_table()
        self.update_vardiya_table()



    def belirli_saat_araligi(self, calisan_tipi, vardiya_tipi):
        if calisan_tipi == 'Garson':
            if vardiya_tipi == 'Sabahçı':
                return '10.00-19.00'
            elif vardiya_tipi == 'Akşamcı':
                return '15.00-00.00'
        elif calisan_tipi == 'Barista':
            if vardiya_tipi == 'Sabahçı':
                return '08.00-17.00'
            elif vardiya_tipi == 'Akşamcı':
                return '15.00-00.00'
        elif calisan_tipi == 'Aracı':
            # Burada istediğiniz gibi saat aralıklarını belirleyebilirsiniz
            saat_araligi, ok_pressed = QInputDialog.getText(None, 'Saat Aralığı', 'Çalışma saat aralığını belirle:')
            if ok_pressed:
                return saat_araligi
        else:
            return 'Belirtilmemiş'

    def update_vardiya_table(self):
    # Tablo oluştur
        vardiya_table = QTableWidget()
        vardiya_table.setColumnCount(9)  # İsim, Pazartesi, Salı, Çarşamba, Perşembe, Cuma, Cumartesi, Pazar, Çalışma Saatleri
        vardiya_table.setHorizontalHeaderLabels(['İsim', 'Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar', 'Çalışma Saatleri'])

    # Çalışanların vardiya bilgilerine göre tabloyu doldur
        for calisan in self.calisanlar:
            vardiya_table.insertRow(vardiya_table.rowCount())
            vardiya_table.setItem(vardiya_table.rowCount() - 1, 0, QTableWidgetItem(calisan.isim))
        for satir in range(1, 25):
            for sutun in range(8):
                vardiya_table.setItem(vardiya_table.rowCount() - 1, sutun + 1, QTableWidgetItem(calisan.vardiya[satir][sutun]))

    # Eğer daha önce bir tablo varsa kapat
        if hasattr(self, 'vardiya_table_widget'):
            self.layout.removeWidget(self.vardiya_table_widget)
            self.vardiya_table_widget.deleteLater()

    # Oluşturulan tabloyu uygulamaya ekle
        self.vardiya_table_widget = vardiya_table
        self.layout.addWidget(self.vardiya_table_widget)


def run_app():
    app = QApplication(sys.argv)
    uygulama = VardiyaUygulamasi()
    uygulama.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run_app()
