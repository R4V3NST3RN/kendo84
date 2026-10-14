import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
os.chdir(ROOT)
TEST_URL = (ROOT / 'test.html').as_uri()   # build with: sh src/build.sh
GAME_URL = (ROOT / 'index.html').as_uri()
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page()
    pg.add_init_script("window.requestAnimationFrame=()=>0")
    pg.goto(TEST_URL);pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>{const K=__K;K.S.demo=true;K.S.mode=1;K.newMatch();for(let i=0;i<300;i++)K.update();
      let t=performance.now();for(let i=0;i<600;i++){K.update();K.render();}const tr=(performance.now()-t)/600;
      t=performance.now();for(let i=0;i<600;i++){K.update();}const tu=(performance.now()-t)/600;return {renderPlusUpdate_ms:tr.toFixed(3),update_ms:tu.toFixed(3)};}"""))
    b.close()
