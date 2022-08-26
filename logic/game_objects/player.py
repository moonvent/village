from logic.game_objects.action import ActionType
from logic.game_objects.character.character import Character
from logic.game_objects.position import Position
from logic.game_objects.character.moving import PlayerMovingMixin, MoveDirection


class Player(Character,
             PlayerMovingMixin):
    _handle_point: Position = None
    # точка персонажа на карте, то, где его будут обрабатывать (на данный момент низ топ)

    def __init__(self):
        super().__init__()
        PlayerMovingMixin.__init__(self)
        self.spawn_point = Position(0, 0)
        self.Direction = MoveDirection.Right
        # self.handle_point = self.rect.midbottom
        self.handle_point = self.rect.midbottom

    @property
    def handle_point(self):
        return self._handle_point

    @handle_point.setter
    def handle_point(self, value: tuple[int, int] | Position):
        self._handle_point = value if isinstance(value, Position) else Position(*value)

    @property
    def coords(self) -> Position:
        return Position(self.rect.x + self.handle_point.x,
                        self.rect.y + self.handle_point.y)

    @coords.setter
    def coords(self, value):
        raise NotImplemented

    def moving(self, action_type: ActionType):
        super(Player, self).moving(action_type)
        self.update()
        self.stop(swap_sprite=False,
                  action_type=action_type)

