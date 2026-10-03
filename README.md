# Night Ferry

[![Play in your browser](https://img.shields.io/badge/Play-in%20your%20browser-2ea44f)](https://danielstephenson.dev/play/night-ferry)

*One crossing, six passengers, and a cabin booked but empty.*

The night boat to Halde leaves Brekka at eight and comes alongside at six. You are the night steward, taken on this afternoon on the quay; the purser has given you a white jacket, a master key to every cabin, and one rule: cabin 6 is not to be opened.

Cabin 6 was paid for in cash. Nobody has come aboard to claim it.

Night Ferry is a text adventure built on [tak](https://github.com/Stephenson-Software/tak), the text-adventure kit, and a sibling of [Overwinter](https://github.com/Stephenson-Software/Overwinter) and [Tidewater](https://github.com/Stephenson-Software/Tidewater). Ten hours, hour by hour; talk, eavesdrop, open what you shouldn't. Who the empty cabin was for comes out before docking, however you play — and the last page says plainly what you did and what it cost whom. A crossing takes twenty to forty minutes.

When the first crossing ends, the same save can sail again: **the last night boat**, Halde to Brekka in March, five months later, the Kittiwake's final night run before she is sold south. Everything you did in October is remembered there.

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

## The last night boat

From the first crossing's last screen, *Sail the last night boat (March)* starts the second crossing in the same save. The captain is crossing as a passenger in cabin 6, booked in her own name, with a suitcase and a cardboard box tied with string, and the one rule tonight is hers: nobody disturbs six. The mate, Per Aasen, has the ship for one night. The question is where the captain is going, and what is in the box.

It has its own thirteen facts (`Known: n/13`), its own fixed hours (`lastboat/crossing.py`: last orders at eleven, the mate's watch at midnight, Brekka's lights at four, five o'clock, the quay at six), and its own choices: the purser's ledger column, Maren's piano on the car deck and whether her last pupil plays it, whether the mate tells the captain what he always knew, whether Hanne knocks on six. Four endings — **on which days**, **the column**, **over the side**, and **kept from the record**. At five, if nothing has been settled, the mate sends for you and the captain tells you all of it at the stern rail before she puts the choice to you: the failure-proof answer again.

October carries over (`lastboat/carried.py`): how the first crossing ended, whether Hanne knew, whether you told Raske the truth, whether you opened six, whether you still have Maren's letter in your pocket. It changes who is in command, what the purser's winter was like, what Hanne already knows, and every line of the last page. The notebook keeps October's last page.

## Achievements

On [arcade](https://danielstephenson.dev/play), signed-in players earn achievements through `tak.arcade.unlock` (`src/nightferry/achievements.py`): one for each of the eight endings, and some for discoveries — all sixteen things on the first crossing, all thirteen on the last, the answer before four, never opening cabin 6, and a few hidden ones. A save from before achievements existed is credited the first time it is opened. Outside the browser the calls do nothing.

The state is one tier (`state.py`): the minute, where you are, the facts and the time each was learned, the flags (every one named in `flags.py`), and the ending once there is one. The clock is `crossing.py`: it fires the hours of the night — the bar at eleven, the dark saloon at one, Hanne waking at three, the captain at four, the light at five, the quay at six. Scenes and people never compare the clock themselves.

What the saloon and the sea show you is drawn from a seeded sequence, one generator per draw, so a reloaded save sees the same night.

## Saves

Numbered slots under `data/` (or `NIGHTFERRY_SAVE_DIR`), one `save.json` each, validated against `schemas/save.json` on every load and save. Saves made by 0.1.0 (schema version 1, one crossing) load unchanged: `state.migrate()` brings them forward in memory, and the next save writes them as version 2, which adds `crossing` and `past` (the first crossing as it ended). `tests/fixtures/saves-0.1.0/` holds saves written by 0.1.0 itself, and `tests/test_save_compat.py` loads, plays on and sails the last boat from each. A save that can't be read is listed as damaged, never overwritten, and copied aside if you open it anyway. In the browser, saves live in IndexedDB (`night-ferry-saves`) and the page's Saves control downloads or loads them as a file.

## Development

```bash
pip install pytest pytest-cov -r requirements.txt
./test.sh
```

`tests/routes.py` holds scripted crossings — the canonical solve, the do-nothing night, the kept secret, and the last boat's canonical — and `tests/test_game.py`, `tests/test_endings.py` and `tests/test_lastboat.py` play them through a scripted front-end to each ending; if a menu label moves or a gate breaks, those tests say which. `tests/test_achievements.py` plays them with `tak.arcade` mocked and checks that every achievement is earned by some route.

## License
This project is licensed under the **Stephenson Software Non-Commercial License (Stephenson-NC)**.  
© 2026 Daniel McCoy Stephenson. All rights reserved.  

You may use, modify, and share this software for **non-commercial purposes only**.  
Commercial use is prohibited without explicit written permission from the copyright holder.  

Full license text: [Stephenson-NC License](https://github.com/Stephenson-Software/stephenson-nc-license) (also in [LICENSE](LICENSE))  
SPDX Identifier: `Stephenson-NC`
