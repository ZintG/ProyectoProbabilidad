/* Glosario común: búsqueda insensible a tildes y etiquetas accesibles. */
(()=>{'use strict';
const norm=s=>String(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('es').trim();
function setup(){document.querySelectorAll('.glossary-widget').forEach((block,i)=>{
 const input=block.querySelector('.glossary-search'),rows=[...block.querySelectorAll('.glossary-entry')],empty=block.querySelector('.glossary-noresults');if(!input)return;
 input.setAttribute('aria-label','Buscar términos del glosario '+(i+1));if(!input.id)input.id='glosario-comun-'+(i+1);
 const match=()=>{const query=norm(input.value);let count=0;rows.forEach(row=>{const valid=!query||norm((row.dataset.term||'')+' '+row.textContent).includes(query);row.hidden=!valid;count+=valid?1:0;});if(empty)empty.hidden=count>0;};
 input.addEventListener('input',match);match();
});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',setup);else setup();
})();
