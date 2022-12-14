import os

from pygame import Surface
from pygame.sprite import Sprite, Group

from src.logic.game_objects.character.player import Player

from src.logic.game_objects.map.element import MapElement, MapElementInGame, MapElements
from src.logic.game_objects.map.location_patterns import Location, locations
from src.services.constants import Folders, GameConstants
from src.services.load_resources import load_image


class Map:
    _elements_group: Group = None
    _display_surface: Surface = None
    _elements: dict[tuple[int, int], MapElementInGame] = None
    _update_after_player: list[Sprite] = None
    _location: Location = None
    _player: Player = None

    def __init__(self,
                 surface: Surface,
                 location: Location,
                 player: Player
                 ):
        self._display_surface = surface
        self._player = player
        self._location = location

        self._elements = {}
        self._elements_group = Group()

        self._create_map()

    @property
    def player(self):
        return self._player

    @property
    def location(self):
        return self._location

    @property
    def map_surface(self):
        return self._display_surface

    @property
    def map_elements(self) -> dict[tuple[int, int], MapElementInGame]:
        return self._elements

    def get_element_by_coords(self,
                              x: int,
                              y: int) -> MapElementInGame | None:
        """
            Получение элемента карты с помощью координат которые передаются
        :param x:
        :param y:
        :return: элементв в списке элементов
        """
        x = x // GameConstants.WidthMapElement * GameConstants.WidthMapElement
        y = y // GameConstants.HeightMapElement * GameConstants.HeightMapElement
        return self.map_elements.get((x, y))

    def change_location(self, location: Location):
        self._location = location
        self._create_map()

    def _create_map(self):
        """
            Создание карты, параллельно добавление всех элементов по координатам в словарь
        :return:
        """
        self._elements_group.empty()

        for row_number, row in enumerate(self._location.pattern):
            for column_number, element in enumerate(row):

                if map_element_const := MapElements.get(element):

                    sprites_path, sprites = [], []
                    if isinstance(map_element_const.path, str):
                        sprites_path.append(map_element_const.path)
                    else:
                        sprites_path = map_element_const.path

                    for path_to_sprite in sprites_path:
                        path_to_image = os.path.join(Folders.Map.value, path_to_sprite)
                        element_preset, _ = load_image(path_to_image)
                        sprites.append(element_preset)

                    x, y = column_number * GameConstants.WidthMapElement, row_number * GameConstants.HeightMapElement

                    map_element = MapElement(x, y, sprites[0])

                    additional_sprites = tuple(MapElement(x, y, surface, constant=True) for surface in sprites[1:])

                    self._elements[(x, y)] = MapElementInGame(sprite=map_element,
                                                              action_type=map_element_const.action_type,
                                                              additional_sprites=additional_sprites,
                                                              map_level=map_element_const.map_level,
                                                              code=element,
                                                              directions=map_element_const.directions,
                                                              available_walk_side=map_element_const.available_walk_side)

                    for map_elem in (map_element, *additional_sprites):
                        self._elements_group.add(map_elem)

    def draw(self):
        self._elements_group.draw(self._display_surface)

    def repaint(self,
                player: Player) -> tuple:
        actual_coords = player.coords
        nearby_rects = (-1, 0, 1)
        last_element = from_point = to_point = None

        self._update_after_player = []

        for row_element in nearby_rects:
            for column_element in nearby_rects:

                elements_coords = ((actual_coords.x // GameConstants.WidthMapElement + row_element) * GameConstants.WidthMapElement,
                                   (actual_coords.y // GameConstants.HeightMapElement + column_element) * GameConstants.HeightMapElement)

                if element := self._elements.get(elements_coords):
                    element: MapElementInGame = element

                    self._update_after_player += list(element.additional_sprites)
                    self.map_surface.blit(element.sprite.image,
                                          element.sprite.rect)

                    # для обновления определенной области
                    last_element = element
                    if not from_point:
                        from_point = elements_coords
        else:
            to_point = (last_element.sprite.rect.x + last_element.sprite.rect.width,
                        last_element.sprite.rect.y + last_element.sprite.rect.height,)

        return from_point, to_point

    def update_after_player(self):
        for sprite in self._update_after_player:
            self.map_surface.blit(sprite.image,
                                  sprite.rect)

    def player_achieve_end_of_location(self):
        """
            Обновляем локацию и обновляем экран если игрок пришел к границе локации
            :return: обновляем ли ВЕСЬ экран (из-за смены локации) или нет
        """
        if self.player.direction in self.location.available_sides:
            next_location = locations[self.location.next_locations[self.location.available_sides.index(self.player.direction)]]
            self.change_location(location=next_location)
            self.draw()
            return True


map_object = Map
