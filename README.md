# The Best Game Evahh

A two-player Pygame platform game. Players are linked by a spring and must climb
above the rising water. The level, sprites, background, and sounds are included
in this repository.

## Play in a browser

The game is packaged for WebAssembly with [Pygbag](https://github.com/pygame-web/pygbag).
Once the Pages workflow is enabled and has deployed, open:

<https://connorsawaya.github.io/Sawaya_Connor_my_game_spr2026/>

In the repository settings, set **Settings → Pages → Build and deployment → Source**
to **GitHub Actions** before the first deployment.

The browser build runs the Python/Pygame game through WebAssembly. Its first load
downloads the Pygbag runtime from `pygame-web.github.io`; sound starts after a
keyboard interaction if the browser blocks audio autoplay.

## Controls

- Player 1: `A` / `D` to move, `W` to jump.
- Player 2: arrow keys to move and jump.
- `P` pauses. After game over, press a key to restart.

## Run on desktop

Requires Python 3.10+ and Pygame Community Edition:

```sh
python -m pip install pygame-ce
python main.py
```

## License

MIT. See [LICENSE](LICENSE).

