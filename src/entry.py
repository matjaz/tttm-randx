import random
from js import Response
from urllib.parse import urlparse, parse_qs

async def on_fetch(request):
    url = urlparse(request.url)
    params = parse_qs(url.query)

    if "gid" in params:
        moves = params["moves"][0] if "moves" in params else None
        size = int(params["size"][0]) if "size" in params else 3
        game = Game(
            params["playing"][0],
            Game.parse_moves(moves, size),
            size
        )
        move = game.suggested_move()

        return Response.new(move)

    return Response.new("This is tttm-randx. Because x is before y")

# borrowed from https://github.com/otobrglez/tttm-randy
class Game:
    move_separator = "_"
    position_separator = "-"

    def __init__(self, playing, moves, size):
        self.playing = playing
        self.moves = moves
        self.size = size

    @staticmethod
    def parse_moves(raw: str, size: int) -> list[tuple[str, tuple[int, int]]]:
        if raw is None or raw == "":
            return []

        return [(symbol, (int(x), int(y))) for symbol, x, y in
                [x.split(Game.position_separator, maxsplit=3) for x in
                 raw.split(Game.move_separator, maxsplit=size * size)]]

    def moves_dict(self):
        return {pos: symbol for symbol, pos in self.moves}

    def grid(self) -> list[tuple[None, tuple[int, int]]]:
        return [(self.moves_dict().get((x, y), None), (x, y)) for x in range(self.size)
                for y in range(self.size)]

    def render_move(self, m) -> str:
        return f"Move:{self.playing}{Game.position_separator}{m[0]}{Game.position_separator}{m[1]}"

    def suggested_move(self) -> str:
        possible_moves = [position for (symbol, position) in self.grid() if
                          symbol is None]
        random_choice = random.choice(possible_moves)
        return self.render_move(random_choice)
