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
    pg.evaluate("const K=__K;for(let i=0;i<40;i++)K.update();K.S.menu=2;K.render()");shot('tr_menu')
    pg.evaluate("const K=__K;K.startTraining();for(let i=0;i<30;i++){K.keys.add('KeyD');K.update();}K.keys.delete('KeyD');K.render()");shot('tr_reach')
    pg.evaluate("const K=__K;K.nextLesson();K.nextLesson();for(let i=0;i<14;i++){K.keys.add('KeyD');K.update();}K.keys.delete('KeyD');K.render()");shot('tr_men')
    pg.evaluate("""const K=__K;const T=K.T;for(let i=0;i<60;i++){const d=Math.abs(T.p.x-T.f.x);if(d>65)K.keys.add('KeyD');else K.keys.delete('KeyD');K.update();}
      K.keys.add('KeyF');K.pressed.add('KeyF');K.update();K.keys.delete('KeyF');K.pressed.clear();for(let i=0;i<14;i++)K.update();K.render();""");shot('tr_men_hit')
    pg.evaluate("const K=__K;for(let i=0;i<6;i++)K.nextLesson();const T=K.T;for(let i=0;i<70;i++)K.update();K.render()");shot('tr_tell')
    pg.evaluate("const K=__K;for(let i=0;i<4;i++)K.nextLesson();K.render()");shot('tr_hiki')
    pg.evaluate("const K=__K;K.nextLesson();K.nextLesson();for(let i=0;i<120;i++)K.update();K.render()");shot('tr_done')
    print('errors',errs)
    b.close()
