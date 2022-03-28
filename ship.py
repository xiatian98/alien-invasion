import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类"""
    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()

        # 将游戏窗口的屏幕赋给Ship的一个属性，以便这个类中的所有方法都可以访问
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # 使用get_rect()获取屏幕的属性，并将其赋给self.screen_rect
        # 以便将飞船放在游戏窗口的正确位置
        # 获取当前的游戏窗口并将其赋给screen_rect
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形
        # pygame.image.load()加载飞船图像，将图像的位置传递给self.image
        self.image = pygame.image.load('../imgs/ship.bmp')
        # 用get_rect()方法获取飞船的外接矩形并将这个矩形传递给rect
        self.rect = self.image.get_rect()

        # 将每一艘新飞船都将其放在屏幕底部中央
        # 获取游戏窗口的矩形的底部中央并将其赋给飞船矩形rect的midbottom属性
        self.rect.midbottom = self.screen_rect.midbottom
        # 在飞船的属性x,y中存储小数值
        # 把飞船矩形rect的横纵坐标转换为浮点型并赋给变量x,y
        # 用这个x,y的值作为飞船的坐标
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 移动标志
        # 向右移动
        self.moving_right = False
        # 向左移动
        self.moving_left = False
        # 向上移动
        self.moving_up = False
        # 向下移动
        self.moving_down = False

    def update(self):
        """根据移动标志调整飞船的位置"""
        # 更新飞船而不是rect对象的x值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # 如果移动标志为真且飞船的右边x值小于屏幕右边的x值，说明飞船在游戏屏幕内
            # 向右移动
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            # 如果移动标志为真且飞船的左边位置大于0,说明在游戏窗口内
            # 向左移动
            self.x -= self.settings.ship_speed
        # 根据浮点型self.x 更新整型的rect对象
        self.rect.x = self.x
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        self.rect.y = self.y

    def blitme(self):
        """在指定位置绘制飞船"""
        # self.image要绘制的图像，self.rect要绘制的图像的位置
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕底端居中"""
        # 将游戏窗口屏幕的底部中央赋值给飞船的midbottom
        self.rect.midbottom = self.screen_rect.midbottom
        # 飞船的x坐标赋值给x
        self.x = float(self.rect.x)
