import os, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
os.chdir(ROOT)
TEST_URL = (ROOT / 'test.html').as_uri()   # build with: sh src/build.sh
GAME_URL = (ROOT / 'index.html').as_uri()
import sys
from playwright.sync_api import sync_playwright
groups=[
 ['kamae','walkA','stand','rei','sonkyo','tsuba'],
 ['menUp','menHit','koteUp','koteHit','doUp','doHit'],
 ['tsukiHit','harai','hikiUp','hikiMen','hikiDo','hit'],
 ['guardHigh','guardLow','openMen','openKote','openDo','kamae'],
]
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1100,'height':900})
    pg.goto(TEST_URL); pg.wait_for_timeout(500)
    pg.evaluate("__K.S.screen='none'")
    for gi,g in enumerate(groups):
        for side in ['shiro','aka']:
            pg.evaluate("""([names,side])=>{const K=__K;K.enterScene(0);const c=K.ctx;K.setC(c);
              c.drawImage(K.SCENES[0].c,0,0);
              names.forEach((n,i)=>{const f=new K.Fighter(side);f.reset(30+i*52, side==='shiro'?1:-1);f.st='pose';f.cur=K.P[n].slice();K.drawFighter(f);
                c.fillStyle='#fff';c.font='7px monospace';c.fillText(n,10+i*52,175);});}""",[g,side])
            pg.locator('#game').screenshot(path=f'tests/g{gi}_{side}.png')
    b.close()
