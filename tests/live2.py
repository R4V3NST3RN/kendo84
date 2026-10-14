import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
os.chdir(ROOT)
TEST_URL = (ROOT / 'test.html').as_uri()   # build with: sh src/build.sh
GAME_URL = (ROOT / 'index.html').as_uri()
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1100,'height':900})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(GAME_URL);pg.wait_for_timeout(500)
    pg.click('#bTrain');pg.wait_for_timeout(300)
    pg.keyboard.down('KeyD');pg.wait_for_timeout(600);pg.keyboard.up('KeyD');pg.wait_for_timeout(200)
    pg.locator('#game').screenshot(path='tests/live_train.png')
    pg.screenshot(path='tests/live_train_page.png')
    print('errors',errs)
    b.close()
