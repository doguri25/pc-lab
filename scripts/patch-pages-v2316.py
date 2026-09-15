from pathlib import Path
import json,sys
p=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/pc-lab.html')
s=p.read_text()
def rep(a,b,n):
 global s
 c=s.count(a)
 if c!=1: raise SystemExit(f'{n}: expected 1 match, got {c}')
 s=s.replace(a,b,1)
rep('<title>PC LAB v2.3.15 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.15"><meta name="pc-lab-build" content="2.3.15-1ed8f3203523">','<title>PC LAB v2.3.16 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.16"><meta name="pc-lab-build" content="2.3.16-d5ebb8108e4e">','release identity')
rep('</button>`;}\\nconst ONBOARDING_KEY','</button>`;}\nconst ONBOARDING_KEY','tutorial newline syntax')
entry={
 'version':'2.3.16','date':'2026-09-15','timezone':'Asia/Seoul','channel':'stable-local',
 'title':'시작 튜토리얼 배포 검정 화면 긴급 수정',
 'changes':['GitHub Pages에 v2.3.15 시작 튜토리얼을 적용하는 과정에서 잘못 삽입된 문자 때문에 화면이 검게 멈추던 문제를 수정','처음 접속 시 메인 화면을 정상 렌더링한 뒤 6단계 시작 튜토리얼이 열리도록 복구','기존 모바일 부품 선택 후 슬롯 터치 장착, 브라우저 뒤로가기, 만든이: 도구리 표기는 그대로 유지'],
 'scopeNote':'배포 번들의 시작 오류만 수정하며 조립 규칙·부품 데이터·학습 내용은 변경하지 않습니다.'
}
marker='</script><script>\n/* PC LAB content pack 0.1.0.'
if marker not in s: raise SystemExit('content marker missing')
j=json.dumps(entry,ensure_ascii=False,separators=(',',':'))
inject="</script><script>\nwindow.PCRelease.version='2.3.16';window.PCRelease.date='2026-09-15';window.PCRelease.buildId='2.3.16-d5ebb8108e4e';window.PCRelease.title="+json.dumps(entry['title'],ensure_ascii=False)+";window.PCRelease.changes="+json.dumps(entry['changes'],ensure_ascii=False)+";window.PCRelease.scopeNote="+json.dumps(entry['scopeNote'],ensure_ascii=False)+";window.PCRelease.history=["+j+",...window.PCRelease.history];\n</script><script>\n/* PC LAB content pack 0.1.0."
s=s.replace(marker,inject,1)
p.write_text(s)
