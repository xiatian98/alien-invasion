import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        """初始化按钮的属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸
        self.width, self.height = 200, 50
        # 颜色
        self.button_color = (0, 255, 0)
        # 文字颜色
        self.text_color = (255, 255, 255)
        # 字体为默认字体，大小为48号
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮的rect对象
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        # 使按钮居中
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需用创建一次
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        """调用font.render()将存储在msg中的文本转换为图像，再将该图像存储在self.msg_image中。
        方法font.render()还接受一个布尔实参，该实参指定开启还是关闭反锯齿功能（反锯齿让文本的边缘更平滑）。
        余下的两个实参分别是文本颜色和背景色。我们启用了反锯齿功能，并将文本的背景色设置为按钮的颜色。"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        """让文本图像在按钮上居中：根据文本图像创建一个rect，并将其center属性设置为按钮的center属性。"""
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        # 绘制表示矩形的按钮
        self.screen.fill(self.button_color, self.rect)
        # 在游戏窗口绘制文本图像
        self.screen.blit(self.msg_image, self.msg_image_rect)
