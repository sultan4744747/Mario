#вызов библиотеки pygame и инициализация ее
import pygame
import random
pygame.init ()

#Выставляем широту и длину экрана в переменных
W = 800
H = 600

#сосздаем сам экран
screen = pygame.display.set_mode ((W, H))

#создаем счетчик кадров секунду
FPS =60

#объект часов
clock = pygame.time.Clock()

#создание всех необходимых переменных(шрифт,game_over которая будет обозначать проигрышь или нет)
font_path = 'SuperMario256.ttf'
font_large = pygame.font.Font(font_path, 48)
font_small = pygame.font.Font(font_path, 24)

game_over = False
# поверхности которые будут появлять при проигрыше и расположение его на экране
retry_text = font_small.render('PRESS ANY KEY', True, (255, 255, 255))
retry_rect = retry_text.get_rect()
retry_rect.midtop = (W//2,H//2)

#добавление файла земли а так же редактирование его в нужные размеры
ground_image = pygame.image.load('Снимок экрана 2024-05-04 в 17.27.10.png')
ground_image = pygame.transform.scale(ground_image,(804,60))
GROUND_H = ground_image.get_height()


#добавление файла uev,s а так же редактирование его в нужные размеры
enemy = pygame.image.load('gimi.png')
enemy = pygame.transform.scale(enemy,(80,80))


#добавление файла мертвого гумбы а так же редактирование его в нужные размеры
enemy_image = pygame.image.load('goomba_mini.png')
enemy_image = pygame.transform.scale(enemy_image,(80,80))


#добавление файла mario а так же редактирование его в нужные размеры
player_image = pygame.image.load('images1.png')
player_image = pygame.transform.scale(player_image,(80,60))



#//////////////////////////////////////////////////////////////////////////////////////////////////////
#класс для обвъявления сущностей(марио,гумба)
class Entity:
    #создание главной функции конструктора и создания в нем переменных для рисунка марио или гумба, скорости
    def __init__(self,image):
        self.image = image
        self.rect = self.image.get_rect()
        #скорость по x и y
        self.x_speed = 0
        self.y_speed = 0

        self.speed = 5 #оснавная скорость
        # переменные для проверки упали ли мы в пропасть или живыли мы или нет
        self.is_out = False
        self.is_dead=False
        #скорость прыжка
        self.jump_speed = -12
        #скорость гравитации
        self.gravity = 0.4
        #переменная для того чтобы мы знали находимся ли мы на земле или нет
        self.is_grounded = False

    #функция для управления пользовательским вводом. Она будет пустая но я буду предопредялять для того кому она нуждна будет в этом случаи для марио
    def handle_input(self):
        pass

    #функция для убивания нашей сущности
    def kill(self,dead_image):
        #замена картинки сущности на сплющенную
        self.image =dead_image
        #будем говорить что наша сущность мертва
        self.is_dead = True
        #эффект отлитания при смерти в сторону и подпрыгивания
        self.x_speed = -self.x_speed
        self.y_speed = self.jump_speed

    #функция перемещения
    def update(self):
        self.rect.x +=self.x_speed
        self.y_speed +=self.gravity
        self.rect.y += self.y_speed

        # проверка на то что умерли мы или нет
        if self.is_dead:
            if self.rect.top >GROUND_H:
                self.is_out = True

        else:
            self.handle_input()

            if self.rect.bottom >H-GROUND_H:
                self.is_grounded = True
                self.y_speed =0
                self.rect.bottom = H-GROUND_H
    #функция для отрисовки сущности
    def draw(self,surface):
        surface.blit(self.image, self.rect)



#//////////////////////////////////////////////////////////////////////////////////////////////////////
#класс для марио,унаследеванный из класса entity
class Player(Entity):
    def __init__(self):
        super().__init__(player_image) #передаем загруженную картинку игрока
        self.respawn()
    #функция для влияния скорости игрока
    def handle_input(self):
        self.x_speed = 0

        # реализация клавиши для движения в лево
        keys =pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_speed = -self.speed #двигаем в лево

        #реализация клавиши для движения в права
        elif keys[pygame.K_d]:
            self.x_speed  = self.speed# двигаем в право

        #реализация клавиши для прыжка
        if  self.is_grounded and keys[pygame.K_SPACE]:
            self.is_grounded = False
            self.jump()

    #функция для рестарта игры
    def respawn(self):
        self.is_out = False
        self.is_dead= False
        self.rect.midbottom = (W//2,H-GROUND_H)

    #функция прыжка
    def jump(self):
        self.y_speed = self.jump_speed


#/////////////////////////////////////////////////////////
#класс гумба или класса врага
class Goomba(Entity):
    def __init__(self):
        super().__init__(enemy)
        self.spawn()

    #функция для того что гумба появлялся
    def spawn(self):
        direction = random.randint(0,1)#выпадение гумба справа(0) или слева(1)

        if direction == 0:
            self.x_speed = self.speed
            self.rect.bottomright = (0,0)
        if direction == 1:
            self.x_speed = -self.speed
            self.rect.bottomleft(W,0)

    # добавление уже существующей функции и доработка её
    def update(self):
        super().update()

        #проверка на то что ушли ли гумбы в правую или левую часть экрана
        if self.x_speed > 0 and self.rect.left > W or self.x_speed <0 and self.rect.rect.right <0:
            self.is_out = True


player =  Player()# объект класса

#переменная для подсчиитания наших очков в игре
score =0

#список который булет хранить всех гумб на экране
goombas = []
# переменная которая будет хранить в себе начальную задержку гумбы
INIT_DELAY = 2000
#переменная которая будет oбозначать как часто спавняться гумбы
spawn_delay = INIT_DELAY
#переменная которая нужна для того чтобы усложнять игру или сокрощать время спавна гумб
DECREASE_BASE = 1.01
#переменная для того чтобы знать время последнего спавно
the_last_spawn_time  = pygame.time.get_ticks()

#игровой цыкл
running = True
while running:
    #перебираю события закрытия окна
    for e in pygame.event.get ( ) :
        if e.type == pygame. QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if player.is_out:
                score =0
                spawn_delay = INIT_DELAY
                the_last_spawn_time = pygame.time.get_ticks()
                player.respawn()
                goombas.clear()
    #ограничиваю игру по кадрам в секунду
    clock.tick(FPS)

    screen.fill((92,148,252))#залил экран

    #отрисовка земли
    screen.blit(ground_image, (0,H-GROUND_H))

    # поверхность для отрисовки очков и переменная
    score_text = font_large.render(str(score), True, (255,255,255))
    score_rect = score_text.get_rect()

    # проверка на то что вылетил ли марио за границы
    if player.is_out:
        score_rect.midbottom = (W//2,H//2)
        screen.blit(retry_text,retry_rect)
    else:

        # добавление сущности
        player.update()
        player.draw(screen)
        # текущее игровое время
        now_time = pygame.time.get_ticks()
        # время которое прошло с моента предидущего спавна
        elapsed = now_time - the_last_spawn_time
        # добавление сущности

        # проверка на то что прошло ли время  с момента предидущего спавно
        if elapsed >spawn_delay:
            the_last_spawn_time = now_time
            goombas.append(Goomba())

        # редактирование гумб(удалять тех кто ушел за поле )
        for goomba in list(goombas):
            if goomba.is_out:
                goombas.remove(goomba)
            else:
                goomba.update()
                goomba.draw(screen)
            if not player.is_dead and not goomba.is_dead and player.rect.colliderect(goomba.rect):
                if player.rect.bottom - player.y_speed < goomba.rect.top:
                    goomba.kill(enemy_image)
                    player.jump()
                    score+=1
                    spawn_delay = INIT_DELAY/(DECREASE_BASE ** score)
                else:
                    player.kill(player_image)


        #расположение счетчика
        score_rect.midtop = (W//2,H//5)
    #выставили счет очков в игре
    screen.blit(score_text,score_rect)
    pygame.display.flip()#обновил экран для того чтоб все отоброжалось
quit()