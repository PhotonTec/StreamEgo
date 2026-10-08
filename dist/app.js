const methodInfo={
 teacher:{alt:'Streaming dual-branch priors and the bidirectional teacher with a region-aware training curriculum.',caption:'The teacher uses streaming dynamic ego and body-guided human pose priors as pixel-aligned conditions. A region-aware curriculum balances shared appearance, unseen context, and hand–object interactions.'},
 student:{alt:'Chunk-wise autoregressive student: prior extraction, cached memory, region-aware history corruption, first-chunk curriculum, and a distilled diffusion transformer.',caption:'The student generates the current chunk from streaming priors and cached egocentric history using three denoising steps. Region-aware history corruption and a first-chunk curriculum stabilize continuous rollouts.'}
};
function selectMethod(button){
 const key=button.dataset.method;
 document.querySelectorAll('[data-method]').forEach(b=>{const active=b===button;b.classList.toggle('is-active',active);b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1;});
 const image=document.querySelector('#method-image');image.src=`assets/${key}.svg?v=rgba-v1`;image.alt=methodInfo[key].alt;
 document.querySelector('#method-image-link').href=`assets/${key}.pdf`;
 document.querySelector('#method-caption').textContent=methodInfo[key].caption;
 document.querySelector('#method-panel').setAttribute('aria-labelledby',button.id);
}
document.querySelectorAll('[data-method]').forEach(button=>{
 button.addEventListener('click',()=>selectMethod(button));
 button.addEventListener('keydown',event=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;event.preventDefault();const buttons=[...document.querySelectorAll('[data-method]')];const next=event.key==='Home'?buttons[0]:event.key==='End'?buttons[1]:buttons.find(b=>b!==button);selectMethod(next);next.focus();});
});
const visualizations={cooking:'Cooking · Ego-Exo4D · 30 seconds',piano:'Playing piano · Ego-Exo4D · 30 seconds',objects:'Object handling · H2O · 10 seconds'};
const comparisons={h2o:'Book interaction · H2O',bicycle:'Bicycle repair · Ego-Exo4D',assembly:'Toy assembly · Assembly101',cpr:'CPR practice · Ego-Exo4D',h2o2:'Device interaction · H2O',reading:'Reading · Ego-Exo4D',cooking:'Cooking · Ego-Exo4D'};
const videos=[document.querySelector('#visualization-video'),document.querySelector('#comparison-video')];
const visibility=new Map(),resumeOnReturn=new WeakSet();
const reduceMotion=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function installGallery(kind,labels){
 const video=document.querySelector(`#${kind}-video`);
 document.querySelectorAll(`[data-${kind}]`).forEach(button=>button.addEventListener('click',()=>{
  const key=button.dataset[kind];videos.forEach(v=>{v.pause();resumeOnReturn.delete(v);});
  document.querySelectorAll(`[data-${kind}]`).forEach(b=>{const active=b===button;b.classList.toggle('thumbnail-selected',active);b.setAttribute('aria-pressed',String(active));});
  video.poster=`assets/${kind}-${key}.jpg`;video.src=`assets/${kind}-${key}.mp4`;video.setAttribute('aria-label',labels[key]);document.querySelector(`#${kind}-caption`).textContent=labels[key];video.load();video.play().catch(()=>{});
 }));
}
installGallery('visualization',visualizations);installGallery('comparison',comparisons);
const started=new WeakSet();
const observer=new IntersectionObserver(entries=>{
 for(const entry of entries){const video=entry.target;visibility.set(video,entry.isIntersecting);if(!entry.isIntersecting){if(!video.paused){resumeOnReturn.add(video);video.pause();}}else if(!reduceMotion&&(!started.has(video)||resumeOnReturn.has(video))){started.add(video);resumeOnReturn.delete(video);video.play().catch(()=>{});}}
},{threshold:0.25});
videos.forEach(video=>observer.observe(video));
document.addEventListener('visibilitychange',()=>{
 if(document.hidden){videos.forEach(video=>{if(!video.paused){resumeOnReturn.add(video);video.pause();}});}else if(!reduceMotion){videos.forEach(video=>{if(visibility.get(video)&&resumeOnReturn.has(video)){resumeOnReturn.delete(video);video.play().catch(()=>{});}});}
});
