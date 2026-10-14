import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
os.chdir(ROOT)
TEST_URL = (ROOT / 'test.html').as_uri()   # build with: sh src/build.sh
GAME_URL = (ROOT / 'index.html').as_uri()
from playwright.sync_api import sync_playwright
BOT="""([stage,n,smart])=>{const K=__K,S=K.S;let wins=0,pts=[0,0],tech={};
 for(let m=0;m<n;m++){
  S.mode=1;S.demo=false;S.stage=stage;K.newMatch();let cool=0;
  const press=k=>{K.pressed.add(k);K.keys.add(k);};
  for(let i=0;i<60*120&&S.screen==='match';i++){
    const M=K.M;
    if(M.ph==='fight'){
      const a=M.a,bb=M.b,d=Math.abs(bb.x-a.x);if(cool>0)cool--;
      K.keys.delete('KeyD');K.keys.delete('KeyA');K.keys.delete('KeyS');
      if(bb.st==='attack'&&bb.mt<8&&Math.random()<(smart?0.9:0.5)){const w=bb.mv.win[0].tg;K.keys.add('KeyA');if(w==='kote'||w==='do')K.keys.add('KeyS');}
      else if(d>(smart?67:66))K.keys.add('KeyD');
      else if(d<58&&a.x>40)K.keys.add('KeyA');
      else if(cool===0&&a.canAct()){if(smart){const k=Math.random();if(k<0.4)press('KeyF');else if(k<0.7){K.keys.add('KeyS');press('KeyF');}else press('KeyG');}else press(Math.random()<0.6?'KeyF':'KeyG');cool=smart?50:40;}
    }
    K.update();K.pressed.clear();K.keys.delete('KeyF');K.keys.delete('KeyG');
    if(M.ph==='hitstop'&&M.t===0){}
  }
  for(const k of['KeyD','KeyA','KeyS'])K.keys.delete(k);
  const M=K.M; if(M){pts[0]+=M.a.score;pts[1]+=M.b.score;}
  if(S.screen==='result'&&K.R.kind==='promo'){wins++;}
 }
 return {stage,wins,n,pts};}"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page()
    pg.add_init_script("window.requestAnimationFrame=()=>0")
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(TEST_URL);pg.wait_for_timeout(300)
    pg.evaluate("__K.S.screen='none'")
    for smart in [0,1]:
        for st in [0,3,6,9,12]:
            print('smart' if smart else 'naive',pg.evaluate(BOT,[st,40,smart]))
    print('errors',errs)
    b.close()
