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
    upd=lambda n:pg.evaluate("n=>{for(let i=0;i<n;i++)__K.update();__K.render();}",n)
    upd(160);shot('s_title2')
    pg.evaluate("const K=__K;K.S.mode=1;K.S.demo=false;K.S.stage=6;K.S.score=15400;K.S.screen='result';K.setR({kind:'promo',t:50,tb:1450});K.render()");shot('s_promo')
    pg.evaluate("const K=__K;K.setR({kind:'over',t:80});K.S.newHi=false;K.render()");shot('s_over')
    pg.evaluate("const K=__K;K.S.tally=[3,2];K.setR({kind:'tally',w:'aka',t:80});K.render()");shot('s_tally')
    pg.evaluate("__K.S.stage=4;__K.startBonus()");upd(60);shot('b_ready')
    # play bonus: watch for open, press the right key
    r=pg.evaluate("""()=>{const K=__K,B0=K.B;const keyFor={men:['KeyF'],kote:['KeyS','KeyF'],do:['KeyG']};let shots=[];let snap=null;
      for(let i=0;i<4000&&K.S.screen==='bonus';i++){
        const B=K.B; if(!B)break;
        if(B.ph==='open'&&B.pt===6){ if(!snap){K.render();snap=1;shots.push('open:'+B.tg);} for(const k of keyFor[B.tg]){K.keys.add(k);K.pressed.add(k);} }
        K.update();
        for(const k of ['KeyF','KeyS','KeyG']){K.keys.delete(k);} K.pressed.clear();
        if(B.ph==='done'&&B.pt===30){K.render();shots.push('done '+B.hits+'/'+B.total+' gain '+B.gain);break;}
      } return shots;}""")
    print(r);shot('b_done')
    # one more: capture mid-strike in bonus
    pg.evaluate("__K.startBonus()")
    r=pg.evaluate("""()=>{const K=__K;for(let i=0;i<2000;i++){const B=K.B;if(B.ph==='open'&&B.pt===4){K.render();return B.tg;}K.update();}}""")
    print('open target',r);shot('b_open')
    print('errors',errs)
    b.close()
