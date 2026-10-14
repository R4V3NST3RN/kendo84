import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
os.chdir(ROOT)
TEST_URL = (ROOT / 'test.html').as_uri()   # build with: sh src/build.sh
GAME_URL = (ROOT / 'index.html').as_uri()
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1100,'height':900})
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(GAME_URL);pg.wait_for_timeout(600)
    pg.click('#game');pg.wait_for_timeout(200)
    pg.keyboard.press('Enter');pg.wait_for_timeout(2700)
    pg.keyboard.down('KeyD');pg.wait_for_timeout(250);pg.keyboard.up('KeyD')
    pg.keyboard.press('KeyF');pg.wait_for_timeout(170)
    pg.locator('#game').screenshot(path='tests/live1.png')
    pg.wait_for_timeout(800)
    pg.keyboard.press('KeyP');pg.wait_for_timeout(100)
    pg.screenshot(path='tests/live_page.png',full_page=True)
    print('errors',errs)
    b.close()
