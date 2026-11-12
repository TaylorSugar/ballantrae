(function(){
document.documentElement.classList.add('js');
var hd=document.querySelector('header.site'),b=document.querySelector('.menu'),n=document.querySelector('nav.main');
function sc(){if(hd)hd.classList.toggle('solid',window.scrollY>40)}sc();window.addEventListener('scroll',sc,{passive:true});
function setMenu(o){n.classList.toggle('open',o);b.setAttribute('aria-expanded',o);document.body.style.overflow=o?'hidden':''}
if(b){b.addEventListener('click',function(){setMenu(!n.classList.contains('open'))});n.addEventListener('click',function(e){if(e.target.closest('a'))setMenu(false)});document.addEventListener('keydown',function(e){if(e.key==='Escape')setMenu(false)});window.addEventListener('resize',function(){if(window.innerWidth>1180)setMenu(false)})}
/* reveal on scroll (CSS only animates when motion is allowed) */
var rv=[].slice.call(document.querySelectorAll('.rv'));
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});rv.forEach(function(x){io.observe(x)})}else rv.forEach(function(x){x.classList.add('in')});
/* ---------- charts ---------- */
var root=document.getElementById('charts');
if(root&&window.BD){
 var BD=window.BD,M=BD.models,Y=BD.years,PAL=BD.pal,metric='avg',view='year',yr=Y[Y.length-1],on={};M.forEach(function(m){on[m]=true});
 var cv=document.getElementById('cv'),ro=document.getElementById('readout'),leg=document.getElementById('legend'),yrow=document.getElementById('yrow'),ttl=document.getElementById('ctitle'),cap=document.getElementById('ccap');
 var NS='http://www.w3.org/2000/svg';
 function fm(v){return '$'+(v/1e6).toFixed(2)+'M'}function fu(v){return '$'+Math.round(v).toLocaleString('en-CA')}
 function el(t,a,p){var e=document.createElementNS(NS,t);for(var k in a)if(a[k]!==null)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
 function nice(lo,hi){var st=hi-lo>1.2e6?.4e6:.2e6,a=Math.floor(lo/st)*st,t=[];for(var v=a;v<hi+st*.99;v+=st)t.push(v);return t}
 function drawLegend(){leg.innerHTML='';if(view==='model'){leg.style.display='none';yrow.style.display='flex';return}leg.style.display='flex';yrow.style.display='none';
  M.forEach(function(m,i){var bt=document.createElement('button');bt.className='leg';bt.style.setProperty('--c',PAL[i]);bt.setAttribute('aria-pressed',on[m]);bt.innerHTML='<i></i>'+m;bt.onclick=function(){on[m]=!on[m];if(!M.some(function(x){return on[x]}))on[m]=true;draw()};leg.appendChild(bt)})}
 function draw(){
  var W=Math.max(300,Math.round(cv.clientWidth)),H=W<520?330:410,pl=W<520?46:60,pr=W<520?14:24,pt=24,pb=(W<520&&view==='model')?74:(W<520?40:46),s=el('svg',{viewBox:'0 0 '+W+' '+H,role:'img','aria-label':ttl.textContent});
  var data=BD[metric],nm=metric==='avg'?'Average':'Highest';
  ttl.textContent=nm+' sold price by model, '+(view==='year'?Y[0]+'–'+Y[Y.length-1]:yr);
  cap.textContent=view==='year'?'Each line is a model. Tap or hover a year to compare. Use the model buttons to show or hide lines.':'Each bar is a model, for the year you pick. Tap a bar for its exact values.';
  var vals=[];M.forEach(function(m){if(view==='year'&&!on[m])return;(view==='year'?data[m]:[data[m][Y.indexOf(yr)]]).forEach(function(v){vals.push(v)})});
  var lo=Math.max(0,Math.min.apply(null,vals)*.9),hi=Math.max.apply(null,vals)*1.08;if(view==='model')lo=0;var tk=nice(lo,hi);lo=tk[0];hi=tk[tk.length-1];
  var X0=pl,X1=W-pr,Y0=H-pb,Y1=pt,y=function(v){return Y0-(Y0-Y1)*(v-lo)/(hi-lo)};
  tk.forEach(function(v){el('line',{x1:X0,x2:X1,y1:y(v),y2:y(v),stroke:'#dbe8dc','stroke-width':1},s);var t=el('text',{x:X0-8,y:y(v)+4,'text-anchor':'end','font-size':11,fill:'#566a5e'},s);t.textContent=fm(v).replace('.00M','M')});
  if(view==='year'){
   var xs=function(i){return X0+(X1-X0)*(i+.0)/(Y.length-1)};
   Y.forEach(function(yy,i){var t=el('text',{x:xs(i),y:H-pb+22,'text-anchor':'middle','font-size':W<520?10:12,fill:'#14261c'},s);t.textContent=yy});
   var g=el('line',{x1:0,x2:0,y1:Y1,y2:Y0,stroke:'#16523a','stroke-width':1.5,'stroke-dasharray':'4 4',opacity:0},s),dots=[];
   M.forEach(function(m,k){if(!on[m])return;var pts=data[m].map(function(v,i){return xs(i)+','+y(v)}).join(' ');el('polyline',{points:pts,fill:'none',stroke:PAL[k],'stroke-width':3,'stroke-linejoin':'round','stroke-linecap':'round'},s);data[m].forEach(function(v,i){var c=el('circle',{cx:xs(i),cy:y(v),r:W<520?3.5:4.5,fill:'#fff',stroke:PAL[k],'stroke-width':2.5},s);c.dataset.m=m;c.dataset.i=i;dots.push(c)})});
   function show(i){g.setAttribute('x1',xs(i));g.setAttribute('x2',xs(i));g.setAttribute('opacity',1);
    var rows=M.map(function(m,k){return {m:m,k:k,v:data[m][i]}}).filter(function(r){return on[r.m]}).sort(function(a,b){return b.v-a.v});
    ro.innerHTML='<b>'+Y[i]+'</b> · '+rows.map(function(r){return '<span style="white-space:nowrap"><i style="display:inline-block;width:10px;height:10px;border-radius:50%;background:'+PAL[r.k]+';margin:0 4px 0 8px"></i>'+r.m+' '+fu(r.v)+'</span>'}).join(' ');
    dots.forEach(function(d){d.setAttribute('r',+d.dataset.i===i?(W<520?5.5:6.5):(W<520?3.5:4.5))})}
   function mv(e){var r=s.getBoundingClientRect(),px=(e.clientX-r.left)*W/r.width,i=Math.round((px-X0)/(X1-X0)*(Y.length-1));i=Math.max(0,Math.min(Y.length-1,i));show(i)}
   var ov=el('rect',{x:X0-10,y:Y1,width:X1-X0+20,height:Y0-Y1,fill:'transparent'},s);ov.addEventListener('pointermove',mv);ov.addEventListener('pointerdown',mv);show(Y.length-1);
  }else{
   var iy=Y.indexOf(yr),bw=(X1-X0)/M.length;
   M.forEach(function(m,k){var v=data[m][iy],x=X0+k*bw+bw*.14,w=bw*.72,r=el('rect',{x:x,y:y(v),width:w,height:Y0-y(v),fill:PAL[k],rx:5,tabindex:0,style:'cursor:pointer'},s);
    var t=el('text',{x:x+w/2,y:y(v)-6,'text-anchor':'middle','font-size':W<520?10:12,'font-weight':700,fill:'#14261c'},s);t.textContent=fm(v).replace('M','M');
    var nar=W<520,lb=el('text',{x:nar?x+w/2+3:x+w/2,y:Y0+16,'text-anchor':nar?'end':'middle','font-size':nar?11:12,fill:'#14261c',transform:nar?'rotate(-38 '+(x+w/2+3)+' '+(Y0+16)+')':null},s);if(nar){lb.textContent=m}else m.split(' ').forEach(function(p,j){var ts=el('tspan',{x:x+w/2,dy:j?12:0},lb);ts.textContent=p});
    function pick(){ro.innerHTML='<b>'+m+' · '+yr+'</b> · Average '+fu(BD.avg[m][iy])+' · Highest '+fu(BD.hi[m][iy])+(BD.n[m][iy]!=null?' · '+BD.n[m][iy]+' sale'+(BD.n[m][iy]===1?'':'s'):'');s.querySelectorAll('rect[tabindex]').forEach(function(q){q.setAttribute('opacity',q===r?1:.55)})}
    r.addEventListener('click',pick);r.addEventListener('focus',pick);r.addEventListener('pointerenter',pick)});
   ro.innerHTML='Tap a bar for exact average and highest prices.';
  }
  el('line',{x1:X0,x2:X1,y1:Y0,y2:Y0,stroke:'#9bb5a2'},s);cv.innerHTML='';cv.appendChild(s)}
 function seg(id,fn){var bs=document.querySelectorAll('#'+id+' button');[].forEach.call(bs,function(x){x.addEventListener('click',function(){[].forEach.call(bs,function(o){o.setAttribute('aria-pressed',o===x)});fn(x.dataset.v);drawLegend();draw()})})}
 seg('seg-metric',function(v){metric=v});seg('seg-view',function(v){view=v});
 Y.slice().reverse().forEach(function(y0){var c=document.createElement('button');c.className='chip';c.textContent=y0;c.dataset.y=y0;c.setAttribute('aria-pressed',y0===yr);c.onclick=function(){yr=y0;[].forEach.call(yrow.children,function(o){o.setAttribute('aria-pressed',+o.dataset.y===y0)});draw()};yrow.appendChild(c)});
 drawLegend();draw();var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(draw,120)});
}
/* ---------- sold filters ---------- */
var app=document.getElementById('sold-app');if(!app)return;
var fy='all',fm_='all',rows=[].slice.call(app.querySelectorAll('tr[data-y]')),blocks=[].slice.call(app.querySelectorAll('.yearblock')),cnt=document.getElementById('sold-count');
function apply(){var shown=0;
 rows.forEach(function(r){var ok=(fy==='all'||r.dataset.y===fy)&&(fm_==='all'||r.dataset.m===fm_);r.classList.toggle('hide',!ok);if(ok)shown++});
 blocks.forEach(function(bl){var vis=bl.querySelectorAll('tr[data-y]:not(.hide)').length,h3=bl.querySelector('h3'),ys=bl.querySelector('.yearsum');if(!h3.dataset.o)h3.dataset.o=h3.textContent;bl.classList.toggle('hide',!vis);
  if(fm_==='all'){h3.textContent=h3.dataset.o;if(ys)ys.style.display=''}else{var mn=(app.querySelector('[data-model="'+fm_+'"]')||{textContent:fm_}).textContent;h3.textContent=h3.dataset.o.split(':')[0]+': '+vis+' '+mn+' sale'+(vis===1?'':'s');if(ys)ys.style.display='none'}});
 app.querySelectorAll('tr[data-mm]').forEach(function(r){r.classList.toggle('sel',fm_!=='all'&&r.dataset.mm===fm_)});
 if(cnt)cnt.textContent=shown+' sale'+(shown===1?'':'s')+' shown'+(fy!=='all'?' · '+fy:'')+(fm_!=='all'?' · '+(app.querySelector('[data-model="'+fm_+'"]')||{textContent:fm_}).textContent:'');
 try{history.replaceState(null,'','#'+fy+'/'+fm_)}catch(e){}}
function pr(sel,val,a){[].forEach.call(app.querySelectorAll(sel),function(c){c.setAttribute('aria-pressed',c.dataset[a]===val)})}
app.addEventListener('click',function(e){var t=e.target.closest('[data-year],[data-model],[data-pick]');if(!t)return;
 if(t.dataset.pick){e.preventDefault();fm_=t.dataset.pick;pr('[data-model]',fm_,'model');apply();document.getElementById('sold-list').scrollIntoView();return}
 if(t.dataset.year){fy=t.dataset.year;pr('[data-year]',fy,'year')}
 if(t.dataset.model){fm_=t.dataset.model;pr('[data-model]',fm_,'model')}
 apply()});
var h=(location.hash||'').replace('#','').split('/');if(h.length===2){if(h[0]==='all'||app.querySelector('[data-year="'+h[0]+'"]')){fy=h[0];pr('[data-year]',fy,'year')}if(h[1]==='all'||app.querySelector('[data-model="'+h[1]+'"]')){fm_=h[1];pr('[data-model]',fm_,'model')}}
apply();
})();
