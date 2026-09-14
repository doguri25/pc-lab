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

rep('<title>PC LAB v2.3.11 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.11"><meta name="pc-lab-build" content="2.3.11-10d1a00d47bd">',
    '<title>PC LAB v2.3.12 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.12"><meta name="pc-lab-build" content="2.3.12-8f23588a26e1">',
    'release identity')

old="function releasesDialog(){modal('버전 · 날짜 · 변경 기록',`<div class=\"notice subdued\">현재 실행 <strong>v${R.version}</strong> · ${R.date} (Asia/Seoul)<br>BUILD ${S(R.buildId)}<br>게임 실행 날짜가 아니라 해당 버전의 배포 기록입니다.</div>"
new="function releasesDialog(){modal('버전 · 날짜 · 변경 기록',`<div class=\"notice subdued\">현재 실행 <strong>v${R.version}</strong> · ${R.date} (Asia/Seoul)<br>BUILD ${S(R.buildId)}<br><strong>만든이: 도구리</strong><br>게임 실행 날짜가 아니라 해당 버전의 배포 기록입니다.</div>"
rep(old,new,'creator label')

entry={'version':'2.3.12','date':'2026-09-14','timezone':'Asia/Seoul','channel':'stable-local','title':'버전 기록 창 만든이 표기 추가','changes':['버전 · 날짜 · 변경 기록 팝업의 현재 실행 정보에 만든이: 도구리 문구를 추가','기존 v2.3.11의 모바일 작업대 최적화와 메인 배너 겹침 수정은 그대로 유지'],'scopeNote':'버전 기록 창의 제작자 표기만 추가하며 기존 학습·조립 기능과 모바일 레이아웃 동작은 변경하지 않습니다.'}
marker='</script><script>\n/* PC LAB content pack 0.1.0.'
if marker not in s: raise SystemExit('release marker missing')
inject=("</script><script>\n"
 "window.PCRelease.version='2.3.12';window.PCRelease.date='2026-09-14';window.PCRelease.buildId='2.3.12-8f23588a26e1';"
 "window.PCRelease.title="+json.dumps(entry['title'],ensure_ascii=False)+";"
 "window.PCRelease.changes="+json.dumps(entry['changes'],ensure_ascii=False)+";"
 "window.PCRelease.scopeNote="+json.dumps(entry['scopeNote'],ensure_ascii=False)+";"
 "window.PCRelease.history=["+json.dumps(entry,ensure_ascii=False,separators=(',',':'))+",...window.PCRelease.history];\n"
 "</script><script>\n/* PC LAB content pack 0.1.0.")
s=s.replace(marker,inject,1)
p.write_text(s)
