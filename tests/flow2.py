import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
os.chdir(ROOT)
TEST_URL = (ROOT / 'test.html').as_uri()   # build with: sh src/build.sh
GAME_URL = (ROOT / 'index.html').as_uri()
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1100,'height':800})
    pg.add_init_script("window.requestAnimationFrame=()=>0")
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(TEST_URL);pg.wait_for_timeout(300)
    shot=lambda n:pg.locator('#game').screenshot(path=f'tests/{n}.png')
    pg.evaluate(open('tests/runhelper.js').read())
    pg.evaluate("const K=__K;K.S.demo=false;K.startGame(2)")
    pg.evaluate("run(150,[],null)");pg.evaluate("__K.M.time=30")
    print(pg.evaluate("run(6000,[],\"K.M.ph==='hantei'\")"))
    pg.evaluate("__K.update();__K.render()");shot('f_hantei')
    print(pg.evaluate("run(800,[],\"K.S.screen==='result'\")"))
    # 1P: player sits still; AI should win; check game over screen
    pg.evaluate("const K=__K;K.S.screen='title';K.startGame(1)")
    print(pg.evaluate("run(9000,[],\"K.S.screen==='result'\")"))
    pg.evaluate("__K.render()");shot('f_over')
    print('errors',errs)
    b.close()
