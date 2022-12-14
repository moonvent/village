from src.logic.game_objects.character.mechanics.directions import MoveDirection


class Literals:
    a = 'a'
    b = 'b'
    c = 'c'
    d = 'd'
    e = 'e'
    f = 'f'
    g = 'g'
    h = 'h'
    i = 'i'
    j = 'j'
    k = 'k'
    l = 'l'
    m = 'm'
    n = 'n'
    o = 'o'
    p = 'p'
    q = 'q'
    r = 'r'
    s = 's'
    t = 't'
    u = 'u'
    v = 'v'
    w = 'w'


lcode = Literals


class Sides:
    """
        стороны в которые можно пройти, начиная всегда с левой
    """

    All = (MoveDirection.Left, MoveDirection.Up, MoveDirection.Right, MoveDirection.Down)
    Left = (MoveDirection.Left,)
    Top = (MoveDirection.Up,)
    Right = (MoveDirection.Right,)
    Bottom = (MoveDirection.Down,)
    RightBottom = (MoveDirection.Right, MoveDirection.Down)


class Location:
    _pattern: tuple[str, ...] = None
    _available_sides: tuple[MoveDirection, ...] = None
    _next_locations: tuple = None  # кортеж с индексами следующих локаций

    # (индексами в кортеже locations), строго в той последовательности, что и стороны,
    # то есть сторона индекс 0 - к ней локация с таким же индексом

    def __init__(self,
                 pattern: tuple[str, ...],
                 sides: tuple[MoveDirection, ...],
                 next_locations: tuple):
        self._pattern = pattern
        self._available_sides = sides
        self._next_locations = next_locations

    @property
    def pattern(self):
        return self._pattern

    @property
    def available_sides(self):
        return self._available_sides

    @property
    def next_locations(self):
        return self._next_locations


class Locations:
    """
        Locations in game, all locations have a 14 columns and 5 rows
    """
    _locations: tuple[Location] = None

    def __init__(self,
                 locations: tuple[Location, ...]):
        self._locations = locations

    @property
    def locations(self):
        return self._locations

    def __getitem__(self, item: int) -> Location:
        return self._locations[item]


locations = Locations(locations=(
    Location(pattern=(
        'jnnnnnnnnnnnnn',
        'kggeggeggggggg',
        'kfggmjgggggggg',
        'kjopqkopqropqr',
        'kkgggklggggggg',
    ), sides=Sides.RightBottom,
        next_locations=(1, 2,)),
    Location(pattern=(
        'nnnnnnnnnnnnnj',
        'ggggggggggwtwk',
        'ggggggggggvuvk',
        'opqropqropqgok',
        'gggggggggggggi',
    ), sides=Sides.Left,
        next_locations=(0,)),
    Location(pattern=(
        'iissskgggggggg',
        'ssssskgggggggg',
        'sssgmigggggggg',
        'gggggggggggggg',
        'gggggggggggggg',
    ), sides=Sides.Top,
        next_locations=(0,)),
    )
)


