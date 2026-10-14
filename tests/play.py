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
    r=pg.evaluate("""()=>{const K=__K,S=K.S;S.screen='title';K.startGame(1);let log=[],prev='',cool=0;
      const press=k=>{K.pressed.add(k);K.keys.add(k);};
      for(let i=0;i<60*60*12;i++){
        const M=K.M;
        if(S.screen==='match'&&M&&M.ph==='fight'){
          const a=M.a,bb=M.b,d=Math.abs(bb.x-a.x);
          if(cool>0)cool--;
          if(bb.st==='attack'&&bb.mt<6){K.keys.add('KeyA');}
          else if(d>66){K.keys.add('KeyD');K.keys.delete('KeyA');}
          else{K.keys.delete('KeyD');K.keys.delete('KeyA');if(cool===0&&a.canAct()){press(Math.random()<0.6?'KeyF':'KeyG');cool=40;}}
        }else{K.keys.delete('KeyD');K.keys.delete('KeyA');}
        if((S.screen==='result'||(S.screen==='bonus'&&K.B.ph==='done'))&&i%90===0)press('Enter');
        if(S.screen==='bonus'&&K.B.ph==='open'&&K.B.pt===8){const t=K.B.tg;if(t==='kote'){K.keys.add('KeyS');press('KeyF');}else press(t==='men'?'KeyF':'KeyG');}
        K.update();K.pressed.clear();K.keys.delete('KeyF');K.keys.delete('KeyG');K.keys.delete('KeyS');
        const st=S.screen+(S.screen==='result'?':'+K.R.kind:'')+(S.screen==='match'?':st'+S.stage:'');
        if(st!==prev){log.push(st+(M&&S.screen!=='match'?' '+M.a.score+'-'+M.b.score:''));prev=st;}
        if(S.screen==='title')break;
      }
      return {log,stage:S.stage,score:S.score};}""")
    print(r)
    print('errors',errs)
    b.close()
