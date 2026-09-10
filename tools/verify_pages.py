"""Compare deployed pages/assets with exact bytes from a specified Git commit."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
import hashlib,json,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
BASE='https://pheanor-agent.github.io/p-hermes-v2/'

def main():
    commit=sys.argv[1] if len(sys.argv)>1 else 'HEAD'
    sha=subprocess.check_output(['git','rev-parse',commit],cwd=ROOT,text=True).strip()
    paths=['index.html','assets/site.css','assets/site.js','assets/HermesKR.woff2','assets/font-manifest.json','slides/assets/deck.js','slides/assets/deck.css']
    paths += [str(p.relative_to(ROOT/'docs')).replace('\\','/') for p in (ROOT/'docs/lectures').glob('*.html')]
    paths += [f'slides/{s}/index.html' for s in ['overview','tasks','knowledge','catalog','image','video']]
    paths += [f'{kind}/{s}.html' for kind in ['blog','wiki'] for s in ['start','tasks','knowledge','catalog','image','video','integration']]
    paths += [str(p.relative_to(ROOT/'docs')).replace('\\','/') for p in (ROOT/'docs/slides/assets/media').iterdir() if p.is_file()]
    def check(path):
        expected=subprocess.check_output(['git','show',f'{sha}:docs/{path}'],cwd=ROOT)
        request=Request(BASE+path+'?review='+sha,headers={'User-Agent':'p-hermes-release-verification','Cache-Control':'no-cache'})
        with urlopen(request,timeout=30) as response:actual=response.read();status=response.status
        return {'path':path,'status':status,'bytes':len(actual),'sha256':hashlib.sha256(actual).hexdigest(),'matches_commit':actual==expected}
    with ThreadPoolExecutor(max_workers=4) as pool:checks=list(pool.map(check,paths))
    report={'commit':sha,'base':BASE,'checked_at':datetime.now(timezone.utc).isoformat(),'files':checks,'ok':all(x['status']==200 and x['matches_commit'] for x in checks)}
    out=ROOT/'.work/pages-review.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'commit':sha,'files':len(checks),'ok':report['ok'],'mismatches':[x['path'] for x in checks if not x['matches_commit']]}))
    return 0 if report['ok'] else 1

if __name__=='__main__':sys.exit(main())
