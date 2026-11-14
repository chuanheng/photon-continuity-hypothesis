"""Reproduce the v0.86 local source/test inventory.

Requires /mnt/data/photon_v050...v085 and optional *_complete.zip files.
This is a SOURCE-CODE audit, not a claim of empirical photon identity.
"""
import json,os,pathlib,re,subprocess,sys,tempfile,zipfile
ROOT=pathlib.Path('/mnt/data')
def inventory():
    out=[]
    for v in range(50,86):
        name=f'photon_v{v:03d}'
        path=ROOT/name
        tests=path/'tests'
        original=list(path.rglob('*.py')) if path.is_dir() else []
        archive=ROOT/(name+'_complete.zip')
        archive_available=archive.exists()
        test_status='missing'
        test_count=None
        if tests.is_dir() and list(tests.glob('test_*.py')):
            root=path
        elif archive_available:
            temp=tempfile.TemporaryDirectory(prefix='photon-v086-')
            with zipfile.ZipFile(archive) as z:
                if any('..' in pathlib.PurePosixPath(i.filename).parts or pathlib.PurePosixPath(i.filename).is_absolute() for i in z.infolist()):
                    raise RuntimeError('unsafe archive member')
                z.extractall(temp.name)
            root=pathlib.Path(temp.name)/name
            if not root.is_dir():root=pathlib.Path(temp.name)
            tests=root/'tests'
        else:root=None
        if root is not None and tests.is_dir() and list(tests.glob('test_*.py')):
            e=os.environ.copy();e['PYTHONPATH']=str(root)
            cmd=[sys.executable,'-m','unittest','discover','-s',str(tests),'-v']
            try:
                p=subprocess.run(cmd,cwd=root,env=e,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=30)
                test_status='pass' if p.returncode==0 else 'fail'
                m=re.search(r'Ran\s+(\d+)\s+tests?',p.stdout)
                test_count=int(m.group(1)) if m else None
            except subprocess.TimeoutExpired:test_status='timeout'
        if 'temp' in locals():
            temp.cleanup();del temp
        out.append({'version':'v0.'+str(v).zfill(2),'local_python_files':len(original),
                    'zip_fallback':archive_available,'test_status':test_status,'tests':test_count})
    return out
if __name__=='__main__':
    data=inventory()
    print(json.dumps({'versions':len(data),'passed_versions':sum(x['test_status']=='pass' for x in data),
       'passed_tests':sum(x['tests'] or 0 for x in data),
       'missing':[x['version'] for x in data if x['test_status']!='pass'],
       'records':data},ensure_ascii=False,indent=2))
