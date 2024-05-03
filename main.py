#вызов библиотеки pygame и инициализация ее
import pygame
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
retry_text = font_small.render ('PRESS ANY KEY', True, (255, 255, 255))
retry_rect = retry_text.get_rect()
retry_text = (W//2,H//2)

#добавление файла земли а так же редактирование его в нужные размеры
ground_image = pygame.image.load('ground.png')
ground_image = pygame.transform.scale(ground_image,(804,60))
GROUND_H = ground_image.get_height()


#добавление файла uev,s а так же редактирование его в нужные размеры
enemy = pygame.image.load('goomba.png')
enemy = pygame.transform.scale(enemy,(80,80))


#добавление файла мертвого гумбы а так же редактирование его в нужные размеры
enemy_image = pygame.image.load('goomba_mini.png')
enemy_image = pygame.transform.scale(enemy_image,(80,80))


#добавление файла mario а так же редактирование его в нужные размеры
player_image = pygame.image.load('MARIO.png')
player_image = pygame.transform.scale(player_image,(80,80))



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
        self.gravity = 0.5
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


player =  Player()# объект класса

#переменная для подсчиитания наших очков в игре
score =0

#игровой цыкл
running = True
while running:
    #перебираю события закрытия окна
    for e in pygame.event.get ( ) :
        if e.type == pygame. QUIT:
            running = False

    #ограничиваю игру по кадрам в секунду
    clock.tick(FPS)

    screen.fill((92,148,252))#залил экран

    #добавление сущности
    player.update()
    player.draw(screen)

    pygame.display.flip()#обновил экран для того чтоб все отоброжалось
quit()