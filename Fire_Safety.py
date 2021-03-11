import cv2
import numpy as np
import serial
import datetime
import time


firein1 = 0
firein2 = 0
firein3 = 0
firein4 = 0
hroom1 = 0
hroom2 = 0
hpass1 = 0

try:
    ser1 = serial.Serial('COM3', 9600, timeout=0)  # COM порт режима
    ser2 = serial.Serial('COM4', 9600, timeout=0)  # COM порт экрана
except:
    print('ERROR:  Ошибка подключения COM портов')
    sys.exit()



if __name__ == '__main__':
    def nothing(*arg):
        pass


    #Создаем окна
    cv2.namedWindow('room1cam1')  # создаем окно комната 1 камера 1
    cv2.namedWindow('room2cam1')  # создаем окно комната 1 камера 1
    #cv2.namedWindow('passcam1')  # создаем окно коридор камера 1
    #cv2.namedWindow('passcam2')  # создаем окно коридор камера 2
    cv2.namedWindow('plan')  # создаем главное окно
    cv2.namedWindow('settings', cv2.WINDOW_NORMAL)  # создаем окно настроек

    # создаем бегунки для настройки
    cv2.createTrackbar('sens Fire', 'settings', 0, 5, nothing)
    cv2.createTrackbar('sens H1', 'settings', 0, 5, nothing)
    cv2.createTrackbar('sens_ H2', 'settings', 0, 5, nothing)
    cv2.createTrackbar('detect', 'settings', 0, 5, nothing)
    cv2.createTrackbar('FIRE ALARM', 'settings', 0, 1, nothing)
    crange = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    #Подключаем камеры
    cap0 = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # комната 1 камера 1
    cap0.set(cv2.CAP_PROP_FPS, 15)
    cap0.set(3, 640)
    cap0.set(4, 480)

    cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # комната 1 камера 2
    cap1.set(cv2.CAP_PROP_FPS, 15)
    cap1.set(3, 640)
    cap1.set(4, 480)

    #cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)  # комната 2 камера 1
    #cap2.set(cv2.CAP_PROP_FPS, 15)
    #cap2.set(3, 640)
    #cap2.set(4, 480)

    #cap3 = cv2.VideoCapture(3, cv2.CAP_DSHOW)  # комната 2 камера 2
    #cap3.set(cv2.CAP_PROP_FPS, 15)
    #cap3.set(3, 640)
    #cap3.set(4, 480)
    #cap2.set(4, 480)

    # схема здания
    imgfile = cv2.imread('1.jpg')


#функция обнаружения огня
def firedetect(hsvV,sens_fire,detect,nroom):
    global firein1
    global firein2
    global firein3
    global firein4

    if sens_fire == 0:
        h_min = np.array((0, 93, 241), np.uint8)
        h_max = np.array((172, 199, 255), np.uint8)

    if sens_fire == 1:
        h_min = np.array((0, 94, 241), np.uint8)
        h_max = np.array((96, 150, 255), np.uint8)

    if sens_fire == 2:
        h_min = np.array((176, 93, 173), np.uint8)
        h_max = np.array((255, 224, 255), np.uint8)

    if sens_fire == 3:
        h_min = np.array((147, 19, 174), np.uint8)
        h_max = np.array((255, 240, 255), np.uint8)

    if sens_fire == 4:
        h_min = np.array((165, 64, 155), np.uint8)
        h_max = np.array((191, 175, 255), np.uint8)

    if sens_fire == 5:
        h_min = np.array((0, 137, 125), np.uint8)
        h_max = np.array((182, 255, 255), np.uint8)

    if detect == 0:
        fdetect = 100
        ldetect = 500
    if detect == 1:
        fdetect = 100
        ldetect = 1000
    if detect == 2:
        fdetect = 100
        ldetect = 20000
    if detect == 3:
        fdetect = 10000
        ldetect = 20000
    if detect == 4:
        fdetect = 12000
        ldetect = 40000
    if detect == 5:
        fdetect = 500
        ldetect = 50000

    # накладываем фильтр на кадр в модели HSV
    thresh = cv2.inRange(hsvV, h_min, h_max)

    # кординаты центра огня
    moments = cv2.moments(thresh, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']

    thresh = cv2.GaussianBlur(thresh, (5, 5), 2)  # размываем кадр

    no_red = cv2.countNonZero(thresh)  # Функция возвращает количество ненулевых элементов
    print('FIRE-',no_red)
    if ((int(no_red) > fdetect) and (int(no_red) < ldetect)):

        # Выводим кординаты огня
        if dArea > 100:
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)
            cv2.circle(imgfile, (x, y), 5, (0, 0, 255), 2)

            if nroom == 'room1':
                firein1 = 1
                cv2.putText(imgfile, "FIRE", (640-x, 810-y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if nroom == 'room2':
                firein2 = 1
                cv2.putText(imgfile, "FIRE",(1200-x, 810-y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if nroom == 'pass1':
                firein3 = 1
                cv2.putText(imgfile, "FIRE",(40,180),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if nroom == 'pass2':
                firein4 = 1
                cv2.putText(imgfile, "FIRE",(1120, 180),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.createTrackbar('FIRE ALARM', 'settings', 1, 1, nothing)

#Функция обнаружения людей
def humandetect(hsvVV,nroom):
    total = 0
    #Зеленые человечки
    if sens_fire == 0:
        h_min = np.array((60, 42, 32), np.uint8)
        h_max = np.array((81, 157, 97), np.uint8)

    if sens_fire == 1:
        h_min = np.array((37, 73, 0), np.uint8)
        h_max = np.array((81, 255, 255), np.uint8)

    if sens_fire == 2:
        h_min = np.array((144, 27, 34), np.uint8)
        h_max = np.array((80, 92, 64), np.uint8)

    if sens_fire == 3:
        h_min = np.array((0, 33, 0), np.uint8)
        h_max = np.array((75, 97, 52), np.uint8)

    if sens_fire == 4:
        h_min = np.array((59, 74, 6), np.uint8)
        h_max = np.array((102, 118, 52), np.uint8)

    if sens_fire == 5:
        h_min = np.array((60, 42, 32), np.uint8)
        h_max = np.array((81, 157, 97), np.uint8)


    hsvVVV = cv2.cvtColor(hsvVV, cv2.COLOR_BGR2HSV)
    green = cv2.inRange(hsvVVV, h_min, h_max)
    gray = cv2.GaussianBlur(green, (3, 3), 0)
    edged = cv2.Canny(gray, 10, 250)
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21), (10, 10))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (14, 14), (5, 5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        # аппроксимируем (сглаживаем) контур
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.0008 * peri, True)

        # если количество вершин = то считаем
        if ((len(approx) > 60) and (len(approx) < 160)):

            moments = cv2.moments(approx, 1)
            dM01 = moments['m01']
            dM10 = moments['m10']
            dArea = moments['m00']
            if dArea > 100:
                x = int(dM10 / dArea)
                y = int(dM01 / dArea)
                #cv2.circle(hsvVV, (x, y), 5, (0, 0, 255), 2)
                if nroom == 'room1':
                    #cv2.putText(hsvVV, "o", (x + 10, y - 10),
                                #cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(imgfile, "o", (640-x, 810-y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

                if nroom == 'room2':
                    #cv2.putText(hsvVV, "%d-%d" % (x, y), (x + 10, y - 10),
                                #cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(imgfile, "o", (1200-x, 810-y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)



                if nroom == 'pass1':
                    cv2.putText(hsvVV, "%d-%d" % (x, y), (x + 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                if nroom == 'pass2':
                    cv2.putText(hsvVV, "%d-%d" % (x, y), (x + 10, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)



            cv2.drawContours(hsvVV, [approx], -1, (0, 255, 0), 4)
            total += 1

    # Синии человечки
    if sens_fire == 0:
        h_min = np.array((99, 122, 0), np.uint8)
        h_max = np.array((255, 255, 255), np.uint8)

    if sens_fire == 1:
        h_min = np.array((96, 157, 24), np.uint8)
        h_max = np.array((173, 255, 255), np.uint8)

    if sens_fire == 2:
        h_min = np.array((46, 47, 26), np.uint8)
        h_max = np.array((113, 197, 123), np.uint8)

    if sens_fire == 3:
        h_min = np.array((91, 102, 39), np.uint8)
        h_max = np.array((114, 178, 98), np.uint8)

    if sens_fire == 4:
        h_min = np.array((98, 128, 0), np.uint8)
        h_max = np.array((111, 175, 186), np.uint8)

    if sens_fire == 5:
        h_min = np.array((94, 99, 46), np.uint8)
        h_max = np.array((151, 199, 106), np.uint8)

    hsvVVV = cv2.cvtColor(hsvVV, cv2.COLOR_BGR2HSV)
    green = cv2.inRange(hsvVVV, h_min, h_max)
    gray = cv2.GaussianBlur(green, (3, 3), 0)
    edged = cv2.Canny(gray, 10, 250)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21), (10, 10))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (14, 14), (5, 5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        # аппроксимируем (сглаживаем) контур
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.0008 * peri, True)

        # если количество вершин = то считаем
        if ((len(approx) > 60) and (len(approx) < 160)):

            moments = cv2.moments(approx, 1)
            dM01 = moments['m01']
            dM10 = moments['m10']
            dArea = moments['m00']
            if dArea > 100:
                x = int(dM10 / dArea)
                y = int(dM01 / dArea)
                #cv2.circle(hsvVV, (x, y), 5, (0, 0, 255), 1)
                if nroom == 'room1':
                    #cv2.putText(hsvVV, "%d-%d" % (x, y), (x + 10, y - 10),
                            #cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(imgfile, "o", (640-x, 810-y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

                if nroom == 'room2':
                    #cv2.putText(hsvVV, "%d-%d" % (x, y), (x + 10, y - 10),
                            #cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(imgfile, "o", (1200-x, 810-y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)


                if nroom == 'pass1':
                    cv2.putText(hsvVV, "%d-%d" % (x, y), (x + 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                if nroom == 'pass2':
                    cv2.putText(hsvVV, "%d-%d" % (x, y), (x + 10, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)



            cv2.drawContours(hsvVV, [approx], -1, (0, 255, 0), 4)
            total += 1

    return total


while True:
    now = datetime.datetime.now() #Текущая дата

    flag0, img0 = cap0.read()  # захватываем текущий кадр и кладем его в переменную img0
    if flag0 == False:
        print('ERROR: Не подключена камера 1')
    flag1, img1 = cap1.read()  # захватываем текущий кадр и кладем его в переменную img1
    if flag1 == False:
        print('ERROR: Не подключена камера 2')
    #flag2, img2 = cap2.read()  # захватываем текущий кадр и кладем его в переменную img2
    #if flag2 == False:
        #print('ERROR: Не подключена камера 3')
    #flag3, img3 = cap3.read()  # захватываем текущий кадр и кладем его в переменную img3
    #if flag3 == False:
        #print('ERROR: Не подключена камера 4')

    #НАСТРОЙКА КАМЕР
    room1 = img0
    room2 = img1
    #pass1 = img2
    #pass2 = img2

    # считываем значения бегунков
    sens_fire = cv2.getTrackbarPos('sens Fire', 'settings')
    sens_H1 = cv2.getTrackbarPos('sens H1', 'settings')
    sens_H2 = cv2.getTrackbarPos('sens H2', 'settings')
    detect = cv2.getTrackbarPos('detect', 'settings')
    FIRE_ALARM = cv2.getTrackbarPos('FIRE ALARM', 'settings')

    # Обновляем картинку
    imgfile = cv2.imread('1.jpg')



    if FIRE_ALARM == 1:
        cv2.putText(imgfile, "ATTENTION: FIRE ", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
        ser2.write(bytes([hroom1])+bytes([hroom2]))
        time.sleep(0.05)

        if (firein1 == 1) and (firein3 == 0) and (firein4 == 0):
            print('РЕЖИМ 3')
            ser1.write(b'3')
            time.sleep(0.1)

        if (firein2 == 1) and (firein3 == 0) and (firein4 == 0):
            print('РЕЖИМ 3')
            ser1.write(b'3')
            time.sleep(0.1)


        if (firein3 == 1) and (firein4 == 0):
            print('РЕЖИМ 2')
            ser1.write(b'2')
            time.sleep(0.1)

        if (firein3 == 0) and (firein4 == 1):
            print('РЕЖИМ 1')
            ser1.write(b'1')
            time.sleep(0.1)

        if (firein3 == 1) and (firein4 == 1):
            print('РЕЖИМ 3')
            ser1.write(b'3')
            time.sleep(0.1)


    else:
        firein1 = 0
        fierin2 = 0
        firein3 = 0
        firein4 = 0
        ser1.write(b'0')
        ser2.write(bytes([0])+bytes([0]))

    firedetect(room1, sens_fire,detect, 'room1')
    firedetect(room2, sens_fire,detect, 'room2')
    #firedetect(pass1, sens_fire,detect, 'pass1')
    #firedetect(pass2, sens_fire,detect, 'pass2')

    hroom1 = humandetect(room1, 'room1')
    hroom2 = humandetect(room2, 'room2')
    #hpass1 = humandetect(pass1, 'pass1')
    #hpass2 = humandetect(pass2, 'pass2')
    #hpass12 = 0
    #hpass12 = hpass1+hpass2



    cv2.putText(imgfile, " find {0} object".format(hroom1), (140, 800), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 4)
    cv2.putText(imgfile, " find {0} object".format(hroom2), (700, 800), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 4)
    #cv2.putText(imgfile, " find {0} object".format(hpass12), (500, 80), cv2.FONT_HERSHEY_SIMPLEX,
                #1, (255, 0, 0), 4)


    cv2.putText(imgfile, "Date:{0} ".format(now.strftime("%d-%m-%Y %H:%M:%S")), (600, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 2)
    #cv2.putText(imgfile, " find {0} object".format(humandetect(pass2, 'pass2')), (300, 150), cv2.FONT_HERSHEY_SIMPLEX,
    #            1, (255, 0, 0), 4)


    #Выводим окна
    cv2.imshow('room1cam1', room1)  # отображаем кадр комната 1 камера 1
    cv2.imshow('room2cam1', room2)  # отображаем кадр комната 1 камера 2
    #cv2.imshow('passcam1', pass1)  # отображаем кадр комната 2 камера 1
    #cv2.imshow('passcam2', pass2)  # отображаем кадр комната 2 камера 2
    cv2.imshow('plan', imgfile)  # отображаем кадр в окне с именем result

    if FIRE_ALARM == 1:
        if ((now.second == 10) or (now.second == 20) or (now.second == 30) or (now.second == 40) or (now.second == 50)):
            filename1 = now.strftime("%d%m%y-%H%M%S")
            cv2.imwrite(filename1 + '.png', imgfile)

    ch = cv2.waitKey(5)
    if ch == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
