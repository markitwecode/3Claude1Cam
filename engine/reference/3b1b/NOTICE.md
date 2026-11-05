# Notice: material derived from 3Blue1Brown's code

The files below are derived from Grant Sanderson's video code,
[3b1b/videos](https://github.com/3b1b/videos) (© 3Blue1Brown LLC). That code is licensed under
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), and these files are shared under
the same licence. You must credit 3Blue1Brown, and you may not use them commercially. Anything you adapt
from them must be shared under the same licence.

| File | What it is |
|---|---|
| `PATTERNS.md` | How he paces, builds and reveals ideas, measured from his 2023–2026 code. It has short quoted snippets and `file:line` citations into 3b1b/videos @ 306a134 |
| `GL_TO_CE.md` | His most-used ManimGL APIs, with use counts, translated to ManimCE 0.22 and checked against its source |
| `MUSIC.md` | How music is used in his videos, from YouTube captions, his end-screen code and our measurements of the album. It contains no audio |
| `ce_ports.py` | ManimCE ports of ManimGL helpers he uses often |
| `tools/` | Our scripts that measure his code, captions and the album, and their JSON outputs |

The changes: everything here was measured, summarised, or ported from ManimGL to ManimCE. Nothing is
copied wholesale.

`ce_ports.py`, and the API names in `GL_TO_CE.md`, follow the source of ManimGL itself
([3b1b/manim](https://github.com/3b1b/manim)), which is under the MIT License. That licence's notice
applies to those portions:

> MIT License. Copyright (c) 2020-2026 3Blue1Brown LLC
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
> associated documentation files (the "Software"), to deal in the Software without restriction,
> including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
> and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
> subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial
> portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
> LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
> NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
> WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
> SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## What isn't redistributed
- **`videos/` and `manimgl/`** are local clones of 3b1b/videos (@ 306a134) and 3b1b/manim (@ fafa083),
  for reading only. To follow the citations, clone them yourself (commands in `docs/SETUP.md`, §4,
  "Reference clones"). Rename `videos/CLAUDE.md` to `GRANT_CLAUDE.md.txt` straight after cloning, so
  Claude Code doesn't load it as instructions.
- **In `study/`**, the data (`data/`, `load/`) and the scripts (`tools/`) are our own measurements:
  speech and motion activity per video, idea and load codings, and the tables built from them
  (`docs/3b1b-study.md`, `docs/load-calibration.md`). The contact sheets of frames from his videos
  (`study/sheets/`) and anything downloaded to measure (`study/dl/`) aren't redistributed, and no video
  or audio of his is.
- **`_scratch_media/`** holds local test renders.
