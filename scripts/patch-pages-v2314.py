from pathlib import Path
import json, sys
p=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/pc-lab.html')
s=p.read_text()

def rep(old,new,name):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'{name}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

rep('<title>PC LAB v2.3.13 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.13"><meta name="pc-lab-build" content="2.3.13-1d813b29baec">','<title>PC LAB v2.3.14 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.14"><meta name="pc-lab-build" content="2.3.14-96bd6394e936">','release identity')
rep("function bindPartDragSources(){$$('.draggable-part[data-drag-product]').forEach(el=>{if(el.dataset.dragBound)return;el.dataset.dragBound='1';el.addEventListener('pointerdown',e=>{if(e.button!==0&&e.pointerType==='mouse')return;dragSource={id:el.dataset.dragProduct,origin:el.dataset.dragOrigin||'catalog',instance:el.dataset.dragInstance||'',x:e.clientX,y:e.clientY};dragPointer=e.pointerId;dragMoved=false;el.setPointerCapture?.(e.pointerId);});});","function bindPartDragSources(){$$('.draggable-part[data-drag-product]').forEach(el=>{if(el.dataset.dragBound)return;el.dataset.dragBound='1';el.addEventListener('pointerdown',e=>{if(e.pointerType==='touch')return;if(e.button!==0&&e.pointerType==='mouse')return;dragSource={id:el.dataset.dragProduct,origin:el.dataset.dragOrigin||'catalog',instance:el.dataset.dragInstance||'',x:e.clientX,y:e.clientY};dragPointer=e.pointerId;dragMoved=false;el.setPointerCapture?.(e.pointerId);});});",'disable catalog drag on touch')
rep(" if(ui.focus!==slot){focusOn(slot);return;}\n if(slot==='panel'){"," if(ui.selectedProduct&&!['panel','filter','cables','rear'].includes(slot)){installDirect(slot);return;}\n if(ui.focus!==slot){focusOn(slot);return;}\n if(slot==='panel'){",'tap selected product into slot')
rep(" if(ui.selectedProduct){toast('부품을 클릭해 넣는 대신, 왼쪽 부품함에서 실제 슬롯까지 드래그해 놓아 주세요.');return;}\n if(!r.parts[slot]){toast('부품함의 부품을 이 슬롯으로 드래그해 놓으세요.');return;}"," if(ui.selectedProduct){installDirect(slot);return;}\n if(!r.parts[slot]){toast('부품함에서 부품을 한 번 눌러 선택한 뒤 이 슬롯을 누르세요. PC에서는 드래그 장착도 가능합니다.');return;}",'replace drag-only prompt')
rep('부품은 부품함에서 실제 슬롯으로 드래그해 장착하고, 고정을 푼 부품은 잡아 빼서 분리합니다. 아래 목록은 위치 탐색용입니다.','모바일에서는 부품을 한 번 눌러 선택한 뒤 빈 슬롯을 누르면 장착됩니다. PC에서는 드래그 장착도 가능하며, 고정을 푼 부품은 잡아 빼서 분리합니다. 아래 목록은 위치 탐색용입니다.','left panel mobile instructions')
rep('손에 든 부품 · 아직 장착 전','선택한 부품 · 장착 대기','selected banner label')
rep('부품을 잡아 본체의 호환 슬롯까지 드래그해 내려놓으세요.','본체의 호환 슬롯을 한 번 누르면 장착됩니다. PC에서는 슬롯까지 드래그해도 됩니다.','selected banner instructions')
rep('비어 있는 장착 위치입니다. 부품함의 부품을 이 위치까지 드래그해 내려놓으세요.','비어 있는 장착 위치입니다. 모바일에서는 부품함에서 부품을 선택한 뒤 이 슬롯을 누르세요. PC에서는 드래그 장착도 가능합니다.','empty slot instructions')
rep("!cpu?'CPU부터 슬롯에 드래그해 장착하세요.':!grease&&!cooler?'CPU 위에 써멀그리스를 얇게 도포한 뒤 쿨러를 장착하세요.':cooler&&!r.cables.cpuFan?'쿨러의 CPU_FAN 케이블을 연결하세요.':'부품은 드래그로 넣고, 고정 해제 후 분리 작업대까지 드래그해 빼세요.'","!cpu?'모바일은 CPU를 선택한 뒤 빈 CPU 슬롯을 누르세요. PC에서는 드래그 장착도 가능합니다.':!grease&&!cooler?'CPU 위에 써멀그리스를 얇게 도포한 뒤 쿨러를 장착하세요.':cooler&&!r.cables.cpuFan?'쿨러의 CPU_FAN 케이블을 연결하세요.':'모바일은 부품 선택 후 빈 슬롯을 눌러 장착합니다. 분리는 고정 해제 후 부품을 분리 작업대까지 드래그해 빼세요.'",'assembly coach instructions')

style='''<style id="pc-lab-v2314-mobile-tap-install">\n@media (pointer:coarse){.catalog-mini-item.draggable-part{touch-action:manipulation!important;cursor:pointer!important}.catalog-mini-item.selected{box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 35%,transparent)!important}}\n</style>'''
if 'pc-lab-v2314-mobile-tap-install' not in s:
    s=s.replace('</head>',style+'</head>',1)

entry={'version':'2.3.14','date':'2026-09-14','timezone':'Asia/Seoul','channel':'stable-local','title':'모바일 부품 선택 후 슬롯 터치 장착','changes':['모바일 부품 목록에서는 손가락 드래그 대신 부품을 한 번 터치해 선택하도록 변경','선택한 부품이 있으면 호환되는 빈 슬롯을 한 번 터치해 바로 장착하도록 변경','RAM도 RAM 선택 후 원하는 빈 슬롯 터치 장착으로 통일','모바일 안내 문구를 부품 선택 → 슬롯 터치 흐름에 맞게 수정','데스크톱 드래그 장착과 분해 드래그는 그대로 유지'],'scopeNote':'모바일 조립 입력 방식을 터치 선택 중심으로 단순화하며 데스크톱 드래그 조작과 기존 조립·호환성 규칙은 유지합니다.'}
marker='</script><script>\n/* PC LAB content pack 0.1.0.'
if marker not in s: raise SystemExit('release marker missing')
j=json.dumps(entry,ensure_ascii=False,separators=(',',':'))
inject="</script><script>\nwindow.PCRelease.version='2.3.14';window.PCRelease.date='2026-09-14';window.PCRelease.buildId='2.3.14-96bd6394e936';window.PCRelease.title="+json.dumps(entry['title'],ensure_ascii=False)+";window.PCRelease.changes="+json.dumps(entry['changes'],ensure_ascii=False)+";window.PCRelease.scopeNote="+json.dumps(entry['scopeNote'],ensure_ascii=False)+";window.PCRelease.history=["+j+",...window.PCRelease.history];\n</script><script>\n/* PC LAB content pack 0.1.0."
s=s.replace(marker,inject,1)
p.write_text(s)
