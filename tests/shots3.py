import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
os.chdir(ROOT)
TEST_URL = (ROOT / 'test.html').as_uri()   # build with: sh src/build.sh
GAME_URL = (ROOT / 'index.html').as_uri()
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1100,'height':800})
    pg.add_init_script("window.requestAnimationFrame=()=>0")
    pg.goto(TEST_URL);pg.wait_for_timeout(300)
    for sc in [2,3]:
        pg.evaluate(f"const K=__K;K.S.demo=true;K.S.mode=1;K.S.sceneI={sc};K.newMatch();for(let i=0;i<190;i++)K.update();K.render();")
        pg.locator('#game').screenshot(path=f'tests/scene{sc}.png')
    b.close()
