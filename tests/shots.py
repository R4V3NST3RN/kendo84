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
    pg.evaluate("__K.render()");shot('s_title')
    pg.evaluate("Math.random=(()=>{let s=7;return()=>{s=(s*16807)%2147483647;return s/2147483647;}})();const K=__K;K.S.demo=true;K.S.mode=1;K.S.stage=3;K.S.sceneI=1;K.newMatch();")
    def run_until(cond,maxn=4000):
        return pg.evaluate("([c,m])=>{const K=__K;for(let i=0;i<m;i++){K.update();if(eval(c))return i;}return -1}",[cond,maxn])
    run_until("K.M.t===20");pg.evaluate("__K.render()");shot('s_rei')
    run_until("K.M.t===100");pg.evaluate("__K.render()");shot('s_sonkyo')
    run_until("K.M.t===125");pg.evaluate("__K.render()");shot('s_hajime')
    print('fight frames', run_until("K.M.ph==='fight'&&(K.M.a.st==='attack'||K.M.b.st==='attack')&&K.M.t>10"))
    run_until("(K.M.a.st==='attack'&&K.M.a.mt===9)||(K.M.b.st==='attack'&&K.M.b.mt===9)");pg.evaluate("__K.render()");shot('s_strike')
    print('hitstop', run_until("K.M.ph==='hitstop'"))
    pg.evaluate("__K.update();__K.render()");shot('s_flags')
    run_until("K.M.ph==='award'&&K.M.t===30");pg.evaluate("__K.render()");shot('s_award')
    run_until("K.M.ph==='resume'");pg.evaluate("__K.render()");shot('s_nihonme')
    print('win', run_until("K.M&&K.M.ph==='win'&&K.M.t===20",8000));pg.evaluate("__K.render()");shot('s_shobuari')
    run_until("K.M&&K.M.ph==='win'&&K.M.seated&&K.M.t-K.M.seated===95",3000);pg.evaluate("__K.render()");shot('s_rei_end')
    # results screens
    pg.evaluate("const K=__K;K.S.demo=false;K.S.stage=7;K.S.score=12345;K.S.screen='result';K.render;");
    pg.evaluate("__K.S.screen='result';Object.assign(__K,{});")
    pg.evaluate("(()=>{const K=__K;K.S.screen='match';K.newMatch();})()")
    b.close()
    print('errors',errs)
