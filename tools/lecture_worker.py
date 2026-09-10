"""Execute one real educational step per stdin line for browser recording.

All inputs are synthetic. Temporary writes remain in a scoped .work directory.
Receipts intentionally select only the fields discussed on screen.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from p_hermes.store import Store
from p_hermes.core import ContractError
from p_hermes.media import inspect_video
from p_hermes.__main__ import demo

def main():
    scenario=sys.argv[1]
    work=ROOT/'.work';work.mkdir(exist_ok=True)
    with TemporaryDirectory(prefix='recording-',dir=work) as folder:
        folder=Path(folder);assert folder.resolve().is_relative_to(work.resolve())
        store=Store(folder/'work.sqlite3');job=None
        for raw in sys.stdin:
            step=int(raw.strip())
            if scenario=='cas':
                if step==0:
                    job=store.create_job('record-demo',{'purpose':'검토 보고서'})
                    for i in range(7):job=store.act(job['id'],job['revision'],'revise',plan={'purpose':f'검토 보고서 {i+1}'})
                    a=store.job(job['id']);b=store.job(job['id'])
                    command='A = store.job(id)\nB = store.job(id)'
                    output={'A_revision':a['revision'],'B_revision':b['revision'],'state':job['state']}
                elif step==1:
                    job=store.act(job['id'],a['revision'],'approve',approved_digest=a['plan_digest'])
                    command="store.act(id, A_revision, 'approve', ...)"
                    output={'revision':job['revision'],'state':job['state']}
                elif step==2:
                    command="store.act(id, B_revision, 'approve', ...)"
                    try:store.act(job['id'],b['revision'],'approve',approved_digest=b['plan_digest'])
                    except ContractError as exc:output={'error':str(exc),'current_revision':store.job(job['id'])['revision']}
                    else:raise AssertionError('Expected stale revision rejection')
                else:
                    job=store.act(job['id'],job['revision'],'revise',plan={'purpose':'보고서와 변경 요약'})
                    command="store.act(id, revision, 'revise', plan=new_plan)"
                    output={k:job[k] for k in ['revision','state','approved_digest']}
            elif scenario=='knowledge':
                item=lambda v:{'id':f'guide-v{v}','title':f'연결 안내 v{v}','body':f'설명용 연결 안내 {v}','source_ref':f'synthetic:guide-v{v}','license_ref':'CC0-1.0','public':True}
                if step==0:
                    store.register_knowledge(item(1));store.register_knowledge(item(2))
                    command='store.register_knowledge(v1)\nstore.register_knowledge(v2)\nstore.search("연결")'
                    output={'hits':[x['id'] for x in store.search('연결')]}
                elif step==1:
                    store.retire_knowledge('guide-v1')
                    command='store.retire_knowledge("guide-v1")\nSELECT id, state FROM knowledge'
                    output={'records':[dict(x) for x in store.db.execute('SELECT id,state FROM knowledge ORDER BY id')]}
                elif step==2:
                    command='store.search("연결")'
                    output={'hits':[x['id'] for x in store.search('연결')]}
                else:
                    command='store.search("접속")'
                    output={'hits':store.search('접속'),'method':'literal substring'}
            elif scenario=='integration':
                target=folder/'demo-output'
                if step==0:
                    result=demo(target)
                    command='p-hermes demo --output demo-output'
                    output={'status':result['status'],'files':sorted(p.name for p in target.iterdir())}
                elif step==1:
                    command='open demo-output/report.json'
                    report=json.loads((target/'report.json').read_text())
                    output=report['execution']
                elif step==2:
                    command='Store("demo-output/workspace.sqlite3")\nreopened.job("studio-demo")'
                    with Store(target/'workspace.sqlite3') as reopened:
                        value=reopened.job('studio-demo');events=reopened.events('studio-demo')
                        output={'state':value['state'],'revision':value['revision'],'events':[x['action'] for x in events]}
                else:
                    command='open demo-output/timeline.json'
                    value=json.loads((target/'timeline.json').read_text())
                    output={'duration_seconds':value['duration_seconds'],'validation':value['validation'],'intervals':[[s['start_seconds'],s['end_seconds']] for s in value['shots']]}
            elif scenario=='probe':
                path=ROOT/'site/slides/media/probe-2s.mp4'
                command='inspect_video("probe-2s.mp4",\n  expected_duration=2)'
                result=inspect_video(path,expected_duration=2)
                if step==0:output={'duration_seconds':result['duration_seconds'],'validation':result['validation']}
                elif step==1:output=result['video_streams'][0]
                else:output={'audio_stream_count':result['audio_stream_count'],'sha256':result['sha256']}
            else:raise ValueError('Unknown recording scenario')
            print(json.dumps({'command':command,'output':output},ensure_ascii=False),flush=True)
        store.close()

if __name__=='__main__':main()
