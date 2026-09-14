from pathlib import Path
import json, sys
p=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/pc-lab.html')
s=p.read_text()
old='<title>PC LAB v2.3.4 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.4"><meta name="pc-lab-build" content="2.3.4-3f78610b1dc0">'
new='<title>PC LAB v2.3.5 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.5"><meta name="pc-lab-build" content="2.3.5-652ba33c4b49">'
if s.count(old)!=1: raise SystemExit('meta mismatch')
s=s.replace(old,new,1)
style='''<style id="pc-lab-v235-focus-inset-fix">.studio-stage .focus-heading{left:10px!important;right:10px!important;padding:5px 8px 10px!important;box-sizing:border-box!important;width:auto!important;max-width:none!important;overflow:hidden}.studio-stage .focus-heading>.btn{min-width:0;max-width:42%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.studio-stage .focus-heading>.detail-on-stage{margin-left:auto}@media(max-width:650px){.studio-stage .focus-heading{left:10px!important;right:10px!important;padding-left:8px!important;padding-right:8px!important}.studio-stage .focus-heading>.btn{max-width:48%}}</style>'''
if '</head>' not in s: raise SystemExit('head missing')
s=s.replace('</head>',style+'</head>',1)
entry={'version':'2.3.5','date':'2026-09-14','timezone':'Asia/Seoul','channel':'stable-local','title':'확대 작업 헤더 버튼 안쪽 정렬 보정','changes':['확대 작업 헤더 좌우 버튼을 배경선에서 8px 안쪽으로 배치','데스크톱·태블릿에서 헤더 폭 계산과 버튼 경계 정렬을 안정화','모바일에서도 두 버튼이 헤더 안쪽 여백을 유지하도록 보정'],'scopeNote':'로컬 학습용 PC 조립 시뮬레이터.'}
marker='</script><script>\n/* PC LAB content pack 0.1.0.'
if marker not in s: raise SystemExit('release marker missing')
j=json.dumps(entry,ensure_ascii=False,separators=(',',':'))
inject="</script><script>\nwindow.PCRelease.version='2.3.5';window.PCRelease.date='2026-09-14';window.PCRelease.buildId='2.3.5-652ba33c4b49';window.PCRelease.title="+json.dumps(entry['title'],ensure_ascii=False)+";window.PCRelease.changes="+json.dumps(entry['changes'],ensure_ascii=False)+";window.PCRelease.scopeNote="+json.dumps(entry['scopeNote'],ensure_ascii=False)+";window.PCRelease.history=["+j+",...window.PCRelease.history];\n</script><script>\n/* PC LAB content pack 0.1.0."
s=s.replace(marker,inject,1)
p.write_text(s)
