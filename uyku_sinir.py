from cvzone.FaceDetectionModule import FaceDetector
from cvzone.FaceMeshModule import FaceMeshDetector
import cv2


def sinirbul(durum):
    # webcamdan gorundu alindi
    cap = cv2.VideoCapture(0)
    # detector olarak goz agiz gibi degerleri bulan detector secildi
    detector = FaceMeshDetector(maxFaces=1)
    # ikinci detektor olarak yuzu bulan detektor secildi
    detector2 = FaceDetector()
    # gozun etrafini saran noktalarin id degerleri tanimlandi
    idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
    # orani daha etkili bulmasi icin uzaklik ortalamasi degerlerini tutacak liste tanimlandi
    ratioList = []

    while True:
        # video uzerinden deneme yapilinca video bitince basa sarmasi icin kosul
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        # goruntu okundu
        success, img = cap.read()

        # yuz uzerinden islem yapilacagi icin yuz bulunamazsa diye try except blogu kullanildi
        try:
            # yuz bulundu
            img, bboxs = detector2.findFaces(img)

            # yuzdeki degerlerin koordinatlari bulundu
            img, faces = detector.findFaceMesh(img, draw=False)
            # eger yuz bulundu ise
            if faces:
                # yuzun 0 id degeri bos tanimlandi
                face = faces[0]
                # goz noktalarinin dongu uzerinden cizilmesi saglandi
                for id in idList:
                    cv2.circle(img, (face[id][0], face[id][1]), 1,(0, 255, 255), cv2.FILLED)

                # gozde dikey ve yatay en uzun cizgi icin noktalar belirlendi
                leftup = (face[159][0], face[159][1])
                leftdown = (face[23][0], face[23][1])
                leftright = (face[243][0], face[243][1])
                leftleft = (face[130][0], face[130][1])
                cv2.line(img, leftup, leftdown, (0, 200, 0), 2)  # dikey cizgi cizildi
                cv2.line(img, leftleft, leftright, (0, 200, 0), 2)  # yatay cizgi cizildi
                # iki nokta arasindaki uzaklik bulundu
                lenghtVer, _ = detector.findDistance(leftup, leftdown)
                lenghtHor, _ = detector.findDistance(leftleft, leftright)

                # yatay uzaklik dikey uzakliga bolunerek kameraya yaklasma ve uzaklasma durumlarinda bile sadece dikey uzunluk uzerine yanlislik onlendi
                # bu sayede her uzaklikta belirli oranda aciklik saglanirsa programin uyari vermesi saglandi
                ratio = (lenghtVer / lenghtHor) * 100

                # ortalama degeri listeye eklendi
                ratioList.append(ratio)

                # eger listedeki eleman sayisi 3 u gecerse ilk degerin silinmesi saglandi bu sayede son 3 deger uzerinden islem yapilmasi saglandi
                if len(ratioList) > 10:
                    ratioList.pop(0)
                # listedeki elemanlarin ortalamasi alindi
                ratioAvg = sum(ratioList) / len(ratioList)  # formul sonucu tutan listenin toplami listedeki eleman sayisina bolundu

        # exception durumlarindan pas gecilmesi saglandi
        except Exception:
            pass
        
        # bilgilendirme yazisi
        cv2.putText(img, f"{durum} durumuna gecin ve q tusuna basin.", (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 255), 2)
        # goruntunun ekranda gosterilmesi saglandi
        cv2.imshow("Image", img)
        
        # her kare arasinda 10 milisaniye birakildi ve q tusuna basilirsa cikilmasi saglandi
        if cv2.waitKey(10) & 0xFF == ord('q'):
            # goruntu serbest birakildi
            cap.release()
            # pencelerin kapatilmasi saglandi
            cv2.destroyAllWindows()
            return ratioAvg
