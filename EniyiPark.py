import numpy as np
import matplotlib.pyplot as plt
import heapq


def park_alani_olustur():
   
    try:
        satir = int(input("Park alanının yatay uzunluğunu giriniz: "))
        sutun = int(input("Park alanının dikey uzunluğunu giriniz: "))

        print("Park alanının durumunu giriniz (Dolu: 1, Boş: 0):")
        matrix = []
        for i in range(satir):
            while True:
                satir_verileri = input(f"{i + 1}. satır verilerini boşluklarla ayırarak girin: ")
                elemanlar = satir_verileri.split()
                if len(elemanlar) == sutun and all(e in ("0", "1") for e in elemanlar):
                    matrix.append([int(e) for e in elemanlar])
                    break
                else:
                    print("Hatalı giriş! Lütfen yalnızca 0 ve 1 içeren doğru uzunlukta bir satır girin.")
        return matrix
    except ValueError:
        print("Hatalı giriş! Lütfen sayısal bir değer girin.")
        return None


def baslangic_noktasi_belirle(satir, sutun):
    """Başlangıç noktasını kullanıcıdan alır."""
    while True:
        try:
            x = int(input(f"Başlangıç satırını girin (0 ile {satir - 1} arasında): "))
            y = int(input(f"Başlangıç sütununu girin (0 ile {sutun - 1} arasında): "))
            if 0 <= x < satir and 0 <= y < sutun:
                return (x, y)
            else:
                print(f"Geçersiz koordinatlar! Lütfen 0 ile {satir - 1} arasında bir değer girin.")
        except ValueError:
            print("Lütfen geçerli bir sayısal değer girin.")


def dijkstra_algoritmasi(matrix, baslangic):
    """Dijkstra algoritması ile en yakın boş (0) noktayı bulur."""
    satir, sutun = len(matrix), len(matrix[0])
    yonler = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

    queue = [(0, baslangic[0], baslangic[1])]  
    ziyaret_edilen = set()

    while queue:
        mesafe, x, y = heapq.heappop(queue)

        if matrix[x][y] == 0:  # Boş alan bulundu
            return (x, y, mesafe)

        if (x, y) in ziyaret_edilen:
            continue

        ziyaret_edilen.add((x, y))

        for dx, dy in yonler:
            nx, ny = x + dx, y + dy
            if 0 <= nx < satir and 0 <= ny < sutun and (nx, ny) not in ziyaret_edilen:
                heapq.heappush(queue, (mesafe + 1, nx, ny))

    return None  # Boş alan yok


def matrix_gorsellestir(matrix, baslangic_noktasi, en_iyi_nokta):
    """Matrisin görselleştirilmesi."""
    satir, sutun = len(matrix), len(matrix[0])
    gorsel_matrix = np.zeros((satir, sutun, 3))  # RGB renk kodları

    for i in range(satir):
        for j in range(sutun):
            if matrix[i][j] == 1:  # Dolu
                gorsel_matrix[i, j] = [1, 0, 0]  # Kırmızı
            else:  # Boş
                gorsel_matrix[i, j] = [0, 1, 0]  # Yeşil

    # Başlangıç noktası (Sarı)
    gorsel_matrix[baslangic_noktasi[0], baslangic_noktasi[1]] = [1, 1, 0]

    # En iyi nokta (MAvi)
    if en_iyi_nokta:
        en_iyi_x, en_iyi_y, _ = en_iyi_nokta
        gorsel_matrix[en_iyi_x, en_iyi_y] = [0, 0, 1]

    # Görselleştir
    plt.imshow(gorsel_matrix)
    plt.title("Kırmızı: Dolu, Yeşil: Boş, Mavi: En iyi nokta, Sarı: Başlangıç noktası")
    plt.axis("off")
    plt.show()



park_matrix = park_alani_olustur()
if park_matrix:
    satir, sutun = len(park_matrix), len(park_matrix[0])
    baslangic_noktasi = baslangic_noktasi_belirle(satir, sutun)
    sonuc = dijkstra_algoritmasi(park_matrix, baslangic_noktasi)

    if sonuc:
        x, y, mesafe = sonuc
        print(f"En yakın boş park yeri: ({x}, {y}), Mesafe: {mesafe} birim")
    else:
        print("Park alanında boş yer yok.")

    matrix_gorsellestir(park_matrix, baslangic_noktasi, sonuc)
