import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {browserRuntime,reportJSON} from './browser-runtime.mjs';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const {call,evaluate,errors,network,close}=await browserRuntime(root);
const checks=[],screenshots=[],layouts=[],firstScreens=[],contrasts=[];
const downloads=path.join(root,'verification','download-check');
await fs.mkdir(downloads,{recursive:true});
await call('Browser.setDownloadBehavior',{behavior:'allow',downloadPath:downloads});
const check=(ok,name)=>checks.push({passed:!!ok,check:name});
const settle=()=>evaluate('document.fonts.ready.then(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))).then(()=>true)');
async function click(selector){
 const pt=await evaluate(`(()=>{const e=document.querySelector(${JSON.stringify(selector)});e.scrollIntoView({block:'center',behavior:'instant'});const r=e.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()`);
 await call('Input.dispatchMouseEvent',{type:'mousePressed',button:'left',clickCount:1,...pt});
 await call('Input.dispatchMouseEvent',{type:'mouseReleased',button:'left',clickCount:1,...pt});await settle();
}
async function shot(name,width,height){
 const s=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width,height,scale:1}});
 await fs.writeFile(path.join(root,'verification',name),Buffer.from(s.data,'base64'));screenshots.push(name);
}
async function layout(name){
 const data=await evaluate(`(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,offenders:[...document.querySelectorAll('body *')].filter(e=>{if(!e.getClientRects().length)return false;const r=e.getBoundingClientRect();return r.right>innerWidth+1||r.left< -1}).map(e=>({tag:e.tagName,id:e.id,class:e.className,width:e.getBoundingClientRect().width}))}))()`);
 layouts.push({name,...data});check(data.scrollWidth<=data.width,name+' has no horizontal overflow');
}
function luminance(colour){
 const channels=colour.match(/[\d.]+/g).slice(0,3).map(Number).map(value=>{
  const channel=value/255;
  return channel<=0.04045?channel/12.92:((channel+0.055)/1.055)**2.4;
 });
 return channels[0]*0.2126+channels[1]*0.7152+channels[2]*0.0722;
}
try{
 for(const width of [390,1440]){
  const height=width===390?844:900;
  await call('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:width===390});
  await call('Page.navigate',{url:pathToFileURL(path.join(root,'index.html')).href});
  for(let i=0;i<100;i++){if(await evaluate('document.readyState==="complete"&&!!document.querySelector("#results")'))break;await new Promise(r=>setTimeout(r,50))}
  await settle();
  check(await evaluate('document.title==="Build Check-in · Instructor field guide"'),width+' page loads');
  const first=await evaluate(`(()=>{
   const quote=document.querySelector('.question-example');const r=quote.getBoundingClientRect();
   return {top:r.top,bottom:r.bottom,height:innerHeight,text:quote.querySelector('p').textContent,
    example:document.querySelectorAll('.output pre')[0].textContent,
    readme:document.querySelector('a[href*="#readme"]').href};
  })()`);
  firstScreens.push({width,...first,text:undefined,example:undefined});
  const question="At version 2, the AI changed the score line and ran the test again. The test still failed with the same message. Why do you think that change didn't help?";
  check(first.top>=0&&first.bottom<=height&&first.text==='“'+question+'”'&&first.example.includes(question),width+' complete model-written question is above the fold');
  check(first.readme==='https://github.com/NickkkLian/build-check-in#readme',width+' setup link points to the GitHub README');
  const palette=await evaluate(`(()=>{
   const root=getComputedStyle(document.documentElement);const style=s=>getComputedStyle(document.querySelector(s));
   const paper=style('body').backgroundColor;
   return {tokens:['--accent','--ink','--muted','--line'].map(t=>root.getPropertyValue(t).trim()),pairs:[
    ['Ink on paper',style('body').color,paper],['Accent on paper',style('nav a').color,paper],
    ['Button text',style('.download').color,style('.download').backgroundColor],
    ['Muted on paper',style('.meta').color,paper],['Muted on limits',style('.meta').color,style('.limits').backgroundColor],
    ['Output text',style('pre').color,style('pre').backgroundColor]]};
  })()`);
  check(palette.tokens.join(',')==='#1f3a6b,#1c2433,#545d6c,#cfd5df',width+' notebook navy tokens match the review');
  for(const [name,foreground,background] of palette.pairs){
   const values=[luminance(foreground),luminance(background)];
   const ratio=(Math.max(...values)+0.05)/(Math.min(...values)+0.05);
   contrasts.push({width,name,foreground,background,ratio});check(ratio>=4.5,width+' '+name+' meets AA contrast');
  }
  await layout(width+' closed');await shot(`first-${width}.png`,width,height);
  for(const selector of ['#start','#example','#evidence']){
   await click(`nav a[href="${selector}"]`);
   check(await evaluate(`location.hash===${JSON.stringify(selector)}`),width+' navigation '+selector);
  }
  for(let index=0;index<4;index++){
   await click(`.output:nth-of-type(${index+1}) summary`);
   check(await evaluate(`document.querySelectorAll('.output')[${index}].open`),width+' opens example '+(index+1));
   await layout(width+' example '+(index+1));
   await click(`.output:nth-of-type(${index+1}) summary`);
   check(await evaluate(`!document.querySelectorAll('.output')[${index}].open`),width+' closes example '+(index+1));
  }
  await click('#results summary');
  check(await evaluate('document.querySelector("#results").open&&document.querySelectorAll("tbody tr").length===15'),width+' all 15 measured checks expand');await layout(width+' results');
  await evaluate('document.querySelectorAll(".output").forEach(e=>e.open=true);window.scrollTo(0,0)');await settle();
  await shot(`full-open-${width}.png`,width,await evaluate('document.documentElement.scrollHeight'));
  check(await evaluate('[...document.querySelectorAll("summary,nav a,.download")].every(e=>e.getBoundingClientRect().height>=44)'),width+' interactive targets at least 44px high');
  await evaluate('document.querySelector("#results").open=false;document.querySelector("#results summary").focus()');
  await call('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13,text:'\r',unmodifiedText:'\r'});await call('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
  await settle();
  check(await evaluate('document.querySelector("#results").open'),width+' disclosure operates by keyboard');
  check(await evaluate('document.querySelector("[download]").href===new URL("build-checkin.zip",location.href).href'),width+' archive download link resolves');
  await click('[download]');
  let downloaded;
  for(let i=0;i<100;i++){
   try{downloaded=await fs.readFile(path.join(downloads,'build-checkin.zip'));break}catch{}
   await new Promise(resolve=>setTimeout(resolve,50));
  }
  check(downloaded?.equals(await fs.readFile(path.join(root,'build-checkin.zip'))),width+' downloaded archive bytes match release');
  await fs.rm(path.join(downloads,'build-checkin.zip'),{force:true});
 }
 check(network.length===0,'Zero external page requests');check(errors.length===0,'Zero browser runtime errors');
}catch(e){check(false,e.message)}finally{
 await close();await fs.rm(downloads,{recursive:true,force:true});const report={passed:checks.every(c=>c.passed),checks,screenshots,firstScreens,contrasts,layouts,network,errors};
 await fs.writeFile(path.join(root,'verification/browser-results.json'),reportJSON(report,root));
 for(const c of checks)process.stdout.write(`${c.passed?'PASS':'FAIL'} ${c.check}\n`);process.exitCode=report.passed?0:1;
}
