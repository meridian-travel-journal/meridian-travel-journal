(()=>{
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const ls={get(k,d){try{const v=JSON.parse(localStorage.getItem(k));return v==null?d:v}catch(e){return d}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
const PAGES=[{"h": "index.html", "t": "Home", "d": "Worldwide travel stories and guides"}, {"h": "destinations.html", "t": "Destinations", "d": "Browse and filter guides by region"}, {"h": "lofoten.html", "t": "Lofoten, Norway", "d": "Fjords, red cabins and midnight light"}, {"h": "cinque-terre.html", "t": "Cinque Terre, Italy", "d": "Five cliffside villages on the Ligurian coast"}, {"h": "florence.html", "t": "36 hours in Florence", "d": "A weekend itinerary through Tuscany's capital"}, {"h": "travel-tips.html", "t": "Travel tips", "d": "Packing, documents and planning checklists"}, {"h": "culture.html", "t": "Culture and heritage", "d": "Landmarks and how to visit them well"}, {"h": "food.html", "t": "Food and local experiences", "d": "Dishes worth travelling for"}, {"h": "inspiration.html", "t": "Inspiration", "d": "Take the quiz, find your next place"}, {"h": "about.html", "t": "About", "d": "Who we are"}, {"h": "contact.html", "t": "Contact", "d": "Send us a note"}, {"h": "saved.html", "t": "Saved guides", "d": "Your bookmarks"}, {"h": "credits.html", "t": "Photo credits", "d": "Image sources and licences"}, {"h": "maldives.html", "t": "Maldives", "d": "Travel guide to Maldives"}, {"h": "kyoto.html", "t": "Kyoto, Japan", "d": "Travel guide to Kyoto, Japan"}, {"h": "marrakesh.html", "t": "Marrakesh, Morocco", "d": "Travel guide to Marrakesh, Morocco"}, {"h": "patagonia.html", "t": "Patagonia", "d": "Travel guide to Patagonia"}, {"h": "santorini.html", "t": "Santorini, Greece", "d": "Travel guide to Santorini, Greece"}, {"h": "bali.html", "t": "Bali, Indonesia", "d": "Travel guide to Bali, Indonesia"}, {"h": "cappadocia.html", "t": "Cappadocia, T\u00fcrkiye", "d": "Travel guide to Cappadocia, T\u00fcrkiye"}, {"h": "iceland.html", "t": "Iceland", "d": "Travel guide to Iceland"}];
const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
$('#yr')&&($('#yr').textContent=new Date().getFullYear());

/* menu, progress, back-to-top */
const mb=$('#mb'),nav=$('#nav');const closeMenu=()=>{nav.classList.remove('open');mb.setAttribute('aria-expanded','false')};
mb.addEventListener('click',()=>{const o=nav.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
document.addEventListener('click',e=>{if(nav.classList.contains('open')&&!nav.contains(e.target)&&!mb.contains(e.target))closeMenu()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('open')){closeMenu();mb.focus()}});
const bar=$('#prog'),tp=$('#top');addEventListener('scroll',()=>{const h=document.documentElement,m=h.scrollHeight-h.clientHeight;bar.style.width=(m>0?h.scrollTop/m*100:0)+'%';tp.hidden=h.scrollTop<700},{passive:true});
tp.addEventListener('click',()=>scrollTo({top:0,behavior:reduce?'auto':'smooth'}));

/* photos: lead image of a Wikipedia article (freely licensed) */
const loadWiki=async fig=>{const t=fig.dataset.wiki,img=$('img',fig);let u=ls.get('mer_original_'+t,null);
 if(!u){try{const r=await fetch('https://en.wikipedia.org/api/rest_v1/page/summary/'+encodeURIComponent(t));if(!r.ok)throw new Error('Image lookup failed: '+r.status);const j=await r.json();u=j.originalimage&&j.originalimage.source;if(u)ls.set('mer_original_'+t,u)}catch(e){console.error('Could not load image for '+t,e)}}
 if(!u)return;img.onload=()=>fig.classList.add('on');img.src=u};
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){io.unobserve(e.target);loadWiki(e.target)}}),{rootMargin:'300px'});
$$('.ph[data-wiki]').forEach(f=>io.observe(f));
$$('.ph img[src]').forEach(i=>{i.addEventListener('load',()=>i.parentNode.classList.add('on'));i.addEventListener('error',()=>i.parentNode.classList.remove('on'));if(i.complete&&!i.naturalWidth)i.parentNode.classList.remove('on')});

/* bookmarks */
const bms=()=>ls.get('mer_bm',[]),resolveBm=x=>{if(x.h.split(/[?#]/)[0]!=='planner.html')return x;const page=PAGES.find(p=>p.t===x.t);return page?{...x,h:page.h}:null};
const visibleBms=()=>bms().map(resolveBm).filter((x,i,a)=>x&&a.findIndex(y=>y&&y.h===x.h&&y.t===x.t)===i),cnt=()=>{$('#bc').textContent=visibleBms().length};cnt();
$$('.bm').forEach(b=>{const [h,t]=b.dataset.bm.split('|');const sync=()=>{const on=visibleBms().some(x=>x.h===h&&x.t===t);b.classList.toggle('on',on);b.textContent=on?'♥':'♡';b.setAttribute('aria-pressed',on)};sync();
 b.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();let a=bms();const matches=x=>{const item=resolveBm(x);return item&&item.h===h&&item.t===t};if(a.some(matches))a=a.filter(x=>!matches(x));else a.push({h,t});ls.set('mer_bm',a);sync();cnt()})});
const sv=$('#sv');if(sv){const a=visibleBms();sv.innerHTML=a.map(x=>`<li><a href="${x.h}"><b class="serif">${x.t.replace(/</g,'&lt;')}</b></a></li>`).join('');$('#sv-e').hidden=a.length>0}

/* ratings & reactions (stored locally) */
$$('.rate').forEach(r=>{const k='mer_r_'+r.dataset.id,bs=$$('button',r),v=$('.rv',r);const paint=n=>{bs.forEach((b,i)=>b.classList.toggle('on',i<n));v.textContent=n?`You rated ${n}/5`:'Tap to rate'};paint(ls.get(k,0));bs.forEach(b=>b.addEventListener('click',()=>{ls.set(k,+b.dataset.v);paint(+b.dataset.v)}))});
$$('.react').forEach(r=>{const k='mer_e_'+r.dataset.id,st=ls.get(k,{});$$('button',r).forEach((b,i)=>{const e=b.dataset.e,n=()=>(st[e]?1:0)+[12,8,5,9][i];const paint=()=>{b.classList.toggle('on',!!st[e]);$('b',b).textContent=n()};paint();b.addEventListener('click',()=>{st[e]=!st[e];ls.set(k,st);paint()})})});
$$('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(location.href);b.textContent='Copied'}catch(e){b.textContent='Copy failed'}setTimeout(()=>b.textContent='Copy link',1600)}));
$$('[data-native]').forEach(b=>{if(!navigator.share){b.hidden=true;return}b.addEventListener('click',()=>navigator.share({title:document.title,url:location.href}).catch(()=>{}))});

/* search */
const so=$('#so'),sq=$('#sq'),sr=$('#sr');const show=q=>{q=q.trim().toLowerCase();const m=q?PAGES.filter(p=>(p.t+' '+p.d).toLowerCase().includes(q)):PAGES.slice(0,6);sr.innerHTML=m.length?m.map(p=>`<li><a href="${p.h}">${p.t}<small>${p.d}</small></a></li>`).join(''):'<li class="empty">No match. Try “food” or “Italy”.</li>'};
let searchOpener;const openSearch=e=>{searchOpener=e.currentTarget;so.hidden=false;show('');sq.value='';sq.focus()},closeSearch=()=>{if(!so.hidden){so.hidden=true;searchOpener.focus()}};
[$('#sb'),$('#quick-search')].forEach(button=>button.addEventListener('click',openSearch));$('#sx').addEventListener('click',closeSearch);sq.addEventListener('input',()=>show(sq.value));
addEventListener('keydown',e=>{if(e.key==='Escape')closeSearch()});so.addEventListener('click',e=>{if(e.target===so)closeSearch()});

/* forms */
const okMail=v=>/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
const nl=$('.nl');nl.addEventListener('submit',e=>{e.preventDefault();const i=$('input',nl),m=$('.msg',nl);if(okMail(i.value)){m.textContent='Subscriptions are not available yet.';m.className='msg';}else{m.textContent='Enter a valid email, like you@example.com.';m.className='msg err'}});
const cf=$('#ctf');cf&&cf.addEventListener('submit',e=>{e.preventDefault();const m=$('.msg',cf),bad=!$('#cn').value.trim()?'Add your name.':!okMail($('#ce').value)?'Enter a valid email.':$('#cm').value.trim().length<10?'Write at least 10 characters.':'';m.textContent=bad||'Thanks. Your message is ready to send once a mail service is connected.';m.className='msg '+(bad?'err':'ok')});

/* destinations filter */
const dg=$('#dest-grid');if(dg){let f='all',q='';const cs=$$('#dest-filters .chips button');const run=()=>{let n=0;$$('.card',dg).forEach(c=>{const ok=(f==='all'||c.dataset.region===f)&&c.dataset.t.includes(q);c.hidden=!ok;ok&&n++});$('#dest-empty').hidden=n>0;dg.dispatchEvent(new Event('rail-update'))};
 cs.forEach(b=>{b.setAttribute('aria-pressed',b.dataset.f==='all');b.addEventListener('click',()=>{f=b.dataset.f;cs.forEach(x=>x.setAttribute('aria-pressed',x===b));run()})});$('#dq').addEventListener('input',e=>{q=e.target.value.toLowerCase();run()})}

/* home story moods */
const moods=$$('.home-filters button');moods.forEach(button=>button.addEventListener('click',()=>{moods.forEach(b=>b.setAttribute('aria-pressed',b===button));const rail=$('.home-stories');$$('.card',rail).forEach(card=>{card.hidden=button.dataset.mood!=='all'&&card.dataset.region!==button.dataset.mood});rail.dispatchEvent(new Event('rail-update'))}));

/* Scroll-snap story rails work with native touch scrolling and keyboard navigation. */
$$('[data-carousel]').forEach(carousel=>{const rail=$('.story-rail',carousel),prev=$('[data-prev]',carousel),next=$('[data-next]',carousel),count=$('[data-count]',carousel),progress=$('[data-progress]',carousel);let index=0,drag=null,suppress=false;
 const slides=()=>[...rail.children].filter(el=>!el.hidden);
 const paint=()=>{const items=slides();index=Math.max(0,Math.min(index,items.length-1));count.textContent=items.length?`${String(index+1).padStart(2,'0')} / ${String(items.length).padStart(2,'0')}`:'00 / 00';progress.style.width=items.length?`${(index+1)/items.length*100}%`:'0%';prev.disabled=index===0;next.disabled=index>=items.length-1;items.forEach((item,i)=>item.classList.toggle('is-active',i===index))};
 const go=i=>{const items=slides();if(!items.length){paint();return}index=Math.max(0,Math.min(i,items.length-1));rail.scrollTo({left:rail.scrollLeft+items[index].getBoundingClientRect().left-rail.getBoundingClientRect().left,behavior:reduce?'auto':'smooth'});paint()};
 prev.addEventListener('click',()=>go(index-1));next.addEventListener('click',()=>go(index+1));rail.addEventListener('keydown',e=>{if(e.target!==rail)return;if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();go(index+(e.key==='ArrowRight'?1:-1))}});
 rail.addEventListener('scroll',()=>{if(drag)return;const items=slides();if(!items.length)return;const left=rail.getBoundingClientRect().left;let nearest=0;items.forEach((item,i)=>{if(Math.abs(item.getBoundingClientRect().left-left)<Math.abs(items[nearest].getBoundingClientRect().left-left))nearest=i});index=nearest;paint()},{passive:true});
 rail.addEventListener('rail-update',()=>{index=0;rail.scrollLeft=0;rail.classList.remove('filtering');void rail.offsetWidth;rail.classList.add('filtering');paint()});
 rail.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse'||e.button!==0||e.target.closest('button'))return;drag={x:e.clientX,left:rail.scrollLeft,moved:false}});
 rail.addEventListener('pointermove',e=>{if(!drag)return;if(Math.abs(e.clientX-drag.x)>6){drag.moved=true;rail.style.scrollSnapType='none';rail.setPointerCapture(e.pointerId);rail.scrollLeft=drag.left-(e.clientX-drag.x)}});
 const end=()=>{if(!drag)return;const moved=drag.moved;drag=null;rail.style.scrollSnapType='';if(moved){suppress=true;const items=slides(),left=rail.getBoundingClientRect().left;let nearest=0;items.forEach((item,i)=>{if(Math.abs(item.getBoundingClientRect().left-left)<Math.abs(items[nearest].getBoundingClientRect().left-left))nearest=i});go(nearest);setTimeout(()=>suppress=false,0)}};
 rail.addEventListener('pointerup',end);rail.addEventListener('pointercancel',end);rail.addEventListener('click',e=>{if(suppress){e.preventDefault();e.stopPropagation()}},true);paint()});
$$('[data-food-filter]').forEach(button=>button.addEventListener('click',()=>{$$('[data-food-filter]').forEach(b=>b.setAttribute('aria-pressed',b===button));const rail=$('.food-rail');$$('.mi',rail).forEach(item=>{item.hidden=button.dataset.foodFilter!=='all'&&item.dataset.food!==button.dataset.foodFilter});rail.dispatchEvent(new Event('rail-update'))}));
if(!reduce&&'IntersectionObserver'in window){const reveal=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('revealed');reveal.unobserve(entry.target)}}),{threshold:.12});$$('.culture-chapter,.editorial-band,.next-story,.tips-index,.inspire-work').forEach(el=>reveal.observe(el))}

/* toc spy */
const tc=$$('.toc a');if(tc.length){const so2=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)tc.forEach(a=>a.classList.toggle('on',a.hash==='#'+e.target.id))}),{rootMargin:'-30% 0px -60% 0px'});tc.forEach(a=>{const t=$(a.hash);t&&so2.observe(t)})}

/* timeline */
const tl=$('#fl-tl');if(tl){const k='mer_fl',d=ls.get(k,[]),its=$$('.tli',tl);const upd=()=>{const n=its.filter(x=>x.classList.contains('done')).length;$('#fl-bar').style.width=n/its.length*100+'%';$('#fl-count').textContent=`${n} of ${its.length} stops done`};
 its.forEach((li,i)=>{d.includes(i)&&li.classList.add('done');$('button',li).addEventListener('click',()=>{li.classList.toggle('done');ls.set(k,its.map((x,j)=>x.classList.contains('done')?j:-1).filter(j=>j>-1));upd()})});upd()}

/* tabs + checklist */
const tt=$('#tp-tabs');if(tt){$$('[role=tab]',tt).forEach(b=>b.addEventListener('click',()=>{$$('[role=tab]',tt).forEach(x=>x.setAttribute('aria-selected',x===b));$$('.pane',tt).forEach(p=>p.hidden=p.dataset.pane!==b.dataset.tab)}));
 const cks=$$('[data-ck]'),k='mer_pack',d=ls.get(k,[]);const upd=()=>{const n=cks.filter(c=>c.checked).length;$('#pk-bar').style.width=n/cks.length*100+'%';$('#pk-count').textContent=`${n} of ${cks.length} packed`;ls.set(k,cks.map((c,i)=>c.checked?i:-1).filter(i=>i>-1))};
 cks.forEach((c,i)=>{c.checked=d.includes(i);c.addEventListener('change',upd)});$('#pk-reset').addEventListener('click',()=>{cks.forEach(c=>c.checked=false);upd()});upd()}

/* lightbox */
const lb=$('#lb');if(lb){let trigger;const close=()=>{lb.hidden=true;if(trigger)trigger.focus()};$$('.mi').forEach(m=>{m.tabIndex=0;const open=()=>{trigger=m;$('#lbi').innerHTML=m.querySelector('.ph').outerHTML;$('#lbc').textContent=m.dataset.cap;const link=$('#lb-link');link.hidden=!m.dataset.link;if(!link.hidden){link.href=m.dataset.link;link.textContent=m.dataset.linkTitle+' ↗'}lb.hidden=false;$('#lbx').focus()};m.addEventListener('click',open);m.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open()}})});$('#lbx').addEventListener('click',close);lb.addEventListener('click',e=>{if(e.target===lb)close()});addEventListener('keydown',e=>{if(e.key==='Escape'&&!lb.hidden)close()})}

/* quiz + poll */
const qz=$('#qz');if(qz){const Q=[['What pace suits you?',['Slow and scenic','Fast and full','Somewhere in between']],['What do you crave?',['Mountains and sea','Old streets and art','Food and markets']],['When do you go?',['Summer','Spring or autumn','Winter']]];
 const R={'0':['Lofoten, Norway','lofoten.html'],'1':['Florence, Italy','florence.html'],'2':['Cinque Terre, Italy','cinque-terre.html']};let i=0,sc=[0,0,0];
 const draw=()=>{if(i>=Q.length){const w=sc.indexOf(Math.max(...sc)),r=R[w];qz.innerHTML=`<h2 class="serif">Try ${r[0]}</h2><p>A good match for your answers.</p><a class="btn" href="${r[1]}">Read the guide</a> <button class="ghost" id="qr">Retake</button>`;$('#qr').onclick=()=>{i=0;sc=[0,0,0];draw()};return}
  qz.innerHTML=`<p class="cap">Question ${i+1} of ${Q.length}</p><h2 class="serif">${Q[i][0]}</h2>`+Q[i][1].map((t,j)=>`<button data-j="${j}">${t}</button>`).join('');$$('button',qz).forEach(b=>b.onclick=()=>{sc[+b.dataset.j]++;i++;draw()})};draw();
 const P=['Weekend','One week','Two weeks','A month or more'],base=[14,31,22,9],pk='mer_poll';let v=ls.get(pk,-1);const pl=$('#poll');const dp=()=>{const tot=base.reduce((a,b)=>a+b,0)+(v>-1?1:0);pl.innerHTML=P.map((t,j)=>{const n=base[j]+(v===j?1:0),p=Math.round(n/tot*100);return v>-1?`<div>${t}<div class="pbar"><span style="width:${p}%">${p}%</span></div></div>`:`<button class="opt" data-j="${j}">${t}</button>`}).join('');$$('button.opt',pl).forEach(b=>b.onclick=()=>{v=+b.dataset.j;ls.set(pk,v);dp()})};dp()}
})();
