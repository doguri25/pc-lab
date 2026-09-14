from pathlib import Path
import json, sys
p=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/pc-lab.html')
s=p.read_text()

def rep(old,new,name):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{name}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

rep('<title>PC LAB v2.3.5 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.5"><meta name="pc-lab-build" content="2.3.5-652ba33c4b49">','<title>PC LAB v2.3.6 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.6"><meta name="pc-lab-build" content="2.3.6-d024960916af">','release identity')

helper='''function refreshSystemModal(body){const modalBody=$('#modal-root .modal-body');if(ui.modal!=='가상 모니터'||!modalBody)return false;const active=document.activeElement,focusAction=active?.dataset?.action||'',focusTab=active?.dataset?.tab||'',focusType=active?.dataset?.type||'',focusId=active?.id||'',scrollTop=modalBody.scrollTop;modalBody.innerHTML=body;modalBody.scrollTop=scrollTop;let next=null;if(focusAction==='system-tab'&&focusTab)next=modalBody.querySelector(`[data-action="system-tab"][data-tab="${focusTab}"]`);else if(focusAction==='system-type'&&focusType)next=modalBody.querySelector(`[data-action="system-type"][data-type="${focusType}"]`);else if(focusId==='system-disk')next=modalBody.querySelector('#system-disk');if(next)requestAnimationFrame(()=>next?.focus?.({preventScroll:true}));return true;}\n'''
rep('function systemDialog(which=null){',helper+'function systemDialog(which=null){','system refresh helper')
old_tail=" modal('가상 모니터',body,btn(I('power','small')+' 가상 전원 차단','system-prepare','','ghost')+btn('모니터 닫기','close-modal','','ghost'),'wide');}"
new_tail=" if(refreshSystemModal(body))return;modal('가상 모니터',body,btn(I('power','small')+' 가상 전원 차단','system-prepare','','ghost')+btn('모니터 닫기','close-modal','','ghost'),'wide');}"
rep(old_tail,new_tail,'system dialog in-place refresh')

entry={'version':'2.3.6','date':'2026-09-14','timezone':'Asia/Seoul','channel':'stable-local','title':'가상 모니터 메뉴 이동 시 팝업 유지','changes':['가상 모니터의 BIOS/UEFI 및 Windows/Linux 메뉴를 이동할 때 모달 전체를 다시 생성하던 동작을 제거하고 열린 팝업의 본문만 제자리에서 갱신하도록 변경','BIOS·Windows 각 세부 메뉴와 BIOS/OS/설치 화면 전환에서 팝업 배경과 외곽 프레임이 그대로 유지되도록 수정','메뉴 전환 뒤 클릭한 탭의 키보드 포커스와 모달 본문 스크롤 위치를 가능한 한 유지'],'scopeNote':'가상 BIOS·운영체제 화면은 학습용 메뉴 시뮬레이션이며 실제 BIOS/Windows 화면 전체를 복제하거나 실제 시스템 설정을 변경하지 않음.'}
marker='</script><script>\n/* PC LAB content pack 0.1.0.'
if marker not in s: raise SystemExit('release marker missing')
j=json.dumps(entry,ensure_ascii=False,separators=(',',':'))
inject="</script><script>\nwindow.PCRelease.version='2.3.6';window.PCRelease.date='2026-09-14';window.PCRelease.buildId='2.3.6-d024960916af';window.PCRelease.title="+json.dumps(entry['title'],ensure_ascii=False)+";window.PCRelease.changes="+json.dumps(entry['changes'],ensure_ascii=False)+";window.PCRelease.scopeNote="+json.dumps(entry['scopeNote'],ensure_ascii=False)+";window.PCRelease.history=["+j+",...window.PCRelease.history];\n</script><script>\n/* PC LAB content pack 0.1.0."
s=s.replace(marker,inject,1)
p.write_text(s)
