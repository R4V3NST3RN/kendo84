import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
os.chdir(ROOT)
TEST_URL = (ROOT / 'test.html').as_uri()   # build with: sh src/build.sh
GAME_URL = (ROOT / 'index.html').as_uri()
import json,sys
from playwright.sync_api import sync_playwright
JS="""([key,lv,n])=>{const K=__K,S=K.S;const res={counter:0,ippon:0,flagsFail:0,block:0,jam:0,none:0,aiBusy:0};
 for(let i=0;i<n;i++){
   S.demo=false;S.mode=2;K.newMatch();const M=K.M;M.ph='fight';M.t=0;
   const a=M.a,b=M.b;a.set('idle');b.set('idle');a.cur=K.P.kamae.slice();b.cur=K.P.kamae.slice();
   const d=K.MOVES[key].rng[2];a.x=100;b.x=100+d;
   M.aiB=new K.AI(b,lv);M.aiB.next=200; // only reacting, not planning
   a.start(key);
   const h0=a.stats.hits,b0=b.stats.blocks;let out='none';
   for(let t=0;t<60;t++){K.update();if(M.ph==='hitstop'){out=M.pend.att===a?'ippon':'counter';break;}if(b.st==='attack')res.aiBusy++;}
   if(out==='none'){if(b.stats.blocks>b0)out='block';else if(a.stats.hits>h0)out='flagsFail';}
   res[out]++;
 }
 return res;}"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page()
    pg.goto(TEST_URL);pg.wait_for_timeout(300);pg.evaluate("__K.S.screen='none'")
    for lv in [0.1,0.5,0.9]:
        for key in ['men','kote','do','tsuki','tobi','kotemen','harai']:
            print(lv,key,pg.evaluate(JS,[key,lv,60]))
    b.close()
