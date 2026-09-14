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

rep('<title>PC LAB v2.3.9 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.9"><meta name="pc-lab-build" content="2.3.9-69cb4cc7a858">',
    '<title>PC LAB v2.3.11 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.11"><meta name="pc-lab-build" content="2.3.11-10d1a00d47bd">',
    'release identity')

style=r'''<style id="pc-lab-v2311-mobile-fix">
@media(max-width:650px){
  .hero{min-height:428px!important}
  .hero p{margin-bottom:8px!important}
  .hero-copy>.flex{gap:4px!important;transform:translateY(-5px)}
  .hero-copy .btn{min-height:44px;padding:8px 14px}
  .hero-footnote{bottom:0!important}
  .studio-stage{height:clamp(600px,74dvh,660px)!important;min-height:600px!important}
  .studio-viewport{inset:94px 0 239px!important}
  .studio-stage .direct-canvas{inset:96px 8px 239px!important}
  .studio-stage.has-focus .direct-canvas{inset:112px 8px 239px!important}
  .detached-workbench{left:8px!important;right:8px!important;bottom:142px!important;width:auto!important;max-width:none!important;min-height:0!important;height:82px!important;padding:6px 8px!important;box-sizing:border-box!important;display:grid!important;grid-template-columns:92px minmax(0,1fr);gap:7px;align-items:center;overflow:hidden;border-radius:10px}
  .detached-workbench .tray-title{min-width:0;align-self:center}
  .detached-workbench .tray-title strong{font-size:.69rem;line-height:1.35;white-space:normal!important;overflow:visible!important;text-overflow:clip!important;word-break:keep-all}
  .detached-workbench .tray-title span{display:none!important}
  .detached-workbench .tray-visuals{margin-top:0!important;height:64px;min-height:0!important;max-width:100%;display:flex;align-items:center;gap:5px;overflow-x:auto;overflow-y:hidden;scrollbar-width:thin;overscroll-behavior-x:contain}
  .detached-workbench .tray-visual{flex:0 0 50px;min-width:50px;padding:3px}
  .detached-workbench .tray-visual img{max-width:44px;height:33px}
  .detached-workbench .tray-empty{padding:0 4px;font-size:.66rem;line-height:1.5;align-self:center}
  .studio-stage .direct-instruction{bottom:52px!important;left:8px!important;right:8px!important}
  .studio-stage .stage-bottom{bottom:7px!important;left:8px!important;right:8px!important}
  .studio-stage .stage-bottom .btn{min-height:37px}
  .studio-label{top:101px}
}
@media(max-width:360px){.hero-copy{padding-bottom:26px!important}}
</style>'''
if '</head>' not in s: raise SystemExit('head close missing')
s=s.replace('</head>',style+'</head>',1)

entry10={'version':'2.3.10','date':'2026-09-14','timezone':'Asia/Seoul','channel':'stable-local','title':'모바일 작업대 화면 분리와 부품 보관대 최적화','changes':['휴대폰 세로 화면에서 분리 부품 보관대가 3D/2D 작업면의 하단을 덮어 본체가 가려지던 문제를 수정','모바일 작업대를 상단 조작 영역, 본체 작업 화면, 분리 부품 보관대, 작업 안내, 하단 버튼의 독립 영역으로 재배치하여 서로 겹치지 않도록 조정','분리 부품 보관대를 모바일에서 낮은 가로형 도크로 바꾸고 내부 부품은 좌우 스크롤로 확인할 수 있도록 최적화','작업대 높이를 휴대폰 화면 크기에 맞춰 유동적으로 확보하고 3D 작업 화면과 2D 확대 작업 모두 보관대 위에서 끝나도록 안전 여백을 추가','320~430px 폭의 휴대폰 화면에서 본체 작업 영역, 보관대, 작업 안내, 하단 조작 버튼이 겹치지 않는지 브라우저로 검증'],'scopeNote':'모바일 작업대는 세로 화면에서 조작 영역이 겹치지 않도록 학습용 UI를 최적화하며, 실제 하드웨어의 물리적 작업 공간 비율을 의미하지 않습니다.'}
entry11={'version':'2.3.11','date':'2026-09-14','timezone':'Asia/Seoul','channel':'stable-local','title':'모바일 메인 배너 버튼과 하단 문구 겹침 수정','changes':['휴대폰 세로 화면의 메인 배너에서 조립 작업대로 가기·첫 의뢰 살펴보기 버튼과 하단 3D HARDWARE STUDIO 문구가 겹쳐 보이던 문제를 수정','모바일 메인 배너의 버튼군 간격과 위치, 배너 하단 안전 영역을 조정해 두 버튼과 하단 문구가 서로 독립적으로 보이도록 정리','컴퓨터 3D 미리보기와 배너 하단 문구가 겹쳐 보이는 기존 연출은 그대로 유지하고 버튼과 문구 사이의 충돌만 제거','320px·390px·430px 폭의 모바일 화면에서 두 메인 배너 버튼과 하단 문구가 서로 겹치지 않는지 브라우저로 검증'],'scopeNote':'모바일 홈 배너의 터치 버튼 가독성과 간격만 조정하며, 3D 컴퓨터 미리보기와 배너 하단 문구의 겹침 연출은 유지합니다.'}
marker='</script><script>\n/* PC LAB content pack 0.1.0.'
if marker not in s: raise SystemExit('release marker missing')
inject=("</script><script>\n"
 "window.PCRelease.version='2.3.11';window.PCRelease.date='2026-09-14';window.PCRelease.buildId='2.3.11-10d1a00d47bd';"
 "window.PCRelease.title="+json.dumps(entry11['title'],ensure_ascii=False)+";"
 "window.PCRelease.changes="+json.dumps(entry11['changes'],ensure_ascii=False)+";"
 "window.PCRelease.scopeNote="+json.dumps(entry11['scopeNote'],ensure_ascii=False)+";"
 "window.PCRelease.history=["+json.dumps(entry11,ensure_ascii=False,separators=(',',':'))+","+json.dumps(entry10,ensure_ascii=False,separators=(',',':'))+",...window.PCRelease.history];\n"
 "</script><script>\n/* PC LAB content pack 0.1.0.")
s=s.replace(marker,inject,1)
p.write_text(s)
