import os
import re
import sys # sys modülünü import etmeyi unutmayın

def get_latest_vit_folder(root_base_path): # Argüman adını daha açıklayıcı yaptım
    # root_base_path şimdi PyInstaller'dan gelen _MEIPASS veya uygulamanın kök dizini olacak.
    # data klasörünün yolunu oluştur
    data_folder_path = os.path.join(root_base_path, "data")

    if not os.path.isdir(data_folder_path):
        raise FileNotFoundError(f"Data klasörü bulunamadı: {data_folder_path}")

    vit_folders = []
    for name in os.listdir(data_folder_path): # data_folder_path'i kullanın
        match = re.match(r"VIT(\d+)", name)
        if match:
            vit_folders.append((int(match.group(1)), name))

    if not vit_folders:
        raise FileNotFoundError("Hiçbir VIT klasörü bulunamadı.")

    latest_vit_folder = max(vit_folders, key=lambda x: x[0])[1]
    latest_vit_path = os.path.join(data_folder_path, latest_vit_folder) # data_folder_path'i kullanın

    return latest_vit_path

def get_excel_files_from_latest_vit(app_root_path): # app_root_path'i parametre olarak alacak!
    """
    Uygulama kök yolu altındaki 'data' klasöründe bulunan en yeni VITx klasörünü bulur
    ve içindeki Basvurular.xlsx, Mentor.xlsx, Mulakatlar.xlsx dosyalarının yollarını döndürür.
    """
    
    # data klasörünün tam yolunu oluştur
    data_folder_path = os.path.join(app_root_path, "data")

    if not os.path.isdir(data_folder_path):
        # Uygulamanın PyInstaller ile paketlendiğinde data klasörünü bulamaması durumunda
        # Daha detaylı hata mesajı veya loglama eklenebilir.
        # print(f"Hata: 'data' klasörü bulunamadı: {data_folder_path}")
        # QMessageBox.critical(None, "Hata", f"'data' klasörü bulunamadı: {data_folder_path}")
        return {} # Boş bir sözlük döndür

    vit_folders = []
    # data klasöründeki tüm öğeleri tara
    for item in os.listdir(data_folder_path):
        item_path = os.path.join(data_folder_path, item)
        # VITx desenine uyan ve gerçekten bir klasör olanları bul
        if os.path.isdir(item_path) and re.match(r"VIT\d+", item):
            vit_folders.append(item_path)

    if not vit_folders:
        # print("Hata: 'VIT' klasörleri 'data' dizininde bulunamadı.")
        # QMessageBox.critical(None, "Hata", "VIT klasörleri 'data' dizininde bulunamadı.")
        return {}

    # Klasörleri isme göre sırala (VIT1, VIT2, ..., VIT10 gibi doğru sıralama için)
    # Varsayılan sıralama VIT1, VIT10, VIT2 olabilir. Doğru sayısal sıralama için
    # sayısal kısmı ayırıp sıralama anahtarı olarak kullanmalıyız.
    vit_folders.sort(key=lambda x: int(re.search(r"VIT(\d+)", x).group(1)) if re.search(r"VIT(\d+)", x) else 0)

    latest_vit_folder = vit_folders[-1] # En son (en büyük numaralı) klasörü al

    excel_files = {}
    
    # Beklenen Excel dosyalarının tam yollarını oluştur
    basvurular_path = os.path.join(latest_vit_folder, "Basvurular.xlsx")
    mentor_path = os.path.join(latest_vit_folder, "Mentor.xlsx")
    mulakatlar_path = os.path.join(latest_vit_folder, "Mulakatlar.xlsx")

    # Dosyaların varlığını kontrol et ve sözlüğe ekle
    if os.path.exists(basvurular_path):
        excel_files["Basvurular"] = basvurular_path
    else:
        # print(f"Uyarı: {basvurular_path} bulunamadı.")
        pass # Veya kullanıcıya hata mesajı gösterebilirsiniz
    
    if os.path.exists(mentor_path):
        excel_files["Mentor"] = mentor_path
    else:
        # print(f"Uyarı: {mentor_path} bulunamadı.")
        pass

    if os.path.exists(mulakatlar_path):
        excel_files["Mulakatlar"] = mulakatlar_path
    else:
        # print(f"Uyarı: {mulakatlar_path} bulunamadı.")
        pass

    return excel_files