﻿class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()
        # 让游戏一开始处于非活跃状态
        self.game_active = False
        # 任何时候都不应该重置最高得分
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的信息"""
        # 统计信息ships_left指出玩家是否用完了所有的飞船。
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

