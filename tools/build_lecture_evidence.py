"""Run the public contracts on synthetic inputs and retain deterministic teaching evidence."""
from copy import deepcopy
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from p_hermes.store import Store
from p_hermes.catalog import resolve, compile_image
from p_hermes.core import ContractError, digest
from p_hermes.media import record_artifact, compile_timeline


def rejected(operation):
    try:
        operation()
    except ContractError as error:
        return str(error)
    raise AssertionError('Expected an actual ContractError')


def build():
    work = ROOT / '.work'
    work.mkdir(exist_ok=True)
    # The temporary workspace is created under this repository's explicitly owned .work directory.
    with TemporaryDirectory(prefix='lecture-evidence-', dir=work) as directory:
        directory = Path(directory)
        assert directory.resolve().is_relative_to(work.resolve())
        result = {'schema_version': 1, 'scope': 'Executed public reference contracts with synthetic inputs.'}
        with Store(directory / 'lesson.sqlite3') as store:
            job = store.create_job('revision-example', {'purpose': '검토 보고서 작성'})
            for index in range(7):
                job = store.act(job['id'], job['revision'], 'revise', plan={'purpose': f'검토 보고서 작성 · 초안 {index + 1}'})
            before = deepcopy(job)
            after = store.act(job['id'], before['revision'], 'approve', approved_digest=job['plan_digest'])
            stale = rejected(lambda: store.act(job['id'], before['revision'], 'approve', approved_digest=job['plan_digest']))
            revised = store.act(job['id'], after['revision'], 'revise', plan={'purpose': '검토 보고서와 변경 요약 작성'})
            result['task'] = {'read_revision': before['revision'], 'after_first_update': after['revision'],
                              'first_state': after['state'], 'stale_error': stale,
                              'revised_state': revised['state'], 'approval_after_revision': revised['approved_digest']}
            # Exercise the transaction rollback, without adding a new public API or modifying source.
            original = store.job(job['id'])
            event_count = len(store.events(job['id']))
            try:
                with store.transaction():
                    store.db.execute("UPDATE jobs SET state='running' WHERE id=?", (job['id'],))
                    raise RuntimeError('synthetic interruption before event append')
            except RuntimeError:
                pass
            assert store.job(job['id']) == original
            assert len(store.events(job['id'])) == event_count
            result['transaction'] = {'state_before': original['state'], 'state_after_rollback': store.job(job['id'])['state'],
                                     'event_count_before': event_count, 'event_count_after': len(store.events(job['id']))}
            approved = store.act(job['id'], revised['revision'], 'approve', approved_digest=revised['plan_digest'])
            running = store.act(job['id'], approved['revision'], 'start')
            unknown = store.act(job['id'], running['revision'], 'unknown', evidence='Execution response interrupted')
            error = rejected(lambda: store.act(job['id'], unknown['revision'], 'complete', evidence='No observation'))
            done = store.act(job['id'], unknown['revision'], 'reconcile_complete', evidence='Synthetic result file was observed')
            result['recovery'] = {'unknown_state': unknown['state'], 'direct_complete_error': error, 'reconciled_state': done['state']}
            items = [
                {'id': 'guide-v1', 'title': '연결 안내 v1', 'body': '설명용 구버전 연결 안내',
                 'source_ref': 'synthetic:guide-v1', 'license_ref': 'CC0-1.0', 'public': True},
                {'id': 'guide-v2', 'title': '연결 안내 v2', 'body': '설명용 새버전 연결 안내',
                 'source_ref': 'synthetic:guide-v2', 'license_ref': 'CC0-1.0', 'public': True},
            ]
            for item in items:
                store.register_knowledge(item)
            search_before = [i['id'] for i in store.search('연결')]
            store.retire_knowledge('guide-v1')
            search_after = [i['id'] for i in store.search('연결')]
            records = [dict(row) for row in store.db.execute('SELECT id,state FROM knowledge ORDER BY id')]
            result['knowledge'] = {'query': '연결', 'before': search_before, 'after': search_after, 'records': records,
                                   'no_semantic_match': [i['id'] for i in store.search('접속')],
                                   'duplicate_error': rejected(lambda: store.register_knowledge(items[1]))}
        request = json.loads((ROOT / 'examples/image-request.json').read_text(encoding='utf-8'))
        selection = resolve(request['catalog'], **request['pin'])
        compiled = compile_image(request['spec'], selection, request['template'])
        changed = deepcopy(request['catalog']); changed[0]['runtime'] = 'another-runtime'
        template_changed = deepcopy(request['template']); template_changed['noise']['inputs']['seed'] = 99
        bad_binding = deepcopy(request['catalog']); bad_binding[0]['bindings']['seed'] = ['canvas', 'width']
        bad_selection = resolve(bad_binding, **request['pin'])
        wider = request['spec'] | {'width': 1920}
        wider_output = compile_image(wider, selection, request['template'])
        result['catalog'] = {'version': request['catalog'][0]['version'], 'original_runtime': request['pin']['runtime'],
                             'changed_runtime': changed[0]['runtime'], 'original_digest': selection['digest'], 'changed_digest': digest(changed[0]),
                             'runtime_error': rejected(lambda: resolve(changed, **request['pin'])),
                             'metadata_digest_error': rejected(lambda: resolve(changed, **(request['pin'] | {'runtime': 'another-runtime'}), expected_digest=selection['digest'])),
                             'template_digest_error': rejected(lambda: compile_image(request['spec'], selection, template_changed)),
                             'binding_error': rejected(lambda: compile_image(request['spec'], bad_selection, request['template'])),
                             'bindings': request['catalog'][0]['bindings']}
        result['image'] = {'spec': request['spec'], 'workflow': compiled['workflow'], 'validation': compiled['validation'],
                           'wider_spec': wider, 'wider_workflow': wider_output['workflow'], 'model_inference': False}
        # A minimal declared image fixture tests reference bytes; it is not a teaching illustration.
        (directory / 'reference.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"/>', encoding='utf-8')
        artifact = record_artifact(directory, 'reference.svg', artifact_id='reference', media_type='image/svg+xml', license_ref='CC0-1.0', input_refs=['synthetic:input'])
        shots = [{'id': 'shot-a', 'purpose': '도입', 'image_ref': 'reference', 'duration_seconds': 2},
                 {'id': 'shot-b', 'purpose': '설명', 'image_ref': 'reference', 'duration_seconds': 3}]
        timeline = compile_timeline(directory, shots, [artifact])
        (directory / 'reference.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="32" height="16"/>', encoding='utf-8')
        result['video'] = {'timeline': timeline, 'changed_reference_error': rejected(lambda: compile_timeline(directory, shots, [artifact])), 'video_encoding': False}
        return result


if __name__ == '__main__':
    result = build()
    output = ROOT / 'content/slides/evidence.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Executed lecture evidence:', ', '.join(k for k in result if k not in {'schema_version', 'scope'}))
