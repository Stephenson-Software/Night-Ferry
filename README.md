# Night Ferry

*One crossing, six passengers, and a cabin booked but empty.*

The night boat to Halde leaves Brekka at eight and comes alongside at six. You are the night steward, taken on this afternoon on the quay; the purser has given you a white jacket, a master key to every cabin, and one rule: cabin 6 is not to be opened.

Cabin 6 was paid for in cash. Nobody has come aboard to claim it.

Night Ferry is a text adventure built on [tak](https://github.com/Stephenson-Software/tak), the text-adventure kit, and a sibling of [Overwinter](https://github.com/Stephenson-Software/Overwinter) and [Tidewater](https://github.com/Stephenson-Software/Tidewater). Ten hours, hour by hour; talk, eavesdrop, open what you shouldn't. Who the empty cabin was for comes out before docking, however you play — and the last page says plainly what you did and what it cost whom. A crossing takes twenty to forty minutes.

## Play

`pip install -r requirements.txt` needs `git` on your PATH: the kit is installed from a pinned commit on GitHub.

**In your browser** — the game runs in your tab, saves live in your browser:

```bash
pip install -r requirements.txt
python3 web/build_zip.py     # once, and after any src/ change or tak upgrade
python3 web/serve.py         # then open http://127.0.0.1:8080
```

**In a terminal:**

```bash
pip install -r requirements.txt
./run.sh                     # or: PYTHONPATH=src python -m nightferry
```

**As a server** (the browser is a terminal for a game running on your machine; everyone who opens the page shares it): `./run.sh web`, then open `http://127.0.0.1:8000`. `NIGHTFERRY_WEB_HOST`/`NIGHTFERRY_WEB_PORT` move either server.

Hosted, it is deployed to [arcade](https://github.com/Stephenson-Software/arcade) by `.github/workflows/arcade.yml`.

## The story

A boat, a booking, and eight people who each know part of why a schoolteacher's name is on the door of cabin 6. The game tells it in pieces; the notebook's "What is happening to you" page assembles the pieces you have found, in plain words, from the first minute. The whole of it, spoilers included, is in [docs/STORY.md](docs/STORY.md).

## How it works

The crossing is ten hours long. Moving about the boat is free; everything you *do* — a conversation in which you ask anything, a look, a door — costs twenty minutes, and the header counts the hours to the quay. Five places: the saloon, the car deck, the cabin corridor, the open deck, the wheelhouse. People are where the hour puts them: the doctor goes to his cabin when the bar shuts, the woman with two tickets sleeps when the saloon goes dark, the purser leaves his hatch when he walks the boat.

Some of what you hear is a **fact**, and facts go in your notebook and open new questions on other people's menus. Facts point at each other, Outer Wilds fashion: under each one the notebook lists where it leads that you haven't been, without naming what is there. There are sixteen (`Known: n/16` in the header), all sixteen can be learned on one crossing, and the trail from the booking to the bridge is six of them long.

Some of what people ask you is a **choice**, not a question. *Hanne will remember that.* Every passenger, the purser and the captain has one: keep the captain's secret or say Hanne should know; let the lorry driver sleep in cabin 6; carry the nurse's letter yourself or take her up to give it; tell the company's man what the bookings were — which clears the purser and names the captain — or say you know nothing; and when Hanne asks what you would do, answer her.

Four endings — **off the light**, **beside Arne**, **at the door**, and **the kept crossing** — and each one's last page says what happened, who cabin 6 was for, what you did, and what it cost each person on the boat, by name. If nobody has told Hanne by four in the morning, and you have not promised the captain to keep it, the captain comes down to cabin 6 herself and it comes out in the corridor: a player who never asks a question still hears the whole answer before the boat docks.

The state is one tier (`state.py`): the minute, where you are, the facts and the time each was learned, the flags (every one named in `flags.py`), and the ending once there is one. The clock is `crossing.py`: it fires the hours of the night — the bar at eleven, the dark saloon at one, Hanne waking at three, the captain at four, the light at five, the quay at six. Scenes and people never compare the clock themselves.

What the saloon and the sea show you is drawn from a seeded sequence, one generator per draw, so a reloaded save sees the same night.

## Saves

Numbered slots under `data/` (or `NIGHTFERRY_SAVE_DIR`), one `save.json` each, validated against `schemas/save.json` on every load and save. A save that can't be read is listed as damaged, never overwritten, and copied aside if you open it anyway. In the browser, saves live in IndexedDB (`night-ferry-saves`) and the page's Saves control downloads or loads them as a file.

## Development

```bash
pip install pytest pytest-cov -r requirements.txt
./test.sh
```

`tests/routes.py` holds scripted crossings — the canonical solve, the do-nothing night, the kept secret — and `tests/test_game.py` and `tests/test_endings.py` play them through a scripted front-end to each ending; if a menu label moves or a gate breaks, those tests say which.

## License
This project is licensed under the **Stephenson Software Non-Commercial License (Stephenson-NC)**.  
© 2026 Daniel McCoy Stephenson. All rights reserved.  

You may use, modify, and share this software for **non-commercial purposes only**.  
Commercial use is prohibited without explicit written permission from the copyright holder.  

Full license text: [Stephenson-NC License](https://github.com/Stephenson-Software/stephenson-nc-license) (also in [LICENSE](LICENSE))  
SPDX Identifier: `Stephenson-NC`
