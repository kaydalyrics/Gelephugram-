from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
posts = []

@app.route('/')
def home():
    html = '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#fff;font-family:Arial;width:100%}
.top{padding:14px;text-align:center;font-size:28px;border-bottom:1px solid #222;position:sticky;top:0;background:#000}
.story{display:flex;gap:12px;padding:10px;overflow:auto;border-bottom:1px solid #222}
.s{text-align:center}
.r{width:60px;height:60px;border-radius:50%;padding:2px;background:linear-gradient(45deg,#feda75,#fa7e1e,#d62976)}
.i{width:100%;height:100%;border-radius:50%;background:#222;display:flex;align-items:center;justify-content:center;border:2px solid #000}
.post{border-bottom:1px solid #222}
.h{padding:10px;display:flex;gap:8px;align-items:center}
.a{width:30px;height:30px;border-radius:50%;background:#f90;display:flex;align-items:center;justify-content:center;font-weight:bold}
.m img,.m video{width:100%;display:block}
.act{padding:10px;font-size:22px;display:flex;gap:14px}
.likes{padding:0 10px;font-weight:bold;font-size:14px}
.cap{padding:4px 10px;font-size:14px}
.cmt{padding:4px 10px;color:#aaa;font-size:14px}
.b{color:#fff}
.add{display:flex;padding:8px 10px;border-top:1px solid #222;gap:8px}
.add input{flex:1;background:transparent;border:none;color:#fff;outline:none}
.add button{background:none;border:none;color:#0af;font-weight:bold}
.create{padding:10px;border-bottom:1px solid #222;display:flex;gap:8px}
.create textarea{flex:1;background:#111;border:1px solid #222;border-radius:18px;padding:8px 12px;color:#fff;outline:none}
.create button{background:#0af;border:none;color:#fff;padding:8px 14px;border-radius:18px;font-weight:bold}
</style>
</head>
<body>
<div class="top">ZILNOEN'S</div>
<div class="story"><div class="s"><div class="r"><div class="i">K</div></div><div style="font-size:11px">You</div></div></div>
<div class="create"><input type="file" id="f" accept="image/*,video/*" style="display:none" onchange="pv(event)"><label for="f" style="background:#222;padding:8px;border-radius:8px">📷</label><textarea id="cap" placeholder="What in your mind?"></textarea><button onclick="post()">Share</button></div>
<div id="pr" style="display:none;padding:10px"><img id="pi" style="width:100%;border-radius:8px;display:none"><video id="pv" style="width:100%;border-radius:8px;display:none" controls></video><button onclick="clr()" style="background:#222;color:#fff;border:none;padding:4px 8px;border-radius:4px;margin-top:4px">X</button></div>
<div id="feed"></div>
<script>
let sm=null,st=null;
function pv(e){
 let file=e.target.files[0];
 if(!file)return;
 let r=new FileReader();
 r.onload=function(ev){
  sm=ev.target.result;
  st=file.type.startsWith('video')?'video':'image';
  document.getElementById('pr').style.display='block';
  if(st=='image'){
   document.getElementById('pi').src=sm;
   document.getElementById('pi').style.display='block';
   document.getElementById('pv').style.display='none'
  }else{
   document.getElementById('pv').src=sm;
   document.getElementById('pv').style.display='block';
   document.getElementById('pi').style.display='none'
  }
 };
 r.readAsDataURL(file)
}
function clr(){sm=null;st=null;document.getElementById('pr').style.display='none';document.getElementById('f').value=''}
async function load(){
 let r=await fetch('/api/posts');
 let ps=await r.json();
 let feed=document.getElementById('feed');
 feed.innerHTML='';
 if(ps.length==0){feed.innerHTML='<div style="padding:40px;text-align:center;color:#777">No posts yet<br>Be first! 📸</div>';return}
 ps.slice().reverse().forEach(p=>{
  let mh='';
  if(p.media){
   if(p.media_type=='video')mh='<div class="m"><video src="'+p.media+'" controls></video></div>';
   else mh='<div class="m"><img src="'+p.media+'"></div>';
  }
  let ch=p.comments.map(c=>'<div class="b"><b>'+c.user+'</b> '+c.text+'</div>').join('');
  let d=document.createElement('div');
  d.className='post';
  d.innerHTML='<div class="h"><div class="a">'+p.avatar+'</div><div>'+p.username+'</div></div>'+mh+'<div class="act"><span onclick="like('+p.id+')">'+(p.liked?'♥':'♡')+'</span><span>💬</span><span>✈️</span></div><div class="likes">'+p.likes+' likes</div><div class="cap"><b>'+p.username+'</b> '+p.caption+'</div><div class="cmt">'+ch+'</div><div class="add"><input id="inp-'+p.id+'" placeholder="Add comment..."><button onclick="cmt('+p.id+')">Post</button></div>';
  feed.appendChild(d)
 })
}
async function post(){
 let cap=document.getElementById('cap').value;
 if(!cap&&!sm)return alert('Add photo or caption');
 await fetch('/api/posts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({caption:cap,media:sm,media_type:st})});
 document.getElementById('cap').value='';
 clr();
 load()
}
async function like(id){await fetch('/api/posts/'+id+'/like',{method:'POST'});load()}
async function cmt(id){
 let inp=document.getElementById('inp-'+id);
 let t=inp.value.trim();
 if(!t)return;
 await fetch('/api/posts/'+id+'/comment',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t})});
 inp.value='';
 load()
}
load();
</script>
</body>
</html>
'''
    return html

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(posts)

@app.route('/api/posts', methods=['POST'])
def new_post():
    d=request.json
    p={"id":len(posts)+1,"username":"kaydalyrics","avatar":"K","caption":d.get('caption',''),"likes":0,"liked":False,"media":d.get('media'),"media_type":d.get('media_type'),"comments":[]}
    posts.append(p)
    return jsonify(p)

@app.route('/api/posts/<int:pid>/like', methods=['POST'])
def like(pid):
    for p in posts:
        if p['id']==pid:
            p['liked']=not p['liked']
            p['likes']+=1 if p['liked'] else -1
            return jsonify(p)
    return jsonify({"error":"not found"}),404

@app.route('/api/posts/<int:pid>/comment', methods=['POST'])
def comm(pid):
    d=request.json
    for p in posts:
        if p['id']==pid:
            p['comments'].append({"user":"guest","text":d['text']})
            return jsonify(p)
    return jsonify({"error":"not found"}),404

if __name__=='__main__':
    import os
    port=int(os.environ.get("PORT",10000))
    app.run(host='0.0.0.0',port=port)
