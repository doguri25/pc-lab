/* Record the next release once, in Korea time. Usage:
 * node scripts/release.cjs --notes release-notes.json [--bump patch|minor|major]
 * The builder propagates this record to game UI, package, changelog, HTML & manifest. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const root=path.resolve(__dirname,'..'),args=process.argv.slice(2),get=(n,d)=>args.includes(n)?args[args.indexOf(n)+1]:d;
const noteFile=get('--notes');if(!noteFile){console.error('Usage: node scripts/release.cjs --notes notes.json [--bump patch|minor|major]');process.exit(1);}
const history=JSON.parse(fs.readFileSync(path.join(root,'releases.json'),'utf8')),notes=JSON.parse(fs.readFileSync(path.resolve(noteFile),'utf8'));
if(typeof notes.title!=='string'||!notes.title.trim()||!Array.isArray(notes.changes)||!notes.changes.length||notes.changes.some(c=>typeof c!=='string'||!c.trim()))throw Error('title and non-empty changes are required.');
const bump=get('--bump','patch');if(!['patch','minor','major'].includes(bump))throw Error('Invalid bump');let [a,b,c]=history[0].version.split('.').map(Number);if(bump==='major'){a++;b=0;c=0;}else if(bump==='minor'){b++;c=0;}else c++;
const version=[a,b,c].join('.'),date=new Intl.DateTimeFormat('sv-SE',{timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
history.unshift({version,date,timezone:'Asia/Seoul',channel:notes.channel||'stable-local',title:notes.title.trim(),changes:notes.changes,scopeNote:notes.scopeNote||history[0].scopeNote});
fs.writeFileSync(path.join(root,'releases.json'),JSON.stringify(history,null,2)+'\n');
cp.execFileSync(process.execPath,['build.cjs'],{cwd:root,stdio:'inherit'});console.log(`Recorded v${version} / ${date} (Asia/Seoul).`);
