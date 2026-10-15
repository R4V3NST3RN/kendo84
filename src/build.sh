#!/bin/sh
# Builds the game from src/ into the repo root:
#   index.html - the playable game (served by GitHub Pages)
#   test.html  - same game with a test hook exposing internals as window.__K (gitignored)
set -e
cd "$(dirname "$0")"
cat head.part page.part | sed 's#/\*TEST_HOOK\*/##' > ../index.html
cat head.part page.part | sed 's#/\*TEST_HOOK\*/#window.__K={S,get M(){return M},get B(){return B},get R(){return R},MOVES,P,I,Fighter,measure,probe,contact,targetOf,startGame,newMatch,startBonus,toTitle,AI,keys,pressed,SCENES,enterScene,drawFighter,setC:c=>{C=c},getC:()=>C,ctx,render,update,quality,setR:r=>{R=r},endMatch,win,startTraining,openHelp,closeHelp,get T(){return T},LESSONS,nextLesson};#' > ../test.html
echo "built index.html and test.html"
