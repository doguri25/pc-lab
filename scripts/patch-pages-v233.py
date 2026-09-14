from pathlib import Path
import json, sys

path=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/pc-lab.html')
s=path.read_text()

def rep(old,new,name):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{name}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

rep('<title>PC LAB v2.3.2 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.2"><meta name="pc-lab-build" content="2.3.2-b622600c7980">','<title>PC LAB v2.3.3 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.3"><meta name="pc-lab-build" content="2.3.3-2b16f203e5d9">','meta')

rep("async function physicalChange(fn,{kind='touch',element=null,slot=null,wasOn=false,done=null,refresh='render'}={}){\n if(ui.busy)return;const r=profile.current;let result;try{result=fn();}catch(err){toast('작업을 적용하지 못했습니다. '+err.message,true);return;}\n", "async function physicalChange(fn,{kind='touch',element=null,slot=null,wasOn=false,done=null,refresh='render'}={}){\n if(ui.busy)return;const r=profile.current;\n const panelCamera=(kind==='panel-open'||kind==='panel-close')?(()=>{\n  const v=G.sessions.get('work'),c=v&&v.rigId===r?.id?{yaw:v.yaw,pitch:v.pitch,distance:v.distance}:(ui.returnCamera||ui.workCamera);\n  return c&&['yaw','pitch','distance'].every(k=>Number.isFinite(c[k]))?{...c}:null;\n })():null;\n let result;try{result=fn();}catch(err){toast('작업을 적용하지 못했습니다. '+err.message,true);return;}\n", 'panel camera snapshot')

rep(" }finally{ui.busy=false;document.body.classList.remove('physical-busy');if(refresh==='precision')refreshPrecisionSurface();else if(refresh!=='none')render();toast(result.message);}", " }finally{ui.busy=false;document.body.classList.remove('physical-busy');if(panelCamera){ui.restoreCamera={...panelCamera};ui.workCamera={...panelCamera};ui.returnCamera={...panelCamera};}if(refresh==='precision')refreshPrecisionSurface();else if(refresh!=='none')render();toast(result.message);}", 'panel camera restore')

rep(" case 'panel-toggle':notify(E.togglePanel(r));break;", " case 'panel-toggle':{captureWorkCamera();const cam=ui.returnCamera||ui.workCamera,res=E.togglePanel(r);if(res.ok&&cam&&['yaw','pitch','distance'].every(k=>Number.isFinite(cam[k])))ui.restoreCamera={...cam};notify(res);break;}", 'panel toggle camera')

old_css=".workload-category-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:15px}\n.workload-category-card{display:flex;flex-direction:column;align-items:flex-start;gap:5px;min-height:112px;padding:13px;border:1px solid var(--line);border-radius:10px;background:var(--panel2);text-align:left;color:var(--text)}\n.workload-category-card:hover{border-color:color-mix(in srgb,var(--accent) 55%,var(--line));background:color-mix(in srgb,var(--accent) 7%,var(--panel2))}\n.workload-category-card.active{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 13%,var(--panel2));box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent) 25%,transparent)}\n.workload-category-card strong{font-size:.88rem}.workload-category-card span{font-size:.7rem;color:var(--accent);font-weight:700}.workload-category-card small{font-size:.7rem;line-height:1.5;color:var(--muted)}\n@media(max-width:1100px){.workload-category-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}\n@media(max-width:760px){.workload-category-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.workload-category-card{min-height:105px}}\n@media(max-width:480px){.workload-category-grid{grid-template-columns:1fr}.workload-category-card{min-height:0}}"
new_css=".workload-category-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(155px,1fr));gap:7px;margin-top:12px}\n.workload-category-card{display:flex;flex-direction:column;align-items:flex-start;gap:3px;min-height:82px;padding:9px 10px;border:1px solid var(--line);border-radius:8px;background:var(--panel2);text-align:left;color:var(--text)}\n.workload-category-card:hover{border-color:color-mix(in srgb,var(--accent) 55%,var(--line));background:color-mix(in srgb,var(--accent) 7%,var(--panel2))}\n.workload-category-card.active{border-color:var(--accent);background:color-mix(in srgb,var(--accent) 13%,var(--panel2));box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--accent) 25%,transparent)}\n.workload-category-card strong{font-size:.82rem;line-height:1.25}.workload-category-card span{font-size:.64rem;color:var(--accent);font-weight:700}.workload-category-card small{font-size:.64rem;line-height:1.35;color:var(--muted);display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;overflow:hidden}\n@media(max-width:760px){.workload-category-grid{grid-template-columns:repeat(auto-fill,minmax(135px,1fr));gap:6px}.workload-category-card{min-height:76px;padding:8px 9px}}\n@media(max-width:480px){.workload-category-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.workload-category-card{min-height:72px;padding:8px}.workload-category-card small{font-size:.61rem;-webkit-line-clamp:1}}"
rep(old_css,new_css,'Use Case Library compact CSS')

entry={
  'version':'2.3.3','date':'2026-09-14','timezone':'Asia/Seoul','channel':'stable-local',
  'title':'덮개 분리 시점 고정과 활용 분석 카테고리 UI 압축',
  'changes':[
    'PC 덮개를 열거나 닫기 직전의 3D 카메라 회전각(yaw/pitch)과 확대 거리(zoom)를 별도로 보존하고 작업 후 그대로 복원하여 덮개만 이동하고 사용자 시점은 바뀌지 않도록 수정',
    '3D 덮개 조작 경로와 보조 덮개 토글 경로 모두 동일한 카메라 보존 규칙을 적용하여 어느 조작 방식에서도 시점이 초기화되지 않도록 보강',
    '활용 분석 USE CASE LIBRARY의 카테고리 카드를 고정 4열 대형 구조에서 더 촘촘한 자동 채움 구조로 변경하여 가로 빈 공간을 줄임',
    '카테고리 카드의 좌우 패딩·최소 높이·글자 간격을 줄이고 예시 문구를 최대 두 줄로 제한하여 많은 카테고리를 한 화면에서 빠르게 훑을 수 있도록 개선',
    '기존 조립·저장·릴리스 회귀검사와 3D 덮개 개폐 전후 카메라 수치 일치, 데스크톱·모바일 활용 분석 카테고리 크기 검사를 추가 검증'
  ],
  'scopeNote':'로컬 학습용 PC 조립 시뮬레이터. 3D 카메라와 부품 배치는 초보자 학습용 시각화이며 실제 제조사 서비스 도면의 정밀 좌표를 의미하지 않음.'
}
marker='</script><script>\n/* PC LAB content pack 0.1.0.'
inject="</script><script>\nwindow.PCRelease.version='2.3.3';window.PCRelease.date='2026-09-14';window.PCRelease.buildId='2.3.3-2b16f203e5d9';window.PCRelease.title="+json.dumps(entry['title'],ensure_ascii=False)+";window.PCRelease.changes="+json.dumps(entry['changes'],ensure_ascii=False)+";window.PCRelease.scopeNote="+json.dumps(entry['scopeNote'],ensure_ascii=False)+";window.PCRelease.history=["+json.dumps(entry,ensure_ascii=False,separators=(',',':'))+",...window.PCRelease.history];\n</script><script>\n/* PC LAB content pack 0.1.0."
rep(marker,inject,'release override')
path.write_text(s)
