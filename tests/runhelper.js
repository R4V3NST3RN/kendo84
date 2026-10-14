window.run=(n,held,cond)=>{const K=__K;let log=[],prev='';
      for(let i=0;i<n;i++){
        for(const k of held||[]){if(!K.keys.has(k))K.pressed.add(k);K.keys.add(k);}
        K.update();K.pressed.clear();
        const M=K.M,st=K.S.screen+(M?':'+M.ph:'');
        if(st!==prev){log.push(st+(M&&M.say&&M.sayT>0?' «'+M.say+'»':''));prev=st;}
        if(cond&&eval(cond)){log.push('cond@'+i);break;}
      }
      for(const k of held||[])K.keys.delete(k);return log;}