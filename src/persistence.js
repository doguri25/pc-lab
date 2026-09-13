/* Version-isolated local saves. Never reads a legacy save implicitly; never clears
 * origin storage. Optimistic revision checks + per-tab recovery journals retain
 * divergent work. The main copy is never silently adopted across tabs. */
(function(root){
'use strict';
const clone=x=>JSON.parse(JSON.stringify(x));
function hash(s){let h=2166136261;for(const c of String(s)){h^=c.charCodeAt(0);h=Math.imul(h,16777619);}return (h>>>0).toString(36);}
function namespace(version,scope='local'){return 'pc-lab:save:'+version+':'+hash(scope);}
function create({storage,version,scope='local',writer,validate,now=()=>new Date().toISOString(),branch=''}){
 const prefix=namespace(version,scope),key=prefix+(branch?':test:'+branch:''),draftKey=key+':draft:'+writer;
 let base=null,seq=0,blocked=false,lastProfile=null,lastError='',lastBackupTime=0,backupSequence=0;
 const get=k=>storage.getItem(k);
 const parse=raw=>{if(!raw)return null;try{const o=JSON.parse(raw);return validate(o).ok?o:null;}catch{return null;}};
 function pack(p){return {type:'pc-lab-save',schema:1,gameVersion:version,contentVersion:root.PCData?.CONTENT_VERSION||'',savedAt:now(),writer,saveRevision:seq+1,saveNamespace:key,profile:clone(p)};}
 function load(){blocked=false;lastError='';try{base=get(key);if(base===null){lastProfile=null;return {ok:true,empty:true};}const o=parse(base);if(!o||o.gameVersion!==version){blocked=true;return {ok:false,reason:'invalid',message:'이 버전 저장을 읽지 못했습니다. 원본을 보존하고 파일 복원을 기다립니다.'};}seq=Number.isSafeInteger(o.saveRevision)?o.saveRevision:0;lastProfile=JSON.stringify(o.profile);return {ok:true,envelope:o,profile:validate(o).profile};}catch(e){lastError=e.message;return {ok:false,reason:'unavailable',message:'브라우저 저장에 접근할 수 없습니다. 파일 내보내기를 이용하세요.'};}}
 function preserve(p,reason='conflict'){const o=pack(p);o.recoveryReason=reason;try{storage.setItem(draftKey,JSON.stringify(o));return true;}catch(e){lastError=e.message;return false;}}
 function commit(p){let encoded;try{encoded=JSON.stringify(p);}catch{return {ok:false,reason:'invalid',message:'진행을 직렬화하지 못했습니다.'};}
  try{const current=get(key);
   if(blocked||current!==base){blocked=true;const preserved=preserve(p);return {ok:false,reason:'conflict',preserved,message:preserved?'다른 창의 진행과 분리하여 이 창의 복구본을 보관했습니다.':'저장 충돌·복구 공간 부족: 이 창의 진행을 파일로 내보내세요.'};}
   if(encoded===lastProfile)return {ok:true,unchanged:true};
   const out=pack(p),raw=JSON.stringify(out);
   // Independent writer journal survives even if two unsupported browsers race.
   storage.setItem(draftKey,JSON.stringify({...out,recoveryReason:'autosave'}));
   const before=parse(current);const t=Date.parse(out.savedAt);
   if(before&&(!lastBackupTime||t-lastBackupTime>180000)){
    try{storage.setItem(key+':previous',current);lastBackupTime=t;}catch{/* main save still takes priority; no false backup claim */}
   }
   storage.setItem(key,raw);
   if(get(key)!==raw){blocked=true;return {ok:false,reason:'conflict',preserved:true,message:'동시 저장을 감지했습니다. 이 창의 복구본은 별도로 남겼습니다.'};}
   base=raw;seq=out.saveRevision;lastProfile=encoded;lastError='';return {ok:true,envelope:out};
  }catch(e){lastError=e.message;return {ok:false,reason:'unavailable',message:'저장 공간에 기록하지 못했습니다. 진행을 파일로 내보내세요.'};}
 }
 function external(eventKey){if(eventKey!==key&&eventKey!==null)return false;try{if(get(key)!==base){blocked=true;return true;}}catch{}return false;}
 function list(){const found=[];try{for(let i=0;i<storage.length;i++){const k=storage.key(i);if(!(k==='pc-lab-v1'||k==='pc-lab-v1-before-import'||k?.startsWith('pc-lab:save:')))continue;const raw=get(k),o=parse(raw);if(o)found.push({key:k,raw,envelope:o,current:k===key,recovery:k.includes(':draft:')||k.includes(':backup:')||k.endsWith(':previous'),legacy:k.startsWith('pc-lab-v1'),test:k.includes(':test:')});}}catch(e){lastError=e.message;}return found.sort((a,b)=>(Date.parse(b.envelope.savedAt)||0)-(Date.parse(a.envelope.savedAt)||0));}
 function adoptionToken(){try{return get(key);}catch{return undefined;}}
 function adopt(envelope,currentProfile,expected){const v=validate(envelope);if(!v.ok)return {ok:false,reason:'invalid',message:v.message};
  // Never call until the user explicitly confirms a chosen save or import.
  try{const primary=get(key);if(expected===undefined||primary!==expected)return {ok:false,reason:'changed',message:'확인하는 동안 저장본이 변경되었습니다. 목록을 다시 열어 선택하세요.'};
   const backup=key+':backup:'+writer+':'+(Date.parse(now())||Date.now())+'-'+(++backupSequence);
   storage.setItem(backup,JSON.stringify({...pack(currentProfile),recoveryReason:'before-import'}));
   // Preserve the other writer's canonical version too, not just this tab.
   if(primary&&primary!==JSON.stringify(pack(currentProfile)))storage.setItem(backup+':primary',primary);
   base=primary;blocked=false;seq=parse(primary)?.saveRevision||seq;lastProfile=null;
   const next=v.profile;next.version=version;const res=commit(next);return {...res,profile:res.ok?next:null,backupKey:backup};
  }catch(e){return {ok:false,reason:'backup-failed',message:'가져오기 전 백업을 만들 수 없어 현재 진행을 유지했습니다. 파일로 먼저 보관하세요.'};}
 }
 return {key,prefix,draftKey,branch,load,commit,preserve,external,list,adopt,adoptionToken,pack,get blocked(){return blocked;},get error(){return lastError;},get revision(){return seq;}};
}
const API={create,namespace,hash};if(typeof module!=='undefined')module.exports=API;root.PCPersistence=API;
})(typeof window!=='undefined'?window:globalThis);
