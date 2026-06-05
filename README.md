<h1 align="center">PMatrix</h1>

<h3 align="center">Matrix rain + a Pomodoro timer, in your terminal</h3>

<p align="center">
The green rain falls while you work. When the pomodoro ends the rain <b>freezes</b>
and a big break countdown takes over the screen. When the break is over, the rain
falls again — so a glance at your terminal tells you whether it's time to focus or rest.
</p>

<p align="center">
  <a href="./COPYING">
    <img src="https://img.shields.io/github/license/immalleable/pmatrix?color=blue">
  </a>
  <img src="https://img.shields.io/badge/contributions-welcome-orange">
  <a href="https://github.com/immalleable/pmatrix/stargazers">
    <img src="https://img.shields.io/github/stars/immalleable/pmatrix">
  </a>
  <a href="https://github.com/immalleable/pmatrix/network">
    <img src="https://img.shields.io/github/forks/immalleable/pmatrix">
  </a>
</p>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## Contents
- [Overview](#cloud-overview)
- [Pomodoro usage](#tomato-pomodoro-usage)
- [Build dependencies](#open_file_folder-build-dependencies)
- [Building and installing](#floppy_disk-building-and-installing)
- [All options](#bookmark_tabs-all-options)
- [Credits](#busts_in_silhouette-credits)
- [License](#page_facing_up-license)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## :cloud: Overview

PMatrix is a fork of [CMatrix](https://github.com/abishekvashok/cmatrix) — the
"Matrix" rain screensaver for the terminal — with a built-in
[Pomodoro](https://en.wikipedia.org/wiki/Pomodoro_Technique) timer wired into the
animation:

- **Work phase** — the rain falls as usual, with a large block-digit countdown
  (`POMODORO #N` + `MM:SS`) in the top-right corner.
- **Break phase** — the rain freezes and a big centered `BREAK` banner with its
  own countdown takes the screen, so you actually step away.
- The cycle repeats, counting your pomodoros, until you quit.

Everything CMatrix could do (colors, bold, async scroll, lambda/rainbow modes,
custom speed, screensaver mode, …) still works — the binary is just named
`pmatrix`. Pass `-W 0` to disable the timer entirely and get plain rain.

> :grey_exclamation: `Disclaimer`: Not affiliated with the movie "The Matrix",
> Warner Bros, or any of its affiliates. Just fans.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## :tomato: Pomodoro usage

```sh
pmatrix              # 25 min work / 5 min break (defaults)
pmatrix -W 50 -R 10  # 50 min work / 10 min break
pmatrix -W 0         # disable the timer (plain cmatrix-style rain)
```

Keys while running:

| Key | Work phase | Break phase |
|---|---|---|
| `space` / `p` / `P` | Pause — freezes the rain **and** the work clock (`PAUSED #N`) | Pause — freezes the break countdown (`P A U S E D`) |
| `s` / `S` | Skip straight to the break | End the break early, start the next pomodoro |
| `q` | Quit | Quit |

All the original CMatrix runtime keys (`b`/`B`/`n` bold, `a` async, `1`–`9`
speed, `!@#$%^&` colors, `r` rainbow, `m` lambda, …) still work too.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## :open_file_folder: Build dependencies

You need a wide-character ncurses library. On Linux, check with:

```sh
ldconfig -p | grep ncurses
```

If you get no output, install ncurses (e.g. `sudo apt install libncurses-dev`
on Debian/Ubuntu). On Windows, `mingw-w64-ncurses` is recommended.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## :floppy_disk: Building and installing

Clone the repo, then use either build system from inside the `pmatrix` directory.

#### :small_blue_diamond: Using `configure` (recommended for most Linux/MinGW users)
```sh
autoreconf -i   # skip if building from a released tarball
./configure
make
sudo make install
```

#### :small_blue_diamond: Using CMake
```sh
mkdir -p build && cd build
cmake ..                              # installs to /usr/local
# cmake -DCMAKE_INSTALL_PREFIX=/usr .. # ...or to /usr
make
sudo make install
```

Then just run:

```sh
pmatrix
```

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## :bookmark_tabs: All options

```sh
pmatrix [-abBcfhlLnsmVxk] [-u delay] [-C color] [-t tty] [-M message] [-W mins] [-R mins]
```

| Flag | Meaning |
|---|---|
| `-W [mins]` | Pomodoro work duration (default 25, `0` disables the timer) |
| `-R [mins]` | Pomodoro break duration (default 5) |
| `-a` | Asynchronous scroll |
| `-b` / `-B` | Bold characters / all-bold |
| `-c` | Japanese characters (needs an appropriate font) |
| `-l` | Linux mode (matrix console font) |
| `-o` | Old-style scrolling |
| `-s` | Screensaver mode (exits on first keystroke) |
| `-u delay` | Screen update delay, `0`–`10` (default 4) |
| `-C [color]` | Rain color (default green) |
| `-r` / `-m` | Rainbow mode / lambda mode |
| `-M [message]` | Print a message in the center of the screen |
| `-V` | Version, `-h` help |

For the full list run `pmatrix -h` or read `man pmatrix`.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## :busts_in_silhouette: Credits

PMatrix is built on top of [CMatrix](https://github.com/abishekvashok/cmatrix),
written by **Chris Allegretta** and maintained by **Abishek V Ashok**, along with
all of its contributors. All of their work — and the GPL-3.0 license — carries
through here. Huge thanks to them; the pomodoro layer is just a thin addition on
a great program.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

## :page_facing_up: License

GNU GPL v3, same as the upstream CMatrix project. [View License](./COPYING)
