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
    # helper: run frames with a set of held keys
    pg.evaluate("""window.run=(n,held,cond)=>{const K=__K;let log=[],prev='';
      for(let i=0;i<n;i++){
        for(const k of held||[]){if(!K.keys.has(k))K.pressed.add(k);K.keys.add(k);}
        K.update();K.pressed.clear();
        const M=K.M,st=K.S.screen+(M?':'+M.ph:'');
        if(st!==prev){log.push(st+(M&&M.say&&M.sayT>0?' «'+M.say+'»':''));prev=st;}
        if(cond&&eval(cond)){log.push('cond@'+i);break;}
      }
      for(const k of held||[])K.keys.delete(k);return log;}""")
    # --- hansoku: 2P mode, P1 walks backwards out of the court
    pg.evaluate("const K=__K;K.S.demo=false;K.startGame(2)")
    print('intro',pg.evaluate("run(150,[],null)"))
    print('walk out',pg.evaluate("run(400,['KeyA'],\"K.M.ph==='hansoku'\")"))
    pg.evaluate("__K.render()");shot('f_hansoku')
    print('after',pg.evaluate("run(300,[],\"K.M.ph==='fight'\")"), pg.evaluate("[__K.M.a.han,__K.M.a.x,__K.M.b.score]"))
    print('walk out 2',pg.evaluate("run(500,['KeyA'],\"K.M.ph==='hansoku'\")"))
    print('after2',pg.evaluate("run(300,[],\"K.M.ph==='fight'\")"), pg.evaluate("[__K.M.a.han,__K.M.b.score,__K.M.say]"))
    # --- wakare: walk into tsubazeriai and wait
    print('close in',pg.evaluate("run(200,['KeyD'],\"Math.abs(K.M.a.x-K.M.b.x)<34\")"))
    print('wait',pg.evaluate("run(400,[],\"K.M.ph==='wakare'\")"))
    pg.evaluate("__K.update();__K.render()");shot('f_wakare')
    print('resume',pg.evaluate("run(200,[],\"K.M.ph==='fight'\")"),pg.evaluate("Math.abs(__K.M.a.x-__K.M.b.x)"))
    # --- time up -> encho -> hantei
    pg.evaluate("__K.M.time=60")
    print('timeup',pg.evaluate("run(4000,[],\"K.M.ph==='hantei'\")"))
    pg.evaluate("__K.render()");shot('f_hantei')
    print('end',pg.evaluate("run(800,[],\"K.S.screen==='result'\")"))
    pg.evaluate("__K.render()");shot('f_tally')
    print('errors',errs)
    b.close()
