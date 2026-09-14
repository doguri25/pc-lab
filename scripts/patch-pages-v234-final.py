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

# Final local release identity.
rep('<title>PC LAB v2.3.4 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.4"><meta name="pc-lab-build" content="2.3.4-3f78610b1dc0">','<title>PC LAB v2.3.4 — 컴퓨터 조립 시뮬레이터</title><meta name="pc-lab-version" content="2.3.4"><meta name="pc-lab-build" content="2.3.4-4490bd72e3c7">','meta build id')

# Replace the intermediate released-screw illustration with the final empty-hole-only lens.
old_lens=''' else{const hole=`<ellipse cx="125" cy="171" rx="48" ry="14" fill="#020f17" opacity=".8"/><circle cx="125" cy="144" r="41" fill="#162f39" stroke="#7f9b8a" stroke-width="4"/><circle cx="125" cy="144" r="22" fill="#041923" stroke="#405f61" stroke-width="3"/>`;const screwArt=`<g class="precision-moving" style="transform-origin:125px 132px"><path d="M112 131h26v45l-13 13-13-13Z" fill="#8dabb0" stroke="#c6d2b7"/><path d="m111 142 27-6m-27 16 27-6m-27 16 27-6m-27 16 27-6" stroke="#334f58" stroke-width="3"/><circle cx="125" cy="123" r="39" fill="url(#lens-metal)" stroke="#e4e5c2" stroke-width="3"/><circle cx="125" cy="123" r="28" fill="none" stroke="#687f83"/><path d="M103 123h44m-22-22v44" stroke="#243e48" stroke-width="9"/><path d="M103 121h44m-24-20v44" stroke="#051d28" stroke-width="4"/></g>`;diagram=hole+(on?screwArt:`<g class="precision-empty-hole" aria-hidden="true"><circle cx="125" cy="144" r="12" fill="#02090d" opacity=".9"/><path d="M110 144h30" stroke="#4f6b68" stroke-width="2" stroke-dasharray="3 4" opacity=".7"/></g>`);}'''
new_lens=''' else if(!on){diagram=`<ellipse cx="125" cy="171" rx="48" ry="14" fill="#020f17" opacity=".8"/><circle cx="125" cy="144" r="41" fill="#162f39" stroke="#7f9b8a" stroke-width="4"/><circle cx="125" cy="144" r="25" fill="#03131b" stroke="#4f6969" stroke-width="3"/><circle cx="125" cy="144" r="14" fill="#01090e" stroke="#263f46" stroke-width="3"/><path d="M114 136q11-9 22 0m-22 8q11-9 22 0m-22 8q11-9 22 0" fill="none" stroke="#49636a" stroke-width="2" opacity=".65"/><text x="125" y="205" text-anchor="middle" fill="#9eb9ad" font-size="11">나사 제거됨 · 빈 나사 구멍</text>`;}\n else{diagram=`<ellipse cx="125" cy="171" rx="48" ry="14" fill="#020f17" opacity=".8"/><circle cx="125" cy="144" r="41" fill="#162f39" stroke="#7f9b8a" stroke-width="4"/><circle cx="125" cy="144" r="22" fill="#041923" stroke="#405f61" stroke-width="3"/><g class="precision-moving" style="transform-origin:125px 132px"><path d="M112 131h26v45l-13 13-13-13Z" fill="#8dabb0" stroke="#c6d2b7"/><path d="m111 142 27-6m-27 16 27-6m-27 16 27-6m-27 16 27-6" stroke="#334f58" stroke-width="3"/><circle cx="125" cy="123" r="39" fill="url(#lens-metal)" stroke="#e4e5c2" stroke-width="3"/><circle cx="125" cy="123" r="28" fill="none" stroke="#687f83"/><path d="M103 123h44m-22-22v44" stroke="#243e48" stroke-width="9"/><path d="M103 121h44m-24-20v44" stroke="#051d28" stroke-width="4"/></g>`;}'''
rep(old_lens,new_lens,'final precision screw removal')

old_style='''<style id="pc-lab-v234-focus-fix">\n.studio-stage .focus-heading{box-sizing:border-box;min-width:0;max-width:calc(100% - 20px);overflow:hidden}\n.studio-stage .focus-heading>span{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}\n.studio-stage .focus-heading>.btn{flex:0 1 auto;min-width:0;max-width:42%;padding:7px 8px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}\n.studio-stage .focus-heading>.detail-on-stage{margin-left:auto}\n@media(max-width:1050px) and (min-width:651px){.studio-stage .focus-heading{gap:6px}.studio-stage .focus-heading>.btn{font-size:.68rem;max-width:44%;padding:6px 7px}.studio-stage .focus-heading>span{font-size:.68rem}}\n@media(max-width:650px){.studio-stage .focus-heading .btn{font-size:.64rem;padding:6px 7px;max-width:48%;white-space:nowrap}.studio-stage .focus-heading>span{display:none}}\n</style>'''
new_style='''<style id="pc-lab-v234-focus-fix">\n.studio-stage .focus-heading,.direct-stage .focus-heading{box-sizing:border-box;width:auto;max-width:calc(100% - 24px);padding-left:10px!important;padding-right:10px!important;overflow:hidden}\n.studio-stage .focus-heading>span,.direct-stage .focus-heading>span{flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}\n.studio-stage .focus-heading>.btn,.direct-stage .focus-heading>.btn{flex:0 0 auto;max-width:42%;box-sizing:border-box}\n.studio-stage .focus-heading>.detail-on-stage,.direct-stage .focus-heading>.detail-on-stage{margin-left:auto;padding-left:10px!important;padding-right:10px!important}\n@media(max-width:650px){.studio-stage .focus-heading,.direct-stage .focus-heading{max-width:calc(100% - 18px);padding-left:7px!important;padding-right:7px!important}.studio-stage .focus-heading>.btn,.direct-stage .focus-heading>.btn{max-width:43%;padding-left:7px!important;padding-right:7px!important}}\n</style>'''
rep(old_style,new_style,'final focus header containment')

# Update generated runtime metadata from the intermediate build to the frozen final build.
s=s.replace("window.PCRelease.buildId='2.3.4-3f78610b1dc0'","window.PCRelease.buildId='2.3.4-4490bd72e3c7'",1)
s=s.replace('"buildId":"2.3.4-3f78610b1dc0"','"buildId":"2.3.4-4490bd72e3c7"',1)

final_entry={
  'version':'2.3.4','date':'2026-09-14','timezone':'Asia/Seoul','channel':'stable-local',
  'title':'3D 작업 헤더 넘침과 나사 확대창 잔상 수정',
  'changes':[
    '3D 작업 확대 화면의 상단 헤더를 box-sizing과 내부 좌우 여백 기준으로 다시 정리하여 ‘3D 작업대로’와 ‘자세히 보기’ 버튼이 헤더 배경 바깥으로 튀어나오지 않도록 수정',
    '헤더 가운데 부품명 영역에 최소폭 0과 말줄임 처리를 적용하고 양쪽 버튼은 flex 축소 대상에서 제외하여 좁은 화면에서도 버튼과 배경 경계가 겹치지 않도록 보강',
    '정밀 나사 확대창에서 나사를 푼 뒤에도 이동된 나사 본체가 계속 보이던 표현을 제거하고, 풀린 상태에서는 실제 나사 몸체를 완전히 숨긴 뒤 빈 나사 구멍과 나사산만 표시하도록 변경',
    '덮개·메인보드·쿨러·GPU 브래킷·M.2 등 공통 정밀 나사 확대 UI가 동일한 제거 표현을 사용하도록 통일',
    '기존 엔진·저장·릴리스 회귀검사와 데스크톱·모바일 3D 헤더 폭, 정밀 나사 제거 상태를 Chromium에서 재검증'
  ],
  'scopeNote':'로컬 학습용 PC 조립 시뮬레이터. 나사·헤더 UI는 초보자 학습을 위한 시각화이며 실제 제조사 서비스 도면의 정밀 치수와 동일하지 않을 수 있음.'
}
# Replace the first v2.3.4 history object if present so release dialog matches final local notes.
needle='window.PCRelease.history=['
pos=s.find(needle)
if pos!=-1:
    start=pos+len(needle)
    if s.startswith('{',start):
        depth=0; in_str=False; esc=False; end=None
        for i,ch in enumerate(s[start:],start):
            if in_str:
                if esc: esc=False
                elif ch=='\\': esc=True
                elif ch=='"': in_str=False
                continue
            if ch=='"': in_str=True
            elif ch=='{': depth+=1
            elif ch=='}':
                depth-=1
                if depth==0:
                    end=i+1; break
        if end:
            s=s[:start]+json.dumps(final_entry,ensure_ascii=False,separators=(',',':'))+s[end:]

path.write_text(s)
