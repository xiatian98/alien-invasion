# -*- coding:utf-8 -*-
import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏资源和行为的类"""
    """the class who manages game resource and behavior"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        # 初始化背景设置
        pygame.init()
        # 创建设置实例
        self.settings = Settings()
        # 让游戏在全屏下运行
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        # 让游戏在窗口模式下运行
        # pygame.display.set_mode()创建一个显示窗口
        # 游戏的所有图形元素都在其中绘制
        # (self.settings.screen_width, self.settings.screen_height)是一个元组，指定游戏窗口的大小
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")
        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        # 创建记分牌
        self.sb = Scoreboard(self)
        # 创建飞船实例，self是当前AlienInvasion实例
        self.ship = Ship(self)
        # 存储子弹的编组
        self.bullets = pygame.sprite.Group()
        # 存储外星人的编组
        self.aliens = pygame.sprite.Group()
        # 创建一群外星人
        self._create_fleet()
        # 创建play按钮
        self.play_button = Button(self, "START")

    def run_game(self):
        """游戏的主循环"""
        while True:
            # 调用监测鼠标和键盘事件的辅助方法
            self._check_events()
            if self.stats.game_active:
                # 调用飞船的update()方法来更新飞船的位置
                self.ship.update()
                # 调用子弹的update()方法来更新子弹的位置
                self.bullets.update()
                # 删除消失的子弹
                self._update_bullets()
                self._update_aliens()
            # 更新屏幕
            # 更新屏幕要放在最后，以免有内容更新但没有在屏幕上显示
            self._update_screen()
            """让最近绘制的图像可见"""
            # pygame.display.flip()会不断更新屏幕显示并隐去原来位置的元素
            pygame.display.flip()

    """辅助方法，以_开头，在类中执行任务，但不需要通过实例调用"""
    def _check_events(self):
        """监听键盘和鼠标事件"""
        # 事件循环，监听事件并根据事件类型执行相应的任务
        # pygame.event.get()返回一个列表，包含上次被调用之后发生的所有事件
        for event in pygame.event.get():
            # 点击游戏窗口的关闭按钮
            if event.type == pygame.QUIT:
                # 退出游戏
                sys.exit()
            # 按下键盘
            elif event.type == pygame.KEYDOWN:
                # 调用_check_keydown_events()方法
                # 将监测到的event值传给辅助方法，用于判断该执行辅助方法中的哪个语句
                self._check_keydown_events(event)
            # 弹起键盘
            elif event.type == pygame.KEYUP:
                # 调用_check_keyup_events()方法，根据event判断该执行方法中的哪条语句
                self._check_keyup_events(event)
            # 点击鼠标
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标的位置
                mouse_pos = pygame.mouse.get_pos()
                # 调用_check_play_button()方法，根据鼠标位置判断执行方法中的哪条语句
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家点击START时开始新游戏"""
        # pygame.mouse.get_pos()返回一个元组，包含玩家单击时鼠标的x,y坐标
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        """这里使用了rect的方法collidepoint()检查鼠标单击位置是否在Play按钮的rect内。
        如果是，就将game_active设置为True，让游戏开始！"""
        if button_clicked and not self.stats.game_active:
            # 重置游戏设置
            self.settings.initialize_dynamic_settings()
            # 重置游戏统计信息
            self.stats.reset_stats()
            # 将游戏状态设置为True
            self.stats.game_active = True
            # 准备得分图像
            self.sb.prep_score()
            # 确保在开始新游戏时更新等级图像
            self.sb.prep_level()
            # 准备飞船
            self.sb.prep_ships()
            # 清空当前游戏窗口余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人
            self._create_fleet()
            # 将飞船居中
            self.ship.center_ship()
            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """响应按键"""
        # 按下右键
        if event.key == pygame.K_RIGHT:
            # 移动标志设置为True，向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 向左移动
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            # 向上移动
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            # 向下移动
            self.ship.moving_down = True
        # 按Esc退出，想改成其他键，只用改变_后的值
        # 例如K_q，按q退出
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        # 按空格，发射子弹
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开"""
        # 弹起键盘
        if event.key == pygame.K_RIGHT:
            # 停止向右移动
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # 停止向左移动
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            # 停止向上运动
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            # 停止向下运动
            self.ship.moving_down = False

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        # 一次只能发射3颗子弹
        if len(self.bullets) < self.settings.bullet_allowed:
            # 创建新的Bullet类，并将当前AlienInvasion对象传给他
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        # 删除消失的子弹
        """使用for循环遍历列表或编组时，python不允许循环时列表长度改变，所以必须遍历副本"""
        for bullet in self.bullets.copy():
            # 子弹到屏幕顶端
            if bullet.rect.bottom <= 0:
                # 删除子弹
                self.bullets.remove(bullet)
        # 检查子弹和外星人的碰撞
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人发生碰撞"""
        # 删除彼此碰撞的子弹和外星人
        """函数sprite.groupcollide()将一个编组中每个元素的rect同另一个编组中每个元素的rect进行比较。
        在这里，是将每颗子弹的rect同每个外星人的rect进行比较，并返回一个字典，其中包含发生了碰撞的子弹和外星人。
        在这个字典中，每个键都是一颗子弹，而关联的值是被该子弹击中的外星人"""
        # 将bullets和aliens进行比较，看他们是否重叠在一起
        """每当有子弹和外星人的rect重叠时，groupcollide()就在它返回的字典中添加一个键值对。
        两个实参True让Pygame删除发生碰撞的子弹和外星人。"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # 检查字典是否存在
        if collisions:
            # 若存在就遍历其中所有的值，每个值都是一个列表，包含被同一颗子弹击中的所有外星人
            for aliens in collisions.values():
                # 对于每个列表，都将其包含的外星人数量乘以一个外星人的分数，并将结果加入当前得分。
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # 删除现有的子弹
            self.bullets.empty()
            # self.aliens.empty()
            # 新建一群外星人
            self._create_fleet()
            self.settings.increase_speed()
            # 提高等级
            self.stats.level += 1
            # 更新等级
            self.sb.prep_level()

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            # 将ship_left 减一并更新记分牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人，并将飞船放到屏幕底端的中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(2)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘
        更新外星人群中所有外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()
        # 检查外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # 检查是否有外星人到达屏幕底端
        self._check_aliens_bottom()

    def _create_fleet(self):
        """创建外星人"""
        # 创建一个外星人并计算一行可以容纳多少个外星人
        # 外星人的间距为外星人的宽度
        alien = Alien(self)
        # size是一个元组，包含该对象rect的宽和高
        alien_width, alien_height = alien.rect.size
        # 窗口可用的宽度为当前游戏窗口的宽度减去2倍的外星人宽度作为两边的空白
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # 一行可容纳的外星人的数量为窗口可用宽度整除2倍的外星人宽度
        # 一个外星人有自己的宽度和右边的空白
        number_aliens_x = available_space_x // (2 * alien_width)
        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        # 可用的游戏窗口高度 = 当前游戏窗口高度-飞船的高度-一个外星人要占用的高度
        # 这个外星人的高度可以自己调整到符合自己的要求
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        # 当前游戏窗口可以容纳的外星人的行数为可用的游戏窗口高度整除外星人高度的倍数
        # 这个倍数也可以自己设置到符合自己的要求
        number_rows = available_space_y // (4 * alien_height)
        # 创建外星人群
        for row_num in range(number_rows):
            # 从0开始计算到要创建的外星人的行数
            for alien_num in range(number_aliens_x):
                # 内部循环创建一行外星人
                self._create_alien(alien_num, row_num)

    def _create_alien(self, alien_num, row_num):
        """创建一个外星人并将其加入当前行"""
        """除self外，方法_create_alien()还接受另一个参数，即要创建的外星人的编号。
        该方法的代码与_create_fleet()相同，但在内部获取外星人宽度，而不是将其作为参数传入"""
        # 实例化一个外星人对象
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # 外星人的宽度
        alien.x = alien_width + 2 * alien_width * alien_num
        # 外星人群距离游戏窗口左边的距离
        alien.rect.x = alien.x
        # 外星人群距离游戏窗口上方的距离
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_num + 30
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """外星人到达边缘时采取相应措施"""
        # 对外星人群中的每个外星人调用check_edges()方法
        for alien in self.aliens.sprites():
            # alien模块中的check_edges()方法为真
            if alien.check_edges():
                # 改变方向，调用_change_fleet_direction()方法
                self._change_fleet_direction()
                # 退出循环
                break

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            # 外星人到达游戏窗口底端
            if alien.rect.bottom >= screen_rect.bottom:
                # 外星人到底部和撞到飞船一样处理
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """将全部外星人下移，并改变他们的方向"""
        for alien in self.aliens.sprites():
            # 将每个外星人都向下移动fleet_drop_speed个位置
            alien.rect.y += self.settings.fleet_drop_speed
        # 将fleet_direction的值设置成自己*-1就是让整个外星人群改变方向
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新图像"""
        """每次循环时都重绘图像"""
        # 用设置中的背景色填充游戏窗口
        self.screen.fill(self.settings.bg_color)
        # 将飞船绘制在屏幕上
        self.ship.blitme()

        # bullets.sprites()返回一个列表
        # 包含编组bullets中的所有精灵
        for bullet in self.bullets.sprites():
            # 在屏幕上绘制子弹
            bullet.draw_bullet()

        """对编组调用draw()时，Pygame将把编组中的每个元素绘制到属性rect指定的位置。
        方法draw()接受一个参数，这个参数指定了要将编组中的元素绘制到哪个surface上。"""
        self.aliens.draw(self.screen)
        # 显示得分
        self.sb.show_score()
        # 如果游戏处于非活跃状态，就绘制START按钮
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

# 只有在直接运行该文件时，下面的语句才会执行
if __name__ == '__main__':
    """创建游戏实例并运行游戏"""
    # 创建一个AlienInvasion实例
    ai = AlienInvasion()
    # 调用方法运行游戏
    ai.run_game()
