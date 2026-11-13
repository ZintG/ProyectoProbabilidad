/* Plantilla única S01–S12. Construye navegación accesible sobre R Markdown
   estándar o HTML de consulta Pandoc, sin modificar los widgets matemáticos. */
(function(){'use strict';
function create(tag,cls,txt){const el=document.createElement(tag);if(cls)el.className=cls;if(txt!==undefined)el.textContent=txt;return el;}
function setupCourseResets(){
 document.querySelectorAll('.widget').forEach((w,index)=>{
  const inputs=[...w.querySelectorAll('input,select,textarea')].filter(n=>!['button','submit','reset'].includes(n.type));
  if(!inputs.length||w.querySelector('.course-reset'))return;
  const baseline=inputs.map(n=>({node:n,value:n.value,checked:n.checked}));
  const btn=create('button','course-reset','Valores de la guía');btn.type='button';btn.setAttribute('aria-label','Restablecer valores del widget '+(index+1));
  btn.addEventListener('click',()=>{baseline.forEach(({node,value,checked})=>{node.value=value;if(node.type==='checkbox'||node.type==='radio')node.checked=checked;node.dispatchEvent(new Event('input',{bubbles:true}));node.dispatchEvent(new Event('change',{bubbles:true}));});});
  w.insertBefore(btn,w.firstChild);
 });
}
function init(){if(document.querySelector('.course-shell'))return;
 const main=document.querySelector('.main-container')||document.querySelector('main')||document.body;
 const secs=[...main.querySelectorAll('.section.level1,section.level1')].filter(x=>x.querySelector(':scope > h1')?.textContent.trim().startsWith('Bloque '));
 if(!secs.length){document.body.dataset.courseError='No se encontraron los cinco bloques';return;}
 // Detach the original native floating table of contents if present.
 const existingToc=[...document.querySelectorAll('#TOC,.tocify')]; existingToc.forEach(e=>e.hidden=true);
 const titleBlock=main.querySelector('#header,#title-block-header');
 const shell=create('div','course-shell');const side=create('aside','course-sidebar');side.setAttribute('aria-label','Navegación de la sesión');
 const content=create('main','course-content');content.setAttribute('role','main');const toolbar=create('div','course-toolbar');
 const state=create('div');const eyebrow=create('div','course-eyebrow');const counter=create('div','course-counter');
 state.append(eyebrow,counter);const actions=create('div','course-actions');
 const prev=create('button','', '←');prev.title='Tema anterior';prev.setAttribute('aria-label','Tema anterior');
 const next=create('button','', '→');next.title='Tema siguiente';next.setAttribute('aria-label','Tema siguiente');
 const projection=create('button','', 'Proyección');projection.setAttribute('aria-pressed','false');
 actions.append(prev,next,projection);const progress=create('div','course-progress');const bar=create('span');progress.append(bar);toolbar.append(state,actions,progress);
 const intro=create('div','course-intro');const modulesWrap=create('div','course-modules');
 const start=titleBlock||main.firstElementChild; const firstBlock=secs[0];
 // Move all document material before the first block into the common intro.
 let cursor=main.firstChild;let guard=0;while(cursor&&cursor!==firstBlock&&guard++<10000){const following=cursor.nextSibling;if(!existingToc.includes(cursor))intro.append(cursor);cursor=following;}
 // R Markdown may wrap introductory material in a root section or a header.
 if(titleBlock && !intro.contains(titleBlock)) intro.prepend(titleBlock);
 const allBlocks=secs.map((section,i)=>{
  // In standard Rmd, headings are direct children of a section.div.level1.
  const header=section.querySelector(':scope > h1');
  const topics=[...section.children].filter(el=>el.matches('.section.level2,section.level2'));
  const module=create('div','course-module');module.id='course-module-'+(i+1);
  module.append(header.cloneNode(true));header.remove();
  // Terms and introductory notes stay outside the topics, before the tabs.
  [...section.childNodes].filter(x=>!topics.includes(x)).forEach(x=>module.append(x));
  const tabbar=create('div','course-tabbar');tabbar.setAttribute('role','tablist');tabbar.setAttribute('aria-label','Temas del bloque '+(i+1));module.append(tabbar);
  const tabs=[];topics.forEach((topic,j)=>{
    topic.classList.add('course-topic');topic.id='course-topic-'+(i+1)+'-'+(j+1);
    topic.setAttribute('role','tabpanel');
    const h2=topic.querySelector(':scope > h2');
    const b=create('button','',h2?.textContent.trim()||'Tema '+(j+1));
    b.setAttribute('role','tab');b.id='course-tab-'+(i+1)+'-'+(j+1);b.setAttribute('aria-controls',topic.id);topic.setAttribute('aria-labelledby',b.id);
    tabbar.append(b);module.append(topic);tabs.push({b,topic});
  });
  if(!topics.length){const p=create('div','course-topic');module.append(p);[...section.childNodes].forEach(c=>p.append(c));tabs.push({b:create('button','', 'Tema'),topic:p});tabbar.append(tabs[0].b)}
  modulesWrap.append(module);section.remove();return {module,title:module.querySelector(':scope > h1')?.textContent||('Bloque '+(i+1)),tabs};
 });
 const code=(document.title.match(/S\d{2}/)||['SXX'])[0];
 const brand=create('div','course-brand',code+' / Modelos de lenguaje');const tagline=create('div','course-tagline','Del concepto a la demostración, el laboratorio y la investigación');
 const nav=create('nav','course-nav');nav.setAttribute('aria-label','Bloques');side.append(brand,tagline,nav);
 content.append(toolbar,intro,modulesWrap,create('div','course-footer','Maestría en Matemáticas Aplicadas · Material docente interactivo'));
 shell.append(side,content); main.insertBefore(shell,main.firstChild);
 // Any leftover top-level nodes are moved to the intro; avoid nested shells.
 [...main.childNodes].filter(n=>n!==shell).forEach(n=>{if(n.nodeType===1&&!n.matches('#TOC,.tocify'))intro.append(n)});
 let selectedBlock=0,selectedTopic=0;const routes=[];
 allBlocks.forEach((b,i)=>{const n=create('button','',b.title);nav.append(n);n.addEventListener('click',()=>show(i,0));b.navButton=n;b.tabs.forEach((t,j)=>{routes.push([i,j]);t.b.addEventListener('click',()=>show(i,j));t.b.addEventListener('keydown',event=>{const items=b.tabs;if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;event.stopPropagation();event.preventDefault();const k=event.key==='Home'?0:event.key==='End'?items.length-1:(j+(event.key==='ArrowRight'?1:-1)+items.length)%items.length;show(i,k);items[k].b.focus();})});});
 function show(i,j){if(!allBlocks[i])return;const b=allBlocks[i];j=Math.max(0,Math.min(j,b.tabs.length-1));selectedBlock=i;selectedTopic=j; if(typeof smallmenu!=='undefined')smallmenu.value=String(i);
  allBlocks.forEach((x,ix)=>{x.module.hidden=ix!==i;x.navButton.setAttribute('aria-current',String(ix===i));x.tabs.forEach((t,k)=>{const active=ix===i&&k===j;t.topic.hidden=!active;t.b.setAttribute('aria-selected',String(active));t.b.tabIndex=active?0:-1;});});
  eyebrow.textContent=b.title;counter.textContent=(i+1)+' / '+allBlocks.length+' · tema '+(j+1)+' / '+b.tabs.length;
  intro.hidden=(i!==0||j!==0)||document.body.classList.contains('course-projection'); const routeIdx=routes.findIndex(x=>x[0]===i&&x[1]===j);bar.style.width=(100*(routeIdx+1)/routes.length)+'%';
  prev.disabled=routeIdx===0;next.disabled=routeIdx===routes.length-1;
  const h=location.hash;const target='#tema-'+(i+1)+'-'+(j+1);if(h!==target)history.replaceState(null,'',target);
  const topic=b.tabs[j].topic;requestAnimationFrame(()=>{if(document.body.classList.contains('course-projection'))topic.scrollIntoView({block:'start',behavior:'instant'});else if(i===0&&j===0)window.scrollTo({top:0,behavior:'instant'});else topic.scrollIntoView({block:'start',behavior:'instant'});});
 }
 prev.addEventListener('click',()=>{let k=routes.findIndex(x=>x[0]===selectedBlock&&x[1]===selectedTopic);if(k>0)show(...routes[k-1]);});
 next.addEventListener('click',()=>{let k=routes.findIndex(x=>x[0]===selectedBlock&&x[1]===selectedTopic);if(k<routes.length-1)show(...routes[k+1]);});
 projection.addEventListener('click',()=>{const mode=document.body.classList.toggle('course-projection');intro.hidden=mode||(selectedBlock!==0||selectedTopic!==0);projection.textContent=mode?'Lectura':'Proyección';projection.setAttribute('aria-pressed',String(mode));show(selectedBlock,selectedTopic);});
 document.addEventListener('keydown',e=>{if(e.altKey||e.ctrlKey||e.metaKey||/INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName||''))return;if(document.activeElement?.getAttribute('role')==='tab')return;if(e.key==='ArrowRight')next.click();if(e.key==='ArrowLeft')prev.click();});
 const smallmenu=create('select','course-mobile-select');smallmenu.setAttribute('aria-label','Elegir bloque');allBlocks.forEach((b,i)=>{const op=create('option','',b.title);op.value=i;smallmenu.append(op)});smallmenu.addEventListener('change',()=>show(+smallmenu.value,0));side.insertBefore(smallmenu,nav);setupCourseResets();const parsed=location.hash.match(/^#tema-(\d+)-(\d+)$/);show(parsed?Math.min(allBlocks.length-1,+parsed[1]-1):0,parsed?Math.max(0,+parsed[2]-1):0);
 window.COURSE_TEMPLATE={version:'2.2',blocks:allBlocks.length,tabs:routes.length};
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
