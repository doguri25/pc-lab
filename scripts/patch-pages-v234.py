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

# Release identity in the document head.
rep('<title>PC LAB v2.3.3 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.3"><meta name="pc-lab-build" content="2.3.3-2b16f203e5d9">','<title>PC LAB v2.3.4 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.4"><meta name="pc-lab-build" content="2.3.4-3f78610b1dc0">','meta')

# A released precision screw must disappear entirely, leaving only the empty hole.
old_lens=''' else{diagram=`<ellipse cx="125" cy="171" rx="48" ry="14" fill="#020f17" opacity=".8"/><circle cx="125" cy="144" r="41" fill="#162f39" stroke="#7f9b8a" stroke-width="4"/><circle cx="125" cy="144" r="22" fill="#041923" stroke="#405f61" stroke-width="3"/><g class="precision-moving" style="transform-origin:125px 132px" ${!on?'transform="translate(36 -59) rotate(-24 125 132)"':''}><path d="M112 131h26v45l-13 13-13-13Z" fill="#8dabb0" stroke="#c6d2b7"/><path d="m111 142 27-6m-27 16 27-6m-27 16 27-6m-27 16 27-6" stroke="#334f58" stroke-width="3"/><circle cx="125" cy="123" r="39" fill="url(#lens-metal)" stroke="#e4e5c2" stroke-width="3"/><circle cx="125" cy="123" r="28" fill="none" stroke="#687f83"/><path d="M103 123h44m-22-22v44" stroke="#243e48" stroke-width="9"/><path d="M103 121h44m-24-20v44" stroke="#051d28" stroke-width="4"/></g>`;}'''
new_lens=''' else{const hole=`<ellipse cx="125" cy="171" rx="48" ry="14" fill="#020f17" opacity=".8"/><circle cx="125" cy="144" r="41" fill="#162f39" stroke="#7f9b8a" stroke-width="4"/><circle cx="125" cy="144" r="22" fill="#041923" stroke="#405f61" stroke-width="3"/>`;const screwArt=`<g class="precision-moving" style="transform-origin:125px 132px"><path d="M112 131h26v45l-13 13-13-13Z" fill="#8dabb0" stroke="#c6d2b7"/><path d="m111 142 27-6m-27 16 27-6m-27 16 27-6m-27 16 27-6" stroke="#334f58" stroke-width="3"/><circle cx="125" cy="123" r="39" fill="url(#lens-metal)" stroke="#e4e5c2" stroke-width="3"/><circle cx="125" cy="123" r="28" fill="none" stroke="#687f83"/><path d="M103 123h44m-22-22v44" stroke="#243e48" stroke-width="9"/><path d="M103 121h44m-24-20v44" stroke="#051d28" stroke-width="4"/></g>`;diagram=hole+(on?screwArt:`<g class="precision-empty-hole" aria-hidden="true"><circle cx="125" cy="144" r="12" fill="#02090d" opacity=".9"/><path d="M110 144h30" stroke="#4f6b68" stroke-width="2" stroke-dasharray="3 4" opacity=".7"/></g>`);}'''
rep(old_lens,new_lens,'precision screw removal')

# Keep both focus-header buttons inside the header line at narrow widths.
style='''<style id="pc-lab-v234-focus-fix">
.studio-stage .focus-heading{box-sizing:border-box;min-width:0;max-width:calc(100% - 20px);overflow:hidden}
.studio-stage .focus-heading>span{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.studio-stage .focus-heading>.btn{flex:0 1 auto;min-width:0;max-width:42%;padding:7px 8px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.studio-stage .focus-heading>.detail-on-stage{margin-left:auto}
@media(max-width:1050px) and (min-width:651px){.studio-stage .focus-heading{gap:6px}.studio-stage .focus-heading>.btn{font-size:.68rem;max-width:44%;padding:6px 7px}.studio-stage .focus-heading>span{font-size:.68rem}}
@media(max-width:650px){.studio-stage .focus-heading .btn{font-size:.64rem;padding:6px 7px;max-width:48%;white-space:nowrap}.studio-stage .focus-heading>span{display:none}}
</style>'''
if '</head>' not in s: raise SystemExit('head close not found')
s=s.replace('</head>',style+'</head>',1)

entry={
  'version':'2.3.4','date':'2026-09-14','timezone':'Asia/Seoul','channel':'stable-local',
  'title':'정밀 나사 제거 표시와 확대 작업 헤더 경계 수정',
  'changes':[
    '정밀 확대창에서 나사를 풀었을 때 상태 글자만 풀림으로 바뀌고 나사 그림이 확대창 안에 계속 남던 문제를 수정하여, 해제 직후 나사 몸체는 완전히 사라지고 빈 나사 구멍만 표시되도록 변경',
    '덮개 나사뿐 아니라 보드·쿨러·GPU 브래킷·M.2·SATA·PSU 등 screw 스타일을 공유하는 모든 정밀 나사 확대 화면에 동일한 제거 표시 규칙을 적용',
    '작업대의 확대 작업 헤더에서 3D 작업대로 및 자세히 보기 버튼이 헤더 우측 경계를 넘어가던 문제를 수정하고 버튼의 flex 축소·최대 폭·overflow 규칙을 보강',
    '좁은 데스크톱·태블릿에서는 확대 작업 제목을 말줄임하고, 모바일에서는 가운데 제목을 숨겨 두 작업 버튼이 헤더 선 안에서 안정적으로 배치되도록 조정',
    '기존 조립·저장·릴리스 회귀검사와 정밀 나사 제거·헤더 경계 데스크톱/모바일 브라우저 검사를 추가 검증'
  ],
  'scopeNote':'로컬 학습용 PC 조립 시뮬레이터. 나사·부품 위치는 초보자 학습용 도식이며 실제 제조사 서비스 도면의 정밀 치수를 의미하지 않음.'
}
marker='</script><script>\n/* PC LAB content pack 0.1.0.'
if marker not in s: raise SystemExit('release marker not found')
j=json.dumps(entry,ensure_ascii=False,separators=(',',':'))
inject="</script><script>\nwindow.PCRelease.version='2.3.4';window.PCRelease.date='2026-09-14';window.PCRelease.buildId='2.3.4-3f78610b1dc0';window.PCRelease.title="+json.dumps(entry['title'],ensure_ascii=False)+";window.PCRelease.changes="+json.dumps(entry['changes'],ensure_ascii=False)+";window.PCRelease.scopeNote="+json.dumps(entry['scopeNote'],ensure_ascii=False)+";window.PCRelease.history=["+j+",...window.PCRelease.history];\n</script><script>\n/* PC LAB content pack 0.1.0."
s=s.replace(marker,inject,1)
path.write_text(s)
