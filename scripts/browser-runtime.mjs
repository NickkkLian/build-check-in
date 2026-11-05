// Review helper: fresh headless profile, CDP over pipes, no personal browser state.
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawn} from 'node:child_process';

export async function browserRuntime(root,onEvent=()=>{}){
 const out=path.join(root,'verification');await fs.mkdir(out,{recursive:true});
 const profile=await fs.mkdtemp(path.join(out,'browser-profile-'));
 const temp=path.join(profile,'tmp');await fs.mkdir(temp);
 const executable=process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
 const browser=spawn(executable,[
  '--headless=new','--remote-debugging-pipe',`--user-data-dir=${profile}`,
  '--no-first-run','--no-default-browser-check','--disable-background-networking',
  '--disable-component-update','--disable-sync','--disable-extensions','--disable-default-apps',
  '--disable-breakpad','--disable-crash-reporter','--metrics-recording-only',
  '--password-store=basic','--use-mock-keychain','--no-proxy-server',
  '--disable-features=MediaRouter,OptimizationHints,AutofillServerCommunication',
  '--host-resolver-rules=MAP * ~NOTFOUND','about:blank'
 ],{stdio:['ignore','ignore','pipe','pipe','pipe'],env:{PATH:process.env.PATH,TMPDIR:temp,LANG:'en_CA.UTF-8'}});
 let next=0,buffer=Buffer.alloc(0),session,log='';const pending=new Map(),errors=[],network=[];
 browser.stderr.on('data',d=>log+=d);
 browser.on('error',e=>{errors.push(e.message);for(const p of pending.values()){clearTimeout(p.timer);p.reject(e)}pending.clear()});
 function send(method,params={},target){return new Promise((resolve,reject)=>{
  const id=++next,timer=setTimeout(()=>{pending.delete(id);reject(Error('Browser timeout: '+method))},15000);
  pending.set(id,{resolve,reject,timer});const m={id,method,params};if(target)m.sessionId=target;
  browser.stdio[3].write(JSON.stringify(m)+'\0');
 })}
 const call=(method,params={})=>send(method,params,session);
 browser.stdio[4].on('data',d=>{
  buffer=Buffer.concat([buffer,d]);let boundary;
  while((boundary=buffer.indexOf(0))>=0){
   const raw=buffer.subarray(0,boundary).toString();buffer=buffer.subarray(boundary+1);if(!raw)continue;
   const m=JSON.parse(raw);
   if(m.id){const p=pending.get(m.id);if(p){clearTimeout(p.timer);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result)}}
   else {
    if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails.exception?.description||m.params.exceptionDetails.text);
    if(m.method==='Network.requestWillBeSent'&&/^(https?|wss?|ftp):/.test(m.params.request.url))network.push(m.params.request.url);
    if(m.method==='Fetch.requestPaused'){network.push(m.params.request.url);send('Fetch.failRequest',{requestId:m.params.requestId,errorReason:'BlockedByClient'},m.sessionId).catch(e=>errors.push(e.message))}
    onEvent(m,call);
   }
  }
 });
 await send('Browser.getVersion');
 const target=await send('Target.createTarget',{url:'about:blank'});
 session=(await send('Target.attachToTarget',{targetId:target.targetId,flatten:true})).sessionId;
 await call('Page.enable');await call('Runtime.enable');await call('Network.enable');
 await call('Network.setBlockedURLs',{urls:['http://*','https://*','ws://*','wss://*','ftp://*']});
 await call('Fetch.enable',{patterns:['http://*','https://*','ws://*','wss://*','ftp://*'].map(urlPattern=>({urlPattern}))});
 const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(r.exceptionDetails.exception?.description||r.exceptionDetails.text);return r.result.value};
 const close=async()=>{
  try{await send('Browser.close')}catch{}
  if(browser.exitCode===null)browser.kill('SIGTERM');
  await new Promise(resolve=>browser.exitCode!==null?resolve():browser.once('exit',resolve));
  for(const p of pending.values())clearTimeout(p.timer);
  await fs.rm(profile,{recursive:true,force:true});
 };
 return {call,evaluate,errors,network,close};
}

export function reportJSON(value,root){
 return JSON.stringify(value,(_key,v)=>typeof v==='string'?v.split(root).join('.'):v,2)+'\n';
}
