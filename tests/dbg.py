import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
os.chdir(ROOT)
TEST_URL = (ROOT / 'test.html').as_uri()   # build with: sh src/build.sh
GAME_URL = (ROOT / 'index.html').as_uri()
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page()
    pg.add_init_script("window.requestAnimationFrame=()=>0")
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(TEST_URL);pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>{const K=__K;K.startTraining();for(let i=0;i<8;i++)K.nextLesson();const T=K.T,o=[];
      for(let i=0;i<200;i++){K.update();if(i%20===0)o.push([i,T.L.t,T.ph,T.pn,T.pnext,T.p.st,T.f.st,K.S.paused,K.S.screen].join(','));}return o;}"""))
    print(errs)
    b.close()
