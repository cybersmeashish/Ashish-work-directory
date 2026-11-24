"""Structural verification of an initialized capability directory, not security controls."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,csv,hashlib,json,os,platform,re,urllib.parse
ROOT=Path(__file__).resolve().parents[1]

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 catalog=json.loads((ROOT/'catalog.json').read_text());entries=catalog['entries'];problems=[];links=0
 if len(entries)!=33 or [e['id'] for e in entries]!=list(range(1,34)):problems.append('Expected exactly 33 ordered capabilities')
 groups={e['group'] for e in entries}
 if len(groups)!=7 or catalog['groups']!=7 or catalog['capabilities']!=33:problems.append('Group count differs')
 names=[e['folder'] for e in entries]
 if len(set(names))!=33:problems.append('Duplicate folder names')
 for e in entries:
  if not e['folder'].startswith(f"{e['id']:02d}-"):problems.append('Incorrect folder numbering')
  path=ROOT/e['folder']/'README.md'
  if not path.is_file() or e['capability'] not in path.read_text() or e['group'] not in path.read_text():problems.append('Missing or mislabeled capability README')
 numbered=[p.name for p in ROOT.iterdir() if p.is_dir() and re.match(r'^\d\d-',p.name)]
 if set(numbered)!=set(names):problems.append('Unexpected or missing capability directory')
 with (ROOT/'DIRECTORY.csv').open(newline='') as f:rows=list(csv.DictReader(f))
 expected=[{k:str(e[k]) for k in ('id','group','capability','folder','stage')} for e in entries]
 if rows!=expected:problems.append('CSV and catalog differ')
 for path in ROOT.rglob('*.md'):
  for link in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',path.read_text()):
   if urllib.parse.urlparse(link).scheme or link.startswith('#'):continue
   raw=urllib.parse.unquote(link.split('#',1)[0].split('?',1)[0]);target=(path.parent/raw).resolve()
   if not target.is_relative_to(ROOT) or not target.exists():problems.append('Broken local link: '+path.relative_to(ROOT).as_posix()+' -> '+link)
   links+=1
 source={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.rglob('*')) if p.is_file() and not any(x in p.parts for x in ('evidence','__pycache__','.git')) and not p.name.endswith('.pyc')}
 result={'repository':catalog['repository'],'checked_at_utc':datetime.now(timezone.utc).isoformat(),'capability_folders':33,'groups':7,'folder_names':names,'tracked_capability_readmes':33,'catalog_csv_consistent':rows==expected,'local_markdown_links_checked':links,'source_files_hashed':len(source),'runtime':{'python':platform.python_version(),'os':platform.system(),'architecture':platform.machine()},'root_read_only':bool(os.statvfs('/').f_flag & os.ST_RDONLY),'workspace_read_only':bool(os.statvfs(str(ROOT)).f_flag & os.ST_RDONLY),'scope':'Folder organization, labels, navigation and hashes; no capability implementation or operational-control tests','problems':problems}
 (a.out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');(a.out/'source-manifest.json').write_text(json.dumps(source,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ('capability_folders','groups','local_markdown_links_checked','source_files_hashed','problems')},indent=2))
 if problems:raise SystemExit(1)
if __name__=='__main__':main()
