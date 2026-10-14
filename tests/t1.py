import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
os.chdir(ROOT)
TEST_URL = (ROOT / 'test.html').as_uri()   # build with: sh src/build.sh
GAME_URL = (ROOT / 'index.html').as_uri()
import json,sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1100,'height':900})
    errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('console',lambda m:errs.append('console:'+m.text) if m.type=='error' else None)
    pg.goto(TEST_URL)
    pg.wait_for_timeout(800)
    print('errors',errs)
    r=pg.evaluate("Object.fromEntries(Object.entries(__K.MOVES).map(([k,m])=>[k,m.rng]))")
    print(json.dumps(r))
    pg.screenshot(path='tests/title.png')
    b.close()
