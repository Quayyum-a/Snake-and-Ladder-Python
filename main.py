import asyncio
import platform
from controller.game_controller import GameController
from model.board import Board
from model.player import Player
from view.game_view import GameView

FPS = 60

async def main():
    # Initialize game components
    board = Board()
    players = [Player("Player 1", (255, 0, 0)), Player("Player 2", (0, 0, 255))]
    view = GameView()
    controller = GameController(board, players, view)

    # Main game loop
    while True:
        controller.update()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())