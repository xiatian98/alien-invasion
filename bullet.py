import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """管理飞船所发射子弹的类"""
    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹对象"""
        # 继承Sprite类
        super().__init__()
        # 将当前游戏窗口屏幕赋给screen
        self.screen = ai_game.screen
        # 将当前游戏设置赋值给settings
        self.settings = ai_game.settings
        # settings调用子弹颜色，赋值给color
        self.color = self.settings.bullet_color
        # 在(0, 0)处即左上角创建一个表示子弹的矩形，再设置正确的位置
        # 再设置子弹的长宽
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        # 把子弹的位置赋给当前的rect对象
        self.rect.midtop = ai_game.ship.rect.midtop
        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

    def update(self):
        """管理子弹位置的方法"""
        # 更新表示子弹位置的小数值
        # 向上发射子弹
        self.y -= self.settings.bullet_speed
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
