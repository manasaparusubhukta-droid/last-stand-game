import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="LAST STAND | Zombie Survival", page_icon="🧟", layout="wide")
st.markdown("""
<style>
.stApp{background:#0b1115;color:#e8f0f2}.block-container{padding-top:1rem;max-width:1200px}
h1{letter-spacing:2px}.hint{color:#b9c9ce}
</style>
""", unsafe_allow_html=True)
st.title("🧟 LAST STAND")
st.markdown('<p class="hint">Top-down zombie survival • Survive the waves • Collect supplies</p>', unsafe_allow_html=True)
with st.expander("🎮 Controls", expanded=False):
    st.markdown("**Move:** WASD / arrow keys · **Aim:** mouse · **Shoot:** left click / Space · **Collect:** E near a crate · **Pause:** Esc · **Restart:** Restart button. Click the game area first to focus keyboard controls.")

GAME = r"""
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}body{margin:0;background:#081014;color:#eaf2f4;font-family:Arial;overflow:hidden}
#wrap{padding:5px}#hud{display:flex;gap:7px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:5px 2px 9px}
.stats{display:flex;gap:7px;flex-wrap:wrap}.pill{background:#142127;border:1px solid #2c424a;border-radius:8px;padding:7px 10px;font-size:13px}.pill b{color:#65e6d0}
button{background:#183139;color:#eef8fa;border:1px solid #3c626b;padding:8px 12px;border-radius:8px;font-weight:bold;cursor:pointer}
#stage{position:relative}canvas{display:block;width:100%;height:auto;aspect-ratio:16/9;background:#101c1c;border:1px solid #30474a;border-radius:10px;outline:none;touch-action:none}
#overlay{display:none;position:absolute;inset:0;border-radius:10px;background:#03090ccc;align-items:center;justify-content:center;text-align:center;padding:20px}
#overlay.show{display:flex}#overlay h2{font-size:clamp(25px,4vw,42px);letter-spacing:2px;margin:0 0 8px}#overlay p{color:#bfd0d5;line-height:1.5}
#msg{color:#8ce7d8;font-size:13px;min-height:22px;padding:7px 3px}
</style></head><body><div id="wrap">
<div id="hud"><div class="stats">
<div class="pill">❤️ Health: <b id="health">100</b></div><div class="pill">🔫 Ammo: <b id="ammo">60</b></div>
<div class="pill">☠️ Score: <b id="score">0</b></div><div class="pill">🌊 Wave: <b id="wave">1</b></div></div>
<div><button id="pause">Pause</button> <button id="restart">Restart</button></div></div>
<div id="stage"><canvas id="game" width="960" height="540" tabindex="0"></canvas>
<div id="overlay" class="show"><div><h2 id="ot">LAST STAND</h2><p id="op">Survive the zombie waves.<br>Click Start, then click the game area to play.</p><button id="start">Start Game</button></div></div></div>
<div id="msg">Tip: Press E near a supply crate to collect supplies.</div></div>
<script>
(()=> {
const c=document.getElementById('game'),x=c.getContext('2d'),W=960,H=540,$=id=>document.getElementById(id);
const obstacles=[{x:115,y:95,w:135,h:72},{x:710,y:85,w:130,h:80},{x:340,y:65,w:80,h:55},{x:500,y:390,w:155,h:65},{x:100,y:365,w:115,h:78},{x:750,y:340,w:95,h:95},{x:395,y:225,w:65,h:80}];
let keys=new Set(),player,zombies=[],bullets=[],crates=[],particles=[],running=false,paused=false,over=false;
let score=0,wave=1,ammo=60,health=100,last=0,spawn=0,supply=4,shootWait=0,msgTime=0;
let mouse={x:580,y:270,down:false};
const rnd=(a,b)=>a+Math.random()*(b-a),d=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
function say(s){$('msg').textContent=s;msgTime=3}
function hud(){$('health').textContent=Math.max(0,Math.ceil(health));$('ammo').textContent=ammo;$('score').textContent=score;$('wave').textContent=wave}
function blocked(px,py,r){return px<r+7||px>W-r-7||py<r+7||py>H-r-7||obstacles.some(o=>px+r>o.x&&px-r<o.x+o.w&&py+r>o.y&&py-r<o.y+o.h)}
function spawnZombie(){let px,py,tries=0;do{let s=Math.floor(Math.random()*4);px=s===1?W-8:s===3?8:rnd(10,W-10);py=s===0?8:s===2?H-8:rnd(10,H-10);tries++}while((d({x:px,y:py},player)<170||blocked(px,py,15))&&tries<30);zombies.push({x:px,y:py,r:rnd(12,16),speed:rnd(55,73)+wave*2.5,hp:wave>=3?2:1,attack:0})}
function spawnCrate(){for(let i=0;i<60;i++){let q={x:rnd(30,W-30),y:rnd(30,H-30),r:13,bob:rnd(0,6)};if(!blocked(q.x,q.y,17)&&d(q,player)>100){crates.push(q);return}}}
function reset(){player={x:W/2,y:H/2,r:13,speed:205,inv:0};zombies=[];bullets=[];crates=[];particles=[];score=0;wave=1;ammo=60;health=100;spawn=0;supply=4;shootWait=0;running=true;paused=false;over=false;$('overlay').classList.remove('show');$('pause').textContent='Pause';$('start').textContent='Start Game';say('Survive as long as you can.');for(let i=0;i<4;i++)spawnZombie();hud()}
function shoot(){if(!running||paused||over||shootWait>0)return;if(ammo<=0){say('Out of ammo! Find a supply crate.');shootWait=.3;return}let dx=mouse.x-player.x,dy=mouse.y-player.y,l=Math.hypot(dx,dy)||1;bullets.push({x:player.x+dx/l*18,y:player.y+dy/l*18,vx:dx/l*560,vy:dy/l*560,life:1.2});ammo--;shootWait=.17;hud()}
function collect(){if(!running||paused||over)return;let i=crates.findIndex(q=>d(q,player)<q.r+player.r+22);if(i<0){say('Move closer to a supply crate.');return}crates.splice(i,1);health=Math.min(100,health+25);ammo=Math.min(120,ammo+24);say('Supplies collected: +25 health, +24 ammo.');hud()}
function end(){over=true;running=false;$('ot').textContent='GAME OVER';$('op').innerHTML='Final score: <b>'+score+'</b><br>You survived until wave '+wave+'.';$('start').textContent='Play Again';$('overlay').classList.add('show')}
function pause(){if(!running||over)return;paused=!paused;$('pause').textContent=paused?'Resume':'Pause';if(paused){$('ot').textContent='PAUSED';$('op').textContent='Resume when ready.';$('start').textContent='Resume Game';$('overlay').classList.add('show')}else $('overlay').classList.remove('show')}
function update(dt){if(!running||paused||over)return;shootWait=Math.max(0,shootWait-dt);player.inv=Math.max(0,player.inv-dt);
let mx=(keys.has('KeyD')||keys.has('ArrowRight')?1:0)-(keys.has('KeyA')||keys.has('ArrowLeft')?1:0),my=(keys.has('KeyS')||keys.has('ArrowDown')?1:0)-(keys.has('KeyW')||keys.has('ArrowUp')?1:0),m=Math.hypot(mx,my)||1;mx/=m;my/=m;
let nx=player.x+mx*player.speed*dt,ny=player.y+my*player.speed*dt;if(!blocked(nx,player.y,player.r))player.x=nx;if(!blocked(player.x,ny,player.r))player.y=ny;
if(mouse.down||keys.has('Space'))shoot();spawn-=dt;if(spawn<=0&&zombies.length<7+wave*2){spawnZombie();spawn=Math.max(.4,1.5-wave*.06)}supply-=dt;if(supply<=0&&crates.length<3){spawnCrate();supply=9}
for(let z of zombies){z.attack=Math.max(0,z.attack-dt);let dx=player.x-z.x,dy=player.y-z.y,l=Math.hypot(dx,dy)||1,vx=dx/l*z.speed*dt,vy=dy/l*z.speed*dt;if(!blocked(z.x+vx,z.y,z.r))z.x+=vx;else if(!blocked(z.x-dy/l*z.speed*dt,z.y,z.r))z.x-=dy/l*z.speed*dt;if(!blocked(z.x,z.y+vy,z.r))z.y+=vy;else if(!blocked(z.x,z.y+dx/l*z.speed*dt,z.r))z.y+=dx/l*z.speed*dt;
if(d(z,player)<z.r+player.r+2&&z.attack<=0&&player.inv<=0){health-=12;player.inv=.7;z.attack=.8;say('You were hit! Keep moving.');if(health<=0){health=0;hud();end();return}}}
for(let b of bullets){b.x+=b.vx*dt;b.y+=b.vy*dt;b.life-=dt;if(blocked(b.x,b.y,2))b.life=-1;if(b.life>0)for(let z of zombies){if(!z.dead&&d(b,z)<z.r+4){z.hp--;b.life=-1;if(z.hp<=0){z.dead=true;score+=10;if(score>0&&score%100===0){wave++;say('Wave '+wave+' incoming!')} }break}}}
bullets=bullets.filter(b=>b.life>0);zombies=zombies.filter(z=>!z.dead);for(let p of particles){p.x+=p.vx*dt;p.y+=p.vy*dt;p.life-=dt}particles=particles.filter(p=>p.life>0);if(msgTime>0){msgTime-=dt;if(msgTime<=0)$('msg').textContent='Tip: Press E near a supply crate to collect supplies.'}hud()}
function draw(){x.clearRect(0,0,W,H);x.fillStyle='#142321';x.fillRect(0,0,W,H);x.strokeStyle='rgba(99,143,119,.1)';for(let a=0;a<W;a+=32){x.beginPath();x.moveTo(a,0);x.lineTo(a,H);x.stroke()}for(let a=0;a<H;a+=32){x.beginPath();x.moveTo(0,a);x.lineTo(W,a);x.stroke()}
for(let o of obstacles){x.fillStyle='#080f12';x.fillRect(o.x+5,o.y+7,o.w,o.h);x.fillStyle='#344348';x.fillRect(o.x,o.y,o.w,o.h);x.fillStyle='#536166';x.fillRect(o.x+5,o.y+5,o.w-10,7);x.strokeStyle='#17262a';x.strokeRect(o.x+1,o.y+1,o.w-2,o.h-2)}
for(let q of crates){let by=Math.sin(performance.now()/220+q.bob)*2;x.fillStyle='#b88b43';x.fillRect(q.x-12,q.y-12+by,24,24);x.strokeStyle='#f2cf7c';x.strokeRect(q.x-12,q.y-12+by,24,24);x.strokeStyle='#604523';x.beginPath();x.moveTo(q.x-9,q.y+by);x.lineTo(q.x+9,q.y+by);x.stroke();if(d(q,player)<q.r+player.r+22){x.fillStyle='#f4d58a';x.font='12px Arial';x.textAlign='center';x.fillText('Press E',q.x,q.y-20)}}
for(let b of bullets){x.fillStyle='#ffdf91';x.beginPath();x.arc(b.x,b.y,3,0,Math.PI*2);x.fill()}
for(let z of zombies){x.fillStyle='#080c0d';x.beginPath();x.arc(z.x,z.y,z.r+4,0,Math.PI*2);x.fill();x.fillStyle='#789e55';x.beginPath();x.arc(z.x,z.y,z.r,0,Math.PI*2);x.fill();x.fillStyle='#ff515c';x.beginPath();x.arc(z.x-5,z.y-3,2,0,7);x.arc(z.x+5,z.y-3,2,0,7);x.fill();x.strokeStyle='#101616';x.beginPath();x.moveTo(z.x-5,z.y+5);x.lineTo(z.x+5,z.y+5);x.stroke()}
if(player){let a=Math.atan2(mouse.y-player.y,mouse.x-player.x);x.strokeStyle='rgba(92,238,215,.6)';x.lineWidth=3;x.beginPath();x.moveTo(player.x,player.y);x.lineTo(player.x+Math.cos(a)*29,player.y+Math.sin(a)*29);x.stroke();if(player.inv<=0||Math.floor(performance.now()/80)%2===0){x.fillStyle='#071114';x.beginPath();x.arc(player.x,player.y,player.r+5,0,7);x.fill();x.fillStyle='#48d9c4';x.beginPath();x.arc(player.x,player.y,player.r,0,7);x.fill();x.fillStyle='#d4fff7';x.beginPath();x.arc(player.x-3,player.y-4,4,0,7);x.fill();x.save();x.translate(player.x,player.y);x.rotate(a);x.fillStyle='#d3e5e7';x.fillRect(4,-4,22,8);x.restore()}}
x.fillStyle='rgba(0,0,0,.22)';x.fillRect(0,0,W,4)}
function frame(t){let dt=Math.min(.033,(t-(last||t))/1000);last=t;update(dt);draw();requestAnimationFrame(frame)}
function pointer(e){let r=c.getBoundingClientRect();mouse.x=(e.clientX-r.left)/r.width*W;mouse.y=(e.clientY-r.top)/r.height*H}
c.addEventListener('pointermove',pointer);c.addEventListener('pointerdown',e=>{c.focus();pointer(e);if(e.button===0){mouse.down=true;shoot()}});window.addEventListener('pointerup',()=>mouse.down=false);c.addEventListener('contextmenu',e=>e.preventDefault());
window.addEventListener('keydown',e=>{if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space'].includes(e.code))e.preventDefault();keys.add(e.code);if(e.code==='KeyE')collect();if(e.code==='Escape')pause();if(e.code==='KeyR'&&over)reset()});window.addEventListener('keyup',e=>keys.delete(e.code));
$('start').onclick=()=>{if(paused){paused=false;$('overlay').classList.remove('show');$('pause').textContent='Pause'}else reset();c.focus()};$('restart').onclick=reset;$('pause').onclick=pause;
player={x:W/2,y:H/2,r:13,speed:205,inv:0};crates.push({x:W/2+100,y:H/2+60,r:13,bob:0});requestAnimationFrame(frame);
})();
</script></body></html>
"""
components.html(GAME, height=650, scrolling=False)
st.caption("Browser-based Canvas game embedded in Streamlit. Click the game area before using keyboard controls.")
