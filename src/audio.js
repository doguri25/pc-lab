/* Original procedural workshop audio. No samples, music downloads, microphone,
 * autoplay, tracking or external services. Failures must never block gameplay. */
(function(root){
'use strict';
const clamp=(v,a,b)=>Math.min(b,Math.max(a,Number.isFinite(Number(v))?Number(v):a));
const CUES=['click','screwOut','screwIn','latch','panelOpen','panelClose','install','remove','connect','disconnect','clean','boot','powerOff','scan','success','warning','save','reward'];
function settings(v={}){return {enabled:v.sound!==false,volume:clamp(v.volume??35,0,100),ambience:v.ambience===true};}
let ctx=null,master=null,fx=null,airGain=null,airSource=null,noise=null,enabled=true,volume=35,ambience=false,unlocked=false,hidden=false,fanActive=false,lastCue='',lastAt=-Infinity,lastError='',played=0,active=0;
function configure(v){const s=settings(v);enabled=s.enabled;volume=s.volume;ambience=s.ambience;apply();return status();}
function apply(){if(!ctx||!master)return;const t=ctx.currentTime;master.gain.cancelScheduledValues(t);master.gain.setTargetAtTime(enabled&&!hidden?volume/100*.36:0,t,.035);if(airGain)airGain.gain.setTargetAtTime(ambience&&fanActive?.085:0,t,.15);}
function create(){if(ctx)return true;const AC=root.AudioContext||root.webkitAudioContext;if(!AC){lastError='이 브라우저는 Web Audio를 지원하지 않습니다.';return false;}
 try{ctx=new AC();master=ctx.createGain();master.gain.value=0;const limiter=ctx.createDynamicsCompressor();limiter.threshold.value=-14;limiter.knee.value=20;limiter.ratio.value=8;master.connect(limiter);limiter.connect(ctx.destination);fx=ctx.createGain();fx.connect(master);const n=Math.floor(ctx.sampleRate*2);noise=ctx.createBuffer(1,n,ctx.sampleRate);let seed=151101,low=0;const a=noise.getChannelData(0);for(let i=0;i<n;i++){seed=(Math.imul(seed,1664525)+1013904223)>>>0;low=.91*low+.09*(seed/2147483648-1);a[i]=low*3;}airSource=ctx.createBufferSource();airSource.buffer=noise;airSource.loop=true;const filter=ctx.createBiquadFilter();filter.type='lowpass';filter.frequency.value=460;airGain=ctx.createGain();airGain.gain.value=0;airSource.connect(filter);filter.connect(airGain);airGain.connect(master);airSource.start();ctx.onstatechange=()=>{lastError=ctx.state==='closed'?'소리 장치 연결이 종료되었습니다.':'';};return true;
 }catch(e){lastError='소리 장치를 시작하지 못했습니다.';ctx=null;return false;}}
function unlock(){if(!enabled||hidden)return false;if(!create())return false;unlocked=true;try{if(ctx.state==='suspended')ctx.resume().catch(()=>{lastError='첫 클릭 후에도 소리가 차단되어 있습니다. 브라우저 소리 권한을 확인하세요.';});apply();return true;}catch{lastError='소리가 차단되어 있습니다.';return false;}}
function env(node,t,d,v){node.gain.setValueAtTime(.0001,t);node.gain.exponentialRampToValueAtTime(Math.max(.0002,v),t+.008);node.gain.exponentialRampToValueAtTime(.0001,t+d);}
function tone(f,t,d=.1,v=.16,type='sine',end=f){const o=ctx.createOscillator(),g=ctx.createGain();o.type=type;o.frequency.setValueAtTime(f,t);o.frequency.exponentialRampToValueAtTime(Math.max(30,end),t+d);env(g,t,d,v);o.connect(g);g.connect(fx);active++;o.onended=()=>{active--;o.disconnect();g.disconnect();};o.start(t);o.stop(t+d+.015);}
function hiss(t,d=.12,v=.24,hz=1800){const s=ctx.createBufferSource(),f=ctx.createBiquadFilter(),g=ctx.createGain();s.buffer=noise;f.type='bandpass';f.frequency.value=hz;f.Q.value=.8;env(g,t,d,v);s.connect(f);f.connect(g);g.connect(fx);active++;s.onended=()=>{active--;s.disconnect();f.disconnect();g.disconnect();};s.start(t);s.stop(t+d+.015);}
function play(name,options={}){if(!CUES.includes(name)||!enabled||!volume||hidden||!unlocked||!ctx||ctx.state==='closed'||active>64)return false;const t=ctx.currentTime+.008;if(name===lastCue&&t-lastAt<(name==='click'?.07:.12))return false;lastAt=t;lastCue=name;played++;
 try{const pan=Number(options.pan); // optional spatial pan reserved for future mix; never required.
 switch(name){
 case 'click':tone(820,t,.038,.13,'sine',550);break;
 case 'screwIn':case 'screwOut':for(let i=0;i<6;i++){const at=t+i*.072;hiss(at,.04,.55,1800+i*60);tone(name==='screwIn'?600+i*32:770-i*36,at,.035,.08,'triangle');}tone(290,t+.47,.06,.10);break;
 case 'latch':hiss(t,.035,.65,2900);tone(170,t,.07,.25,'triangle',110);tone(610,t+.055,.035,.08);break;
 case 'panelOpen':hiss(t,.34,.4,600);tone(120,t+.3,.14,.2,'triangle',70);break;
 case 'panelClose':hiss(t,.17,.34,700);tone(95,t+.15,.2,.35,'triangle',55);break;
 case 'install':tone(340,t,.1,.15,'triangle',200);hiss(t+.11,.045,.5,2700);tone(720,t+.12,.07,.12);break;
 case 'remove':hiss(t,.12,.35,900);tone(260,t,.12,.16,'triangle',410);break;
 case 'connect':hiss(t,.032,.55,2100);tone(480,t+.035,.06,.17,'triangle');break;
 case 'disconnect':hiss(t,.07,.5,1500);tone(300,t,.08,.14,'triangle',160);break;
 case 'clean':for(let i=0;i<3;i++)hiss(t+i*.13,.17,.30,1800+i*140);break;
 case 'boot':[261.63,392,523.25].forEach((f,i)=>tone(f,t+i*.11,.22,.16));break;
 case 'powerOff':tone(390,t,.27,.14,'sine',130);break;
 case 'scan':[700,850,1050].forEach((f,i)=>tone(f,t+i*.09,.045,.09));break;
 case 'success':[523.25,659.25,783.99].forEach((f,i)=>tone(f,t+i*.095,.17,.14));break;
 case 'warning':tone(285,t,.1,.16);tone(250,t+.15,.13,.15);break;
 case 'save':tone(750,t,.045,.10);tone(1120,t+.08,.10,.09);break;
 case 'reward':[392,493.88,587.33,783.99].forEach((f,i)=>tone(f,t+i*.12,.28,.17));break;
 }return true;}catch{lastError='소리 재생 오류 · 게임은 계속 이용할 수 있습니다.';return false;}}
function setActivity(on){fanActive=!!on;apply();}
function visibility(value){hidden=!!value;apply();if(ctx&&hidden&&ctx.state==='running')ctx.suspend().catch(()=>{});else if(ctx&&!hidden&&unlocked&&enabled)ctx.resume().catch(()=>{});}
function status(){return {enabled,volume,ambience,unlocked,contextState:ctx?.state||'not-started',supported:!!(root.AudioContext||root.webkitAudioContext),hidden,fanActive,played,active,lastCue,error:lastError};}
const api={configure,unlock,play,setActivity,visibility,status,settings,cues:CUES};root.PCAudio=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
