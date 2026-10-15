from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

posts = [
    {"id":1,"username":"gelephu_foodie","avatar":"G","caption":"Best Ema Datshi at Gelephu market! 😋🇧🇹","likes":124,"liked":False,"media":None,"media_type":None,"comments":[{"user":"thimphu_boy","text":"Bro where?"}]},
    {"id":2,"username":"kaydalyrics","avatar":"K","caption":"Kuzu Zangpo from Gelephu! Bhutan's own Instagram is LIVE 📸","likes":342,"liked":True,"media":None,"media_type":None,"comments":[]}
]

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>GelephuGram • Instagram</title>
<link href="https://fonts.googleapis.com/css2?family=Grand+Hotel&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#fff;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto;max-width:470px;margin:0 auto;border-left:1px solid #222;border-right:1px solid #222;min-height:100vh}
.topbar{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;border-bottom:1px solid #222;position:sticky;top:0;background:#000;z-index:20}
.logo{font-family:'Grand Hotel',cursive;font-size:30px}
.top-icons{font-size:22px;display:flex;gap:16px}
.stories{display:flex;gap:14px;padding:12px 12px;overflow-x:auto;border-bottom:1px solid #222}
.story{text-align:center;min-width:66px}
.story-ring{width:62px;height:62px;border-radius:50%;padding:2px;background:linear-gradient(45deg,#feda75,#fa7e1e,#d62976,#962fbf,#4f5bd5)}
.story-img{width:100%;height:100%;border-radius:50%;background:#222;display:flex;align-items:center;justify-content:center;border:2px solid #000;font-weight:bold}
.story span{font-size:11px;margin-top:4px;display:block}
.post{border-bottom:1px solid #222}
.post-h{padding:10px 12px;display:flex;justify-content:space-between;align-items:center}
.user{display:flex;align-items:center;gap:10px}
.avatar{width:32px;height:32px;border-radius:50%;background:linear-gradient(45deg,#ff9933,#ff6600);display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:14px}
.username{font-weight:600;font-size:14px}
.post-media{width:100%;aspect-ratio:1/1;background:#111;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
.post-media img,.post-media video{width:100%;height:100%;object-fit:cover}
.no-media{color:#666;font-size:14px}
.actions{padding:10px 12px;display:flex;justify-content:space-between}
.left-act{display:flex;gap:14px;font-size:24px}
.act{cursor:pointer;user-select:none}
.act.liked{color:#ff3040}
.likes{padding:0 12px;font-weight:600;font-size:14px}
.caption{padding:4px 12px;font-size:14px;line-height:18px}
.comments{padding:4px 12px 0;font-size:14px;color:#a8a8a8}
.com{color:#fff;margin:2px 0}
.com b{margin-right:6px}
.add-comment{display:flex;padding:10px 12px;border-top:1px solid #222;margin-top:8px;gap:10px}
.add-comment input{flex:1;background:transparent;border:none;color:#fff;outline:none;font-size:14px}
.add-comment button{background:none;border:none;color:#0095f6;font-weight:600;cursor:pointer}
.create{padding:12px;border-bottom:1px solid #222;display:flex;gap:10px;align-items:center}
.create input[type="file"]{display:none}
.create label{background:#222;padding:8px 12px;border-radius:8px;cursor:pointer;font-size:18px}
.create textarea{flex:1;background:#111;border:1px solid #222;border-radius:20px;padding:10px 14px;color:#fff;resize:none;outline:none}
.create button.post-btn{background:#0095f6;border:none;color:#fff;padding:8px 16px;border-radius:20px;font-weight:600;cursor:pointer}
.bottom-nav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);width:100%;max-width:470px;background:#000;border-top:1px solid #222;display:flex;justify-content:space-around;padding:10px 0;font-size:22px}
#feed{padding-bottom:60px}
</style>
</head>
<body>
<div class="topbar"><div class="logo">GelephuGram</div><div class="top-icons"><span>♡</span><span>✈️</span></div></div>

<div class="stories">
  <div class="story"><div class="story-ring"><div class="story-img">K</div></div><span>Your story</span></div>
  <div class="story"><div class="story-ring"><div class="story-img">G</div></div><span>gelephu_foodie</span></div>
  <div class="story"><div class="story-ring"><div class="story-img">🇧🇹</div></div><span>bhutan</span></div>
  <div class="story"><div class="story-ring"><div class="story-img">T</div></div><span>thimphu</span></div>
  <div class="story"><div class="story-ring"><div class="story-img">D</div></div><span>druk</span></div>
</div>

<div class="create">
  <label for="media">📷</label>
  <input type="file" id="media" accept="image/*,video/*" onchange="previewMedia(event)">
  <textarea id="cap" rows="1" placeholder="What's in Gelephu?"></textarea>
  <button class="post-btn" onclick="createPost()">Share</button>
</div>
<div id="preview" style="display:none;padding:0 12px 10px"><img id="prevImg" style="width:100%;border-radius:8px;max-height:300px;object-fit:cover"><video id="prevVid" style="width:100%;border-radius:8px;display:none" controls></video><button onclick="clearMedia()" style="background:#222;border:none;color:#fff;padding:4px 8px;border-radius:4px;margin-top:4px">X Remove</button></div>

<div id="feed"></div>
<div class="bottom-nav"><span>⌂</span><span>⌕</span><span>⊕</span><span>◎</span><span style="width:24px;height:24px;background:linear-gradient(45deg,#ff9933,#ff6600);border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:14px">K</span></div>

<script>
let allPosts=[]; let selectedMedia=null; let selectedType=null;
function previewMedia(e){
  let file=e.target.files[0]; if(!file) return;
  let reader=new FileReader();
  reader.onload=function(ev){
    selectedMedia=ev.target.result;
    selectedType=file.type.startsWith('video')?'video':'image';
    document.getElementById('preview').style.display='block';
    if(selectedType==='image'){document.getElementById('prevImg').src=selectedMedia;document.getElementById('prevImg').style.display='block';document.getElementById('prevVid').style.display='none'}
    else{document.getElementById('prevVid').src=selectedMedia;document.getElementById('prevVid').style.display='block';document.getElementById('prevImg').style.display='none'}
  }; reader.readAsDataURL(file);
}
function clearMedia(){selectedMedia=null;selectedType=null;document.getElementById('preview').style.display='none';document.getElementById('media').value='';}

async function load(){
  let r=await fetch('/api/posts'); allPosts=await r.json();
  let feed=document.getElementById('feed'); feed.innerHTML='';
  allPosts.slice().reverse().forEach(p=>{
    from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# FIXED: No empty posts, only real posts will show
posts = []

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GelephuGram</title>
<link href="https://fonts.googleapis.com/css2?family=Grand+Hotel&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#fff;font-family:-apple-system,Segoe UI,Roboto;width:100%;max-width:100%;margin:0}
.topbar{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;border-bottom:1px solid #222;position:sticky;top:0;background:#000;z-index:20}
.logo{font-family:'Grand Hotel',cursive;font-size:30px}
.stories{display:flex;gap:14px;padding:12px;overflow-x:auto;border-bottom:1px solid #222}
.story{text-align:center;min-width:66px}
.story-ring{width:62px;height:62px;border-radius:50%;padding:2px;background:linear-gradient(45deg,#feda75,#fa7e1e,#d62976,#962fbf,#4f5bd5)}
.story-img{width:100%;height:100%;border-radius:50%;background:#222;display:flex;align-items:center;justify-content:center;border:2px solid #000;font-weight:bold}
.story span{font-size:11px;margin-top:4px;display:block}
.post{border-bottom:1px solid #222}
.post-h{padding:10px 12px;display:flex;justify-content:space-between;align-items:center}
.user{display:flex;align-items:center;gap:10px}
.avatar{width:32px;height:32px;border-radius:50%;background:linear-gradient(45deg,#ff9933,#ff6600);display:flex;align-items:center;justify-content:center;font-weight:bold}
.post-media{width:100%;background:#111;display:flex;align-items:center;justify-content:center}
.post-media img,.post-media video{width:100%;height:auto;max-height:600px;object-fit:contain;display:block}
.actions{padding:10px 12px;display:flex;justify-content:space-between;font-size:24px}
.act{cursor:pointer}
.act.liked{color:#ff3040}
.likes{padding:0 12px;font-weight:600;font-size:14px}
.caption{padding:4px 12px;font-size:14px}
.comments{padding:4px 12px;color:#a8a8a8;font-size:14px}
.com{color:#fff}
.add-comment{display:flex;padding:10px 12px;border-top:1px solid #222;gap:10px}
.add-comment input{flex:1;background:transparent;border:none;color:#fff;outline:none}
.add-comment button{background:none;border:none;color:#0095f6;font-weight:600}
.create{padding:12px;border-bottom:1px solid #222;display:flex;gap:10px}
.create input[type="file"]{display:none}
.create label{background:#222;padding:8px 12px;border-radius:8px;cursor:pointer}
.create textarea{flex:1;background:#111;border:1px solid #222;border-radius:20px;padding:10px 14px;color:#fff;outline:none}
.create button{background:#0095f6;border:none;color:#fff;padding:8px 16px;border-radius:20px;font-weight:600}
#feed{padding-bottom:60px}
.bottom-nav{position:fixed;bottom:0;width:100%;background:#000;border-top:1px solid #222;display:flex;justify-content:space-around;padding:12px 0;font-size:22px}
</style>
</head>
<body>
<div class="topbar"><div class="logo">GelephuGram</div><div>♡ ✈️</div></div>
<div class="stories"><div class="story"><div class="story-ring"><div class="story-img">K</div></div><span>Your story</span></div><div class="story"><div class="story-ring"><div class="story-img">G</div></div><span>gelephu_foodie</span></div></div>
<div class="create">
<label for="media">📷</label><input type="file" id="media" accept="image/*,video/*" onchange="previewMedia(event)">
<textarea id="cap" placeholder="What's in Gelephu?"></textarea>
<button onclick="createPost()">Share</button>
</div>
<div id="preview" style="display:none;padding:10px"><img id="prevImg" style="width:100%;border-radius:8px;display:none"><video id="prevVid" style="width:100%;border-radius:8px;display:none" controls></video><button onclick="clearMedia()" style="background:#222;color:#fff;border:none;padding:4px 8px;border-radius:4px">X</button></div>
<div id="feed"></div>
<div class="bottom-nav"><span>⌂</span><span>⌕</span><span>⊕</span><span>◎</span><span>K</span></div>
<script>
let selectedMedia=null,selectedType=null;
function previewMedia(e){
  let file=e.target.files[0]; if(!file) return;
  let reader=new FileReader();
  reader.onload=function(ev){
    selectedMedia=ev.target.result; selectedType=file.type.startsWith('video')?'video':'image';
    document.getElementById('preview').style.display='block';
    if(selectedType==='image'){document.getElementById('prevImg').src=selectedMedia;document.getElementById('prevImg').style.display='block';document.getElementById('prevVid').style.display='none'}
    else{document.getElementById('prevVid').src=selectedMedia;document.getElementById('prevVid').style.display='block';document.getElementById('prevImg').style.display='none'}
  }; reader.readAsDataURL(file);
}
function clearMedia(){selectedMedia=null;selectedType=null;document.getElementById('preview').style.display='none';document.getElementById('media').value='';}
async function load(){
  let r=await fetch('/api/posts'); let allPosts=await r.json();
  let feed=document.getElementById('feed'); feed.innerHTML='';
  if(allPosts.length===0){feed.innerHTML='<div style="padding:40px;text-align:center;color:#777">No posts yet<br>Be first to post photo/video from Gelephu! 📸</div>';return}
  allPosts.slice().reverse().forEach(p=>{
    let mediaHtml='';
    if(p.media){
      if(p.media_type==='video') mediaHtml=`<div class="post-media"><video src="${p.media}" controls></video></div>`;
      else mediaHtml=`<div class="post-media"><img src="${p.media}"></div>`;
    }
    let comHtml=p.comments.map(c=>`<div class="com"><b>${c.user}</b> ${c.text}</div>`).join('');
    let div=document.createElement('div'); div.className='post';
    div.innerHTML=`<div class="post-h"><div class="user"><div class="avatar">${p.avatar}</div><div>${p.username}</div></div><div>⋯</div></div>${mediaHtml}<div class="actions"><div style="display:flex;gap:14px"><span class="act ${p.liked?'liked':''}" onclick="like(${p.id})">${p.liked?'♥':'♡'}</span><span onclick="document.getElementById('inp-${p.id}').focus()">💬</span><span>✈️</span></div><span>🔖</span></div><div class="likes">${p.likes} likes</div><div class="caption"><b>${p.username}</b> ${p.caption}</div><div class="comments">${comHtml}</div><div class="add-comment"><input id="inp-${p.id}" placeholder="Add a comment..."><button onclick="comment(${p.id})">Post</button></div>`;
    feed.appendChild(div);
  });
}
async function createPost(){
  let cap=document.getElementById('cap').value; if(!cap &&!selectedMedia) return alert('Add photo/video or caption');
  await fetch('/api/posts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({caption:cap,media:selectedMedia,media_type:selectedType})});
  document.getElementById('cap').value=''; clearMedia(); load();
}
async function like(id){await fetch('/api/posts/'+id+'/like',{method:'POST'}); load();}
async function comment(id){
  let inp=document.getElementById('inp-'+id); let t=inp.value.trim(); if(!t) return;
  await fetch('/api/posts/'+id+'/comment',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t})});
  inp.value=''; load();
}
load();
</script>
</body>
</html>
    """
@app.route('/api/posts', methods=['GET'])
def get_posts(): return jsonify(posts)
@app.route('/api/posts', methods=['POST'])
def new_post():
    data=request.json
    p={"id":len(posts)+1,"username":"kaydalyrics","avatar":"K","caption":data.get('caption',''),"likes":0,"liked":False,"media":data.get('media'),"media_type":data.get('media_type'),"comments":[]}
    posts.append(p); return jsonify(p)
@app.route('/api/posts/<int:pid>/like', methods=['POST'])
def like(pid):
    for p in posts:
        if p['id']==pid: p['liked']=not p['liked']; p['likes']+=1 if p['liked'] else -1; return jsonify(p)
    return jsonify({"error":"not found"}),404
@app.route('/api/posts/<int:pid>/comment', methods=['POST'])
def comm(pid):
    data=request.json
    for p in posts:
        if p['id']==pid: p['comments'].append({"user":"guest","text":data['text']}); return jsonify(p)
    return jsonify({"error":"not found"}),404
if __name__=='__main__':
    import os; port=int(os.environ.get("PORT",10000)); app.run(host='0.0.0.0',port=port)
      if(p.media_type==='video') mediaHtml=`<video src="${p.media}" controls></video>`;
      else mediaHtml=`<img src="${p.media}">`;
    } else mediaHtml=`<div class="no-media"></div>`;
    let comHtml=p.comments.map(c=>`<div class="com"><b>${c.user}</b>${c.text}</div>`).join('');
    let div=document.createElement('div'); div.className='post';
    div.innerHTML=`<div class="post-h"><div class="user"><div class="avatar">${p.avatar}</div><div class="username">${p.username}</div></div><div>⋯</div></div><div class="post-media">${mediaHtml}</div><div class="actions"><div class="left-act"><span class="act ${p.liked?'liked':''}" onclick="like(${p.id})">${p.liked?'♥':'♡'}</span><span class="act" onclick="document.getElementById('inp-${p.id}').focus()">💬</span><span class="act">✈️</span></div><span>🔖</span></div><div class="likes">${p.likes} likes</div><div class="caption"><b>${p.username}</b> ${p.caption}</div><div class="comments">${comHtml}</div><div class="add-comment"><input id="inp-${p.id}" placeholder="Add a comment..."><button onclick="comment(${p.id})">Post</button></div>`;
    feed.appendChild(div);
  });
}
async function createPost(){
  let cap=document.getElementById('cap').value; if(!cap &&!selectedMedia) return alert('Add photo/video or caption');
  await fetch('/api/posts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({caption:cap,media:selectedMedia,media_type:selectedType})});
  document.getElementById('cap').value=''; clearMedia(); load();
}
async function like(id){await fetch('/api/posts/'+id+'/like',{method:'POST'}); load();}
async function comment(id){
  let inp=document.getElementById('inp-'+id); let t=inp.value.trim(); if(!t) return;
  await fetch('/api/posts/'+id+'/comment',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t})});
  inp.value=''; load();
}
load();
</script>
</body>
</html>
    """

@app.route('/api/posts', methods=['GET'])
def get_posts(): return jsonify(posts)

@app.route('/api/posts', methods=['POST'])
def new_post():
    data=request.json
    p={"id":len(posts)+1,"username":"kaydalyrics","avatar":"K","caption":data.get('caption',''),"likes":0,"liked":False,"media":data.get('media'),"media_type":data.get('media_type'),"comments":[]}
    posts.append(p); return jsonify(p)

@app.route('/api/posts/<int:pid>/like', methods=['POST'])
def like(pid):
    for p in posts:
        if p['id']==pid:
            p['liked']=not p['liked']; p['likes']+=1 if p['liked'] else -1; return jsonify(p)
    return jsonify({"error":"not found"}),404

@app.route('/api/posts/<int:pid>/comment', methods=['POST'])
def comm(pid):
    data=request.json
    for p in posts:
        if p['id']==pid: p['comments'].append({"user":"kaydalyrics","text":data['text']}); return jsonify(p)
    return jsonify({"error":"not found"}),404

if __name__=='__main__':
    import os; port=int(os.environ.get("PORT",10000)); app.run(host='0.0.0.0',port=port)
