import pygame
import numpy as np
import random
import time
from pygame import mixer
from Ball import Ball
from Balloon import Balloon
from Human import Human
from cvzone.PoseModule import PoseDetector
import cv2
import ctypes
from Button import Button


def generate(generatedBalloon, BalloonList, Rwidth):
    if len(BalloonList) < num_of_Balloons:
        newBalloon = Balloon([0, -300], generatedBalloon)  # من class ballon pos color
        tx = random.randint(newBalloon.r,
                            Rwidth - newBalloon.r)  # تابع قيم عشوائية نقاط كل مرة بيطلع من مكان شكل .... استخدمات متحولات الballoon class
        newBalloon.pos[0] = tx  # اسند ال x ل tx
        goodBalloon = True
        for balloon in BalloonList:  # فتح حلقة وعطاها متغير ع و حيعبي الlist
            if Balloon.des(newBalloon, balloon) <= 1.2 * balloon.w:  # w  هو عرض البالون
                goodBalloon = False  # مشان ما يطلعو البوالين فوق بعض
        if goodBalloon:

            BalloonList.append(newBalloon)  # لادخال البوالين المحققة بالشرط في ليست

            if generatedBalloon == 'Red':  # مشان تنويع الألوان
                return 'Green'
            elif generatedBalloon == 'Green':
                return 'Red'
        else:
            return generatedBalloon  # اذا مو فوق بعض ولدهم عادي
    else:
        return generatedBalloon


def setscore(val):
    try:
        f = open("score.txt", "w")  # يتم تخزنينه في ملف نصي خارجي   w لكتابة أوامر على الملف االنصي
        f.write(str(val))
        f.close()
    except:  # في حال الerror ممرها وشغل الcode
        pass


def getscore():
    try:
        f = open("score.txt", "r")
        read = int(f.read())
        f.close()
        return read
    except:
        return False


def showScore():
    scoreText = font.render("Score : " + str(score), True, Black)  # لإظهار ع الشاشة
    screen.blit(scoreText, (0.04882 * width, 0.04166 * height))


def showScore1():
    scoreText = font.render("Max Score : " + str(getscore()), True, (255, 0, 0))
    screen.blit(scoreText, (0.04882 * width, 0.08333 * height))


def showTime(Timer):
    scoreText = font.render("Timer : " + str(int(Timer)), True, Black)  # لإظهار تابع عد الوقت
    screen.blit(scoreText, (0.82031 * width, 0.04166 * height))


def show(a, frame, scper):  # $$$
    resultCopy = frame.copy()
    width = int(resultCopy.shape[1] * scper / 100)
    height = int(resultCopy.shape[0] * scper / 100)
    dim = (width, height)
    resultCopy1 = cv2.resize(resultCopy, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow(a, resultCopy1)


if __name__ == '__main__':
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    print(screensize)
    running = True
    Rwidth = 1500  # لحتى روحح يمين و شمال
    pygame.init()
    width = screensize[0] - 100
    height = screensize[1] - 100
    screen = pygame.display.set_mode((width, height))
    Background = pygame.image.load('background.png')
    Background = pygame.transform.scale(Background, (height*2048//768, height))
    #wall = pygame.image.load()
    pygame.display.set_caption("Pop BalloonZ")
    icon = pygame.image.load('668016.png')
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()  # هي تعليمة مشان يشتغل على اي لابتوب مشان سرعة
    clock.tick(30)
    Black = (0, 0, 0)
    font = pygame.font.SysFont("Snap ITC", 25)
    num_of_Balloons = 10
    JointToLm = [0, 15, 16, 13, 14, 11, 12, 23, 24]  # cv zone list num by defult
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()  # for cvZone
    gameState = True

    while gameState:  # القيم بقبلها تتكرر
        realPos = [np.nan, np.nan]  # اسندنا قيميتن غير محددتين مع النمباي
        cameraPos = [Rwidth / 2 - (width / 2), 0]  # هنا تمركز x في منتصف الشاشة و y=0 من اجل مجال الحركة يكون ععلى x فقط
        moveSpeed = [20, 0]
        handled = False  # من أجل معرفة اذا mouse  موجودة فوق البالون عند عدم استخدام اللإبصار
        generatedBalloon = 'Red'
        BalloonList = []  # نخزن بقلبها كل بالون
        score = 0
        human = Human((width / 2 + 400, height / 1.3))  # متغير لنحدد مكان مركز الشخص النقطة بين الكتاف
        startTime = time.time()  # متغيرات الوقت في pheightgame
        currentTime = startTime
        Timer = 0
        popBalloon = pygame.mixer.Sound('1111.wav')
        modeName = "main"
        startButton = Button([Rwidth//2, height//2], 100, 'startBalloon.png')
        endButton = Button([Rwidth//2, height//3], 100, 'startBalloon.png')
        # DETERMAIN 60 SECOND TIME
        while running:
            if modeName == "main":
                if Ball.collides(human.joints[1], startButton) or Ball.collides(human.joints[2], startButton):
                    popBalloon.play()
                    startTime = time.time()  # متغيرات الوقت في pheightgame
                    currentTime = startTime
                    modeName = "play"
            elif modeName == "play":
                currentTime = time.time()
                Timer = currentTime - startTime
                if Timer > 5:
                    while True:
                        BalloonList.remove(balloon)
                        screen.fill((255, 255, 255))
                        screen.blit(Background, np.multiply(cameraPos, [-1, -1]))
                        modeName == "end"

            elif modeName == "end":

                if Ball.collides(human.joints[1], startButton) or Ball.collides(human.joints[2], startButton):
                    popBalloon.play()



            try:
                success, img = cap.read()  # img is camera variable
                img = cv2.flip(img, 1)  # FOR TOW DEMINTION ARRAY
                img = detector.findPose(img)






                lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)
                if bboxInfo:
                    for lm in lmList:
                        for i in range(0, 9):  ### متل حلقة تتكرر  يعني تسع مراتi<9
                            if lm[0] == JointToLm[i]:
                                human.editJoint(i, [lm[1], lm[2]])
                    realPos = human.convertToPos()
                else:
                    realPos = [np.nan, np.nan]
                # cv2.imshow("Image", img)
                if not np.isnan(realPos[0]):
                    humanOffset = width/20
                    cameraOffset = 20
                    print(realPos[0])
                    newX = ((Rwidth-2*humanOffset)*(realPos[0] - cameraOffset) / (img.shape[1]-2*cameraOffset)) + humanOffset + 100
                    human.setX(newX)
                    cameraPos[0] = newX - width/2
                # to move the body by keybord
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and cameraPos[0] > moveSpeed[0]:  # شرط الand يفيد ان نعمل حد لإزاحتو للإنسان
                    cameraPos = np.subtract(cameraPos, moveSpeed)
                    human.pos = np.subtract(human.pos, moveSpeed)
                if keys[pygame.K_RIGHT] and cameraPos[0] + width < Rwidth - moveSpeed[0]:
                    cameraPos = np.add(cameraPos, moveSpeed)
                    human.pos = np.add(human.pos, moveSpeed)

                    # pop balloon and increase score
                for balloon in BalloonList:
                    if pygame.mouse.get_pressed()[0] and balloon.is_clicked() and not handled:
                        handled = pygame.mouse.get_pressed()[0]
                        BalloonList.remove(balloon)
                        score += 1

                    if not pygame.mouse.get_pressed()[0]:
                        handled = False

                if modeName == "play":
                    generatedBalloon = generate(generatedBalloon, BalloonList, Rwidth)

                for balloon in BalloonList:
                    if Ball.collides(human.joints[1], balloon):
                        BalloonList.remove(balloon)

                        popBalloon.play()
                        if generatedBalloon == 'Red':
                            score += 10
                        elif generatedBalloon == 'Green':
                            score += 20


                    elif Ball.collides(human.joints[2], balloon):
                        BalloonList.remove(balloon)
                        popBalloon.play()
                        if generatedBalloon == 'Red':
                            score += 10
                        elif generatedBalloon == 'Green':
                            score += 20

                for balloon in BalloonList:  # $$
                    balloon.Force((0, 2))

                for balloon in BalloonList:  # $$
                    balloon.updatePos()

                # remove balloons
                for balloon in BalloonList:
                    if balloon.pos[1] >= height:  # to remove balloon when go down and not poped
                        BalloonList.remove(balloon)
                        score -= 3

                screen.fill((255, 255, 255))
                screen.blit(Background, np.multiply(cameraPos, [-1, -1]))
                #screen.blit(,)
                if modeName == "main":
                    startButton.draw(screen, cameraPos)
                human.drawHuman(screen, cameraPos)

                if  modeName == "end":
                    startButton.draw(screen, cameraPos)
                human.drawHuman(screen, cameraPos)

                # هل هاد الكود مشان الحدود ومؤشرات الجانبية على شكل مثلث
                for balloon in BalloonList:
                    if balloon.pos[0] - cameraPos[0] > width + balloon.r:
                        if balloon.color == 'Red':
                            pygame.draw.polygon(screen, (255, 0, 0),
                                                ([width - 50, balloon.pos[1] - 50], [width - 50, balloon.pos[1] + 50],
                                                 [width, balloon.pos[1]]))
                        elif balloon.color == 'Green':
                            pygame.draw.polygon(screen, (0, 255, 0),
                                                ([width - 50, balloon.pos[1] - 50], [width - 50, balloon.pos[1] + 50],
                                                 [width, balloon.pos[1]]))
                    if balloon.pos[0] < cameraPos[0] - balloon.r:
                        if balloon.color == 'Red':
                            pygame.draw.polygon(screen, (255, 0, 0),
                                                ([50, balloon.pos[1] - 50], [50, balloon.pos[1] + 50],
                                                 [0, balloon.pos[1]]))
                        elif balloon.color == 'Green':
                            pygame.draw.polygon(screen, (0, 255, 0),
                                                ([50, balloon.pos[1] - 50], [50, balloon.pos[1] + 50],
                                                 [0, balloon.pos[1]]))
                    else:
                        balloon.draw(screen, cameraPos)
                img = cv2.resize(img, np.floor_divide([img.shape[1], img.shape[0]], 3), interpolation=cv2.INTER_AREA)
                img = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "BGR")
                screen.blit(img, (width - img.get_width(), height - img.get_height()))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        gameState = False
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    running = False

                if modeName == "play":
                    showTime(Timer)
                    showScore()
                    showScore1()
                pygame.display.update()

                if modeName == "end":
                    showScore()

            except Exception as e:
                print("Error:", str(e))

                # to replace maxScore
            if score > getscore():
                setscore(score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            running = True
        elif keys[pygame.K_q]:
            gameState = False
        pygame.event.pump()

    cap.release()
    cv2.destroyAllWindows()
