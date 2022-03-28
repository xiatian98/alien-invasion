import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """显示得分信息的类"""
    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用的字体设置
        # 字体颜色
        self.text_color = (30, 30, 30)
        # 实例化字体对象，使用默认字体，48号大小
        self.font = pygame.font.SysFont(None, 48)
        # 准备初始得分图像
        self.prep_score()
        # 最高得分图像
        self.prep_high_score()
        # 等级
        self.prep_level()
        # 余下的飞船数量
        self.prep_ships()

    def prep_score(self):
        """将得分转换为渲染的图像"""
        # round()将小数精确到小数位，由第二个参数指定
        # 第二个参数为负数，将舍入到最近的10的整数倍
        rounded_score = round(self.stats.score, -1)
        # 将得分转换为图像
        score_str = "{:,}".format(rounded_score)
        # render()创建图像
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        # 在屏幕右上角显示得分，得分牌始终在右上角
        self.score_rect = self.score_image.get_rect()
        # 得分牌的位置在距游戏窗口右边20像素的位置
        self.score_rect.right = self.screen_rect.right - 20
        # 距游戏窗口上方20像素的位置
        self.score_rect.top = 20

    def prep_high_score(self):
        """最高得分转换为渲染的图像"""
        # 将分数舍入到最近的10的整数倍
        high_score = round(self.stats.high_score, -1)
        # 用逗号分隔
        high_score_str = "{:,}".format(high_score)
        # 将得分生成图像
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        # 将最高得分放在顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        # 将分数水平居中
        self.high_score_rect.centerx = self.screen_rect.centerx
        # 将其得分属性设置为当前得分图像的top属性
        self.high_score_rect.top = self.score_rect.top

    def prep_ships(self):
        """显示余下还有多少艘飞船"""
        """方法prep_ships()创建一个空编组self.ships，用于存储飞船实例"""
        self.ships = Group()
        # 为填充这个编组，根据玩家还有多少艘飞船以相应的次数运行一个循环
        for ship_number in range(self.stats.ships_left):
            # 创建新飞船
            ship = Ship(self.ai_game)
            # 设置飞船的x坐标，让整个飞船编组都位于屏幕左边，且每艘飞船的左边距都为10像素
            ship.rect.x = 10 + ship_number * ship.rect.width
            # 设置飞船的y坐标
            ship.rect.y = 10
            # 将每艘新飞船都添加到编组ships中
            self.ships.add(ship)

    def show_score(self):
        """在屏幕上显示得分，最高分，等级"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # 在屏幕上显示飞船
        self.ships.draw(self.screen)

    def check_high_score(self):
        """检查是否诞生了新的最高分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """将等级转换为渲染的图像"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
