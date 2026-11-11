#!/usr/bin/env python3
"""Local packaging and command-line checks with fictional temporary inputs."""
from pathlib import Path
import ast,json,re,subprocess,sys,tempfile,zipfile,os
from html import unescape
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(ok,name):
    checks.append({'passed':bool(ok),'check':name})
    print(('PASS ' if ok else 'FAIL ')+name)
skill=ROOT/'build-checkin'
with zipfile.ZipFile(ROOT/'build-checkin.zip') as z:
    names=z.namelist()
    expected=sorted(p.relative_to(ROOT).as_posix() for p in skill.rglob('*') if p.is_file())
    check(sorted(names)==expected and len(names)==len(set(names)), 'Archive contains exactly the installable skill folder')
    check(all(n.startswith('build-checkin/') and '..' not in Path(n).parts for n in names), 'Archive paths are safe')
    check(z.testzip() is None and all(z.read(n)==(ROOT/n).read_bytes() for n in names),'Archive integrity and every member match the skill')
for p in sorted(skill.rglob('*.py')):
    ast.parse(p.read_text());check(True,'Python parses '+p.relative_to(ROOT).as_posix())
for p in sorted(skill.rglob('*.json')):
    json.loads(p.read_text());check(True,'JSON parses '+p.relative_to(ROOT).as_posix())
for p in sorted(skill.rglob('*.md')):
    links=re.findall(r'\]\(([^)]+)\)',p.read_text())
    check(all((p.parent/x).is_file() for x in links if not x.startswith(('http','#'))),'Skill document links resolve '+p.name)
rows=json.loads((ROOT/'verification/measured-results.json').read_text())['rows']
page=(ROOT/'index.html').read_text()
page_rows = re.findall(r'<tr><th scope="row">(.*?)<small>(.*?)</small></th><td>(.*?)</td><td>(.*?)</td></tr>', page)
check(len(rows) == 15 and [(unescape(label), direction, plain, skill) for label, direction, plain, skill in page_rows] ==
      [(x['check'], x['direction'], x['plain'], x['skill']) for x in rows],
      'All 15 measured rows match the page labels, directions and counts')
denominators=json.loads((ROOT/'verification/measured-results.json').read_text())['drill_denominators']
agreement=next(row for row in rows if row['check'].startswith('Drill made without'))
prediction=next(row for row in rows if row['check'].startswith('Students predict'))
total=12*3
check(total-denominators['runs_without_agreement']==denominators['skill_drills_made']==21 and
      denominators['skill_drills_made']+denominators['plain_drills_without_agreement']==denominators['plain_drills_made']==29 and
      agreement['plain']=='8 of 15 runs' and agreement['skill']=='0 of 15' and
      prediction['plain']=='0 of 29 drills' and prediction['skill']=='21 of 21',
      'Drill denominators reconcile with the measured agreement and content rows')
with tempfile.TemporaryDirectory(dir=ROOT/'verification',prefix='helper-fixture-') as tmp:
    base=Path(tmp)
    def write(name,data): (base/name).write_text(json.dumps(data))
    def history(events): return {'versions':[{'id':'snapshot:1','evidence':['snapshot:1:app.py']}],'prompts':[],'evidence':events,'failure_evidence':[]}
    def event(id_,command,outcome): return [{'id':'tool:'+id_,'kind':'command_proposal','command':command},{'id':'result:'+id_,'kind':'tool_result','tool_evidence':'tool:'+id_,'outcome':outcome}]
    write('unresolved.json',history(event('a','check','failed')+event('b','other','reported_pass')))
    write('resolved.json',history(event('a','check','failed')+event('b','check','reported_pass')))
    (base/'answers.md').write_text('Q1. What happened?\nA1. I changed the button.\n\nQ2. Why?\nA2.\n')
    write('class.json',{'students':[{'label':'A','history':'unresolved.json','last_checkin_version':'snapshot:1','answers':None},{'label':'B','history':'resolved.json','last_checkin_version':'missing','answers':'answers.md'}]})
    cli=[sys.executable,'-B',str(skill/'scripts/class_list.py'),str(base/'class.json')]
    result=subprocess.run(cli+['--json'],capture_output=True,text=True,check=True); data=json.loads(result.stdout)
    check(data[0]['unresolved']==[['result:a']] and data[0]['no_new_version'] and not data[0]['answers_returned'],'Unrelated command pass preserves failure and missing-answer flag')
    check(not data[1]['unresolved'] and data[1]['no_new_version'] is None and data[1]['answer_count']==1,'Same-command pass resolves failure and missing baseline stays unknown')
    text=subprocess.run(cli,capture_output=True,text=True,check=True).stdout
    check('Talk to first' in text and 'I changed' not in text,'Class table prints contact flags without copying answers')
    project=base/'project';project.mkdir();(project/'app.py').write_text('print(1)\n')
    (base/'chat.txt').write_text('USER: The button is missing\nASSISTANT: Check the label\n')
    context=json.loads((skill/'context-template.json').read_text());context['adult_runner_confirmed']=True;context['student_name']='Sample';write('context.json',context)
    cli=[sys.executable,'-B',str(skill/'scripts/extract_history.py'),str(project),'--context',str(base/'context.json'),'--chat',str(base/'chat.txt'),'--out',str(base/'history.json')]
    env=dict(os.environ,TMPDIR=tmp)
    result=subprocess.run(cli,capture_output=True,text=True,env=env)
    check(result.returncode==0,'Extractor normal CLI reads supplied fictional project and chat')
    if result.returncode==0:
        data=json.loads((base/'history.json').read_text());check(len(data['prompts'])==1,'Extractor records the USER prompt')
report={'passed':all(x['passed'] for x in checks),'checks':checks}
(ROOT/'verification/check-results.json').write_text(json.dumps(report,indent=2)+'\n')
raise SystemExit(0 if report['passed'] else 1)
