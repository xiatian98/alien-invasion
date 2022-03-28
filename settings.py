# -*- coding:utf-8 -*-
class Settings:
    """存储游戏中所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        # 游戏窗口的宽
        self.screen_width = 800
        # 游戏窗口的高
        self.screen_height = 600
        # 游戏窗口的背景色
        self.bg_color = (230, 230, 230)

        # 飞船设置
        # 飞船的移动速度 标记
        # self.ship_speed = 1.5
        # 飞船的数量
        self.ship_limit = 3

        # 子弹设置
        # 子弹的速度 标记
        # self.bullet_speed = 1.5
        # 子弹的宽度
        self.bullet_width = 5
        # 子弹的高度
        self.bullet_height = 15
        # 子弹的颜色
        self.bullet_color = (60, 60, 60)
        # 屏幕上子弹的数量
        self.bullet_allowed = 5

        # 外星人设置
        # 外星人移动速度 标记
        # self.alien_speed = 0.5
        # 设置fleet_drop_speed指定有外星人撞到屏幕边缘时，外星人群向下移动的速度。
        self.fleet_drop_speed = 5
        # 加快游戏节奏的速度
        # 每一次重新开始都会在原来的基础上*1.1
        self.speedup_scale = 1.1
        # 外星人分数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随着游戏进行而变化的设置"""
        # 游戏难度增加后
        # 飞船的速度
        self.ship_speed = 2.0
        # 子弹的速度
        self.bullet_speed = 3.0
        # 外星人的速度
        self.alien_speed = 1.0
        # fleet_direction为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1
        # 计分，击杀一个外星人的分数
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置"""
        # 每一次重新开始飞船的移动速度=重新开始之前的速度*增加的速度
        self.ship_speed *= self.speedup_scale
        # 子弹的速度=原来子弹的速度*增加的速度
        self.bullet_speed *= self.speedup_scale
        # 外星人的速度=原来外星人的速度*增加的速度
        self.alien_speed *= self.speedup_scale
        # 外星人的分数=原来的分数*分数的增加值，再取整
        self.alien_points = int(self.alien_points * self.score_scale)