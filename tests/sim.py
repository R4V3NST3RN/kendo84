import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
os.chdir(ROOT)
TEST_URL = (ROOT / 'test.html').as_uri()   # build with: sh src/build.sh
GAME_URL = (ROOT / 'index.html').as_uri()
import json,sys
from playwright.sync_api import sync_playwright
JS="""([n,lvA,lvB])=>{const K=__K,S=K.S;const out={matches:[],errors:[]};
 for(let i=0;i<n;i++){
   S.demo=true;S.mode=1;S.stage=1;S.sceneI=i%4;K.newMatch();
   const M0=K.M;M0.aiA.lv=lvA;M0.aiB.lv=lvB;
   let prev='',log=[],steps=0;
   try{
   while(S.screen==='match'&&K.M===M0&&steps<60*400){
     K.update();steps++;
     const M=K.M;if(!M)break;
     if(M.ph!==prev){
       if(M.ph==='hitstop')log.push((M.pend.att.side[0])+':'+M.pend.att.mk+'/'+M.pend.w.tg);
       if(M.ph==='yame')log.push('HANSOKU:'+M.off.side[0]+M.off.han);
       if(M.ph==='wakare')log.push('WAKARE');
       if(M.ph==='hantei')log.push('HANTEI');
       if(M.ph==='timeup')log.push('TIMEUP');
       if(M.ph==='win')log.push('WIN:'+M.w.side+' '+M.a.score+'-'+M.b.score+' t='+(M.time/60|0));
       prev=M.ph;
     }
   }}catch(e){out.errors.push(String(e)+e.stack);}
   out.matches.push({steps,log,thrownA:M0.a.stats.thrown,thrownB:M0.b.stats.thrown,hitsA:M0.a.stats.hits,hitsB:M0.b.stats.hits,blocks:[M0.a.stats.blocks,M0.b.stats.blocks]});
 }
 return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page()
    errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(TEST_URL); pg.wait_for_timeout(300)
    pg.evaluate("__K.S.screen='none'")
    for lvA,lvB in [(0.6,0.6),(0.2,0.9),(0.9,0.2)]:
        r=pg.evaluate(JS,[int(sys.argv[1]) if len(sys.argv)>1 else 12,lvA,lvB])
        print('=== lvA',lvA,'lvB',lvB,'errors',r['errors'][:2])
        from collections import Counter
        tech=Counter();wins=Counter();misc=Counter()
        for m in r['matches']:
            for e in m['log']:
                if ':' in e and e[1]==':': tech[e[2:]]+=1
                elif e.startswith('WIN'): wins[e.split()[0]]+=1
                else: misc[e.split(':')[0]]+=1
        for m in r['matches'][:4]: print(' ',m['steps'],m['log'],'thrown',m['thrownA'],m['thrownB'],'valid-ish hits',m['hitsA'],m['hitsB'],'blocks',m['blocks'])
        print(' tech',dict(tech)); print(' wins',dict(wins)); print(' misc',dict(misc))
        print(' avg steps',sum(m['steps'] for m in r['matches'])/len(r['matches']))
    print('page errors',errs)
    b.close()
