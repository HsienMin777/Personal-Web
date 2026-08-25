import pygame
import os
import random

#-------------------------------------------------
import cv2
import mediapipe as mp
import math
import keyboard

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
#-------------------------------------------------

pygame.init()

screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))

RUNNING = [
    pygame.image.load(os.path.join("assets/Dino", "Chrome Dino Run.png")),
    pygame.image.load(os.path.join("assets/Dino", "Chrome Dino Run 2.png"))
]
JUMPING = pygame.image.load(os.path.join("assets/Dino", "Dino Jump.png"))
DUCKING = [
    pygame.image.load(os.path.join("assets/Dino", "Dino Duck.png")),
    pygame.image.load(os.path.join("assets/Dino", "Dino Duck 2.png"))
]
CLOUD = pygame.image.load(os.path.join("assets/Other", "Chrome Dinosaur Cloud.png"))
BG = pygame.image.load(os.path.join("assets/Other", "Chrome Dinosaur Track.png"))
SMALL_CACTUS = [
    pygame.image.load(
        os.path.join("assets/Cactus", "Chrome Dinosaur Small Cactus.png")),
    pygame.image.load(
        os.path.join("assets/Cactus", "Chrome Dinosaur Small Cactus (1).png")),
    pygame.image.load(
        os.path.join("assets/Cactus", "Chrome Dinosaur Small Cactus (2).png"))
]
LARGE_CACTUS = [
    pygame.image.load(
        os.path.join("assets/Cactus", "Chrome Dinosaur Large Cactus.png")),
    pygame.image.load(
        os.path.join("assets/Cactus", "Chrome Dinosaur Large Cactus (1).png")),
    pygame.image.load(
        os.path.join("assets/Cactus", "Chrome Dinosaur Large Cactus (2).png")),
]
BIRD = [
    pygame.image.load(
        os.path.join("assets/Bird", "Chrome Dinosaur Bird1.png")),
    pygame.image.load(
        os.path.join("assets/Bird", "Chrome Dinosaur Bird2.png")),
]

#-------------------------------------------------
def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ = 180
    return angle_

# 根據傳入的 21 個節點座標，得到該手指的角度
def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list

# 根據手指角度的串列內容，返回對應的手勢名稱
def hand_pos(finger_angle):
    f1 = finger_angle[0]   # 大拇指角度
    f2 = finger_angle[1]   # 食指角度
    f3 = finger_angle[2]   # 中指角度
    f4 = finger_angle[3]   # 無名指角度
    f5 = finger_angle[4]   # 小拇指角度

    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
    '''
    if f1<50 and f2>=50 and f3>=50 and f4>=50 and f5>=50:
        return 'good'
    elif f1>=50 and f2>=50 and f3<50 and f4>=50 and f5>=50:
        return 'no!!!'
    elif f1<50 and f2<50 and f3>=50 and f4>=50 and f5<50:
        return 'ROCK!'
    '''
    if f1>=50 and f2>=50 and f3>=50 and f4>=50 and f5>=50:
        return '0'
    elif f1<50 and f2<50 and f3<50 and f4<50 and f5<50:
        keyboard.press_and_release('up')
        print("hand key : up")
        return '5'
    elif f1>=50 and f2<50 and f3<50 and f4<50 and f5>50:
        keyboard.press_and_release('down')
        print("hand key : down")
        return '3'    
    else:
        return ''
#-------------------------------------------------

class Dinosaur:
    X_pos = 80
    Y_pos = 310
    Y_pos_duck = 340
    set_jump_vel = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.set_jump_vel
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        print(self.dino_rect)
        #self.dino_rect.inflate_ip(-40, -40)  # 先縮小 hitbox
        print(self.dino_rect)
        self.dino_rect.x = self.X_pos        # 再設定位置
        self.dino_rect.y = self.Y_pos
        print(self.dino_rect)

    def update(self, hand_command):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 20:
            self.step_index = 0

        if hand_command == '5' and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif hand_command == '3' and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or hand_command == 'duck'):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
    def duck(self):
        self.image = self.duck_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.inflate_ip(-30, -30)  # 先縮小 hitbox

        self.dino_rect.x = self.X_pos
        self.dino_rect.y = self.Y_pos_duck
        self.step_index += 1


    def run(self):
        self.image = self.run_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.inflate_ip(-30, -30)  # 先縮小 hitbox
        self.dino_rect.x = self.X_pos
        self.dino_rect.y = self.Y_pos
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 5
            self.jump_vel -= 0.85
            print(f"y pos: {self.dino_rect.y}, jump vel: {self.jump_vel: .2f}")
        if self.jump_vel < -self.set_jump_vel:
            self.dino_jump = False
            self.jump_vel = self.set_jump_vel
            print("jump stop", self.jump_vel)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = screen_width + random.randint(500, 2000)
        self.y = random.randint(50, 200)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = screen_width + random.randint(500, 1500)
            self.y = random.randint(50, 200)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
        
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.inflate_ip(-10, -10)  # 先縮小 hitbox

        self.rect.y = 260
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 10:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

def main():
#-------------------------------------------------
    cap = cv2.VideoCapture(0)            # 讀取攝影機
    fontFace = cv2.FONT_HERSHEY_SIMPLEX  # 印出文字的字型
    lineType = cv2.LINE_AA       
    global game_speed, x_pos_bg, y_pos_bg, obstacles, points
    run = True
    clock = pygame.time.Clock()
    cloud = Cloud()
    player = Dinosaur()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    obstacles = []
    death_count = 0
    points = 0
    font = pygame.font.Font(os.path.join("assets/font", "ARCADECLASSIC.TTF"), 30)


    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        bg_rect = BG.get_rect()
        screen.blit(BG, (x_pos_bg, y_pos_bg))
        screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
        bg_rect.x = x_pos_bg
    
    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render(str(points), True, (94, 94, 94))
        textRect = text.get_rect()
        textRect.center = (1000, 60)
        screen.blit(text, textRect)

    hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
        
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((255, 255, 255))
#-------------------------------------------------
        # mediapipe 啟用偵測手掌
        

        if not cap.isOpened():
            print("Cannot open camera")
            exit()
        w, h = 540, 310                                  # 影像尺寸
        
        ret, img = cap.read()
        img = cv2.resize(img, (w,h))                 # 縮小尺寸，加快處理效率
        if not ret:
            print("Cannot receive frame")
            break
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉換成 RGB 色彩
        results = hands.process(img2)                # 偵測手勢
        hand_command = ""
        finger_angle = None  # 先初始化

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_points = []                   # 記錄手指節點座標的串列
                for i in hand_landmarks.landmark:
                    # 將 21 個節點換算成座標，記錄到 finger_points
                    x = i.x*w
                    y = i.y*h
                    finger_points.append((x,y))
                if finger_points:
                    finger_angle = hand_angle(finger_points)
        
        if finger_angle:
            hand_command = hand_pos(finger_angle)
        else:
            hand_command = ""
#-------------------------------------------------

        userInput = pygame.key.get_pressed()

        cloud.draw(screen)
        cloud.update()

        background()

        score()

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        player.draw(screen)

        player.update(hand_command)
        
        clock.tick(30)
        pygame.display.update()
        

def menu(death_count):
    global points
    run = True
    while run:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(os.path.join("assets/font", "ARCADECLASSIC.TTF"), 30)

        if death_count == 0:
            text = font.render("Press any key to start", True, (94, 94, 94))
        elif death_count > 0:
            text = font.render("Press any key to restart", True, (94, 94, 94))
            score = font.render("Your Score  " + str(points), True, (94, 94, 94))
            scoreRect = score.get_rect()
            scoreRect.center = (screen_width // 2, screen_height // 2 + 50)
            screen.blit(score, scoreRect)

        textRect = text.get_rect()
        textRect.center = (screen_width // 2, screen_height // 2)
        screen.blit(text, textRect)
        screen.blit(RUNNING[0], (screen_width // 2 - 20, screen_height // 2 - 140))   
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

menu(death_count=0)

