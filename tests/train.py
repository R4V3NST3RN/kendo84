import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
os.chdir(ROOT)
TEST_URL = (ROOT / 'test.html').as_uri()   # build with: sh src/build.sh
GAME_URL = (ROOT / 'index.html').as_uri()
from playwright.sync_api import sync_playwright
BOT="""()=>{const K=__K,S=K.S;K.startTraining();const out=[];let frames=0,notes=new Set(),li=-1,lf=0,cool=0;
 const combo={men:['KeyF'],kote:['KeyS','KeyF'],do:['KeyG'],tsuki:['KeyW','KeyF'],tobi:['KeyD','KeyF'],kotemen:['KeyD','KeyG'],harai:['KeyS','KeyG'],hikimen:['KeyA','KeyF']};
 for(;frames<60*600&&S.screen==='train';frames++){
   const T=K.T;if(T.i!==li){if(li>=0)out.push([K.LESSONS[li].t,frames-lf,[...notes].join(' | ')]);li=T.i;lf=frames;notes=new Set();}
   if(T.ph==='complete'){out.push(['COMPLETE',frames-lf,'']);break;}
   const L=T.L,f=T.f,p=T.p,d=Math.abs(p.x-f.x);const hold=new Set(),press=[];
   if(cool>0)cool--;
   if(T.ph==='go'&&f.st!=='walkto'){
     if(L.k==='reach'){const m=L.marks[T.mark];if(m!==undefined){if(f.x<m-2)hold.add('KeyD');else if(f.x>m+2)hold.add('KeyA');}}
     else if(L.k==='maai'||L.k==='cut'){const tech=L.tech==='hikimen'?'hikimen':L.tech,best=K.MOVES[tech].rng[2];
       if(L.k==='cut'&&tech==='hikimen'){if(cool===0&&f.canAct()){press.push(...combo.hikimen);cool=40;}}
       else if(d>best+2)hold.add('KeyD');else if(d<best-2)hold.add('KeyA');
       else if(L.k==='cut'&&cool===0&&f.canAct()){press.push(...combo[L.ok[0]]);cool=50;}}
     else if(L.k==='block'||L.k==='kaeshi'){if(T.tell>0||p.st==='attack'){hold.add('KeyA');if(L.t==='DO-UKE')hold.add('KeyS');}
       if(L.k==='kaeshi'&&f.kaeshiT>0&&f.canAct()&&cool===0){press.push('KeyG');cool=30;}}
     else if(L.k==='info'){press.push('KeyF');}
   }
   for(const k of ['KeyA','KeyD','KeyW','KeyS','KeyF','KeyG'])K.keys.delete(k);
   for(const k of hold)K.keys.add(k);
   for(const k of press){K.keys.add(k);K.pressed.add(k);}
   K.update();K.pressed.clear();
   if(T.note)notes.add(T.note.s);
   if(T.i===8&&frames%40===0&&frames-lf<400)out.push(['dbg',frames-lf,[T.ph,T.pn,T.pnext,p.st,f.st,f.x.toFixed(1),p.x.toFixed(1),T.tell,[...K.keys].join('+')].join(',')]);
 }
 out.push(['END',frames,S.screen+' i='+(K.T&&K.T.i)+' ph='+(K.T&&K.T.ph)+' cnt='+(K.T&&K.T.cnt)+' notes:'+[...notes].join(' | ')]);return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1100,'height':800})
    pg.add_init_script("window.requestAnimationFrame=()=>0")
    errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(TEST_URL);pg.wait_for_timeout(300)
    for row in pg.evaluate(BOT): print(row)
    print('errors',errs)
    b.close()
