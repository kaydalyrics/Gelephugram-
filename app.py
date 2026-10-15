from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
posts = []

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GelephuGram • Instagram</title>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;color:#fff;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;width:100%;overflow-x:hidden}
.top{height:60px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;border-bottom:1px solid #262626;position:sticky;top:0;background:#000;z-index:100}
.logo{font-family:Brush Script MT,cursive;font-size:32px}
.icons{display:flex;gap:18px;font-size:22px}
.story-bar{display:flex;gap:14px;padding:12px 10px;overflow-x:auto;border-bottom:1px solid #262626;scrollbar-width:none}
.story-bar::-webkit-scrollbar{display:none}
.story-item{text-align:center;min-width:66px}
.ring{width:66px;height:66px;border-radius:50%;padding:2.5px;background:linear-gradient(45deg,#feda75,#fa7e1e,#d62976,#4f5bd5)}
.ring-inner{width:100%;height:100%;border-radius:50%;background:#000;border:2.5px solid #000;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:22px}
.story-name{font-size:12px;margin-top:4px}
.create-box{padding:12px 10px;border-bottom:1px solid #262626;display:flex;gap:10px;align-items:center}
.create-box img{width:32px;height:32px;border-radius:50%}
.create-input{flex:1;background:#121212;border:1px solid #262626;border-radius:20px;padding:8px 14px;color:#fff;outline:none}
.btn-share{background:#0095f6;border:none;color:#fff;padding:7px 16px;border-radius:8px;font-weight:600;cursor:pointer}
.btn-share:disabled{opacity:.4}
.post{border-bottom:1px solid #262626;padding-bottom:8px}
.post-head{padding:12px 10px;display:flex;align-items:center;justify-content:space-between}
.head-left{display:flex;align-items:center;gap:10px}
.avatar{width:32px;height:32px;border-radius:50%;background:linear-gradient(45deg,#feda75,#d62976);display:flex;align-items:center;justify-content:center;font-weight:bold}
.username{font-weight:600;font-size:14px}
.post-media{width:100%;background:#111;display:flex;align-items:center;justify-content:center;max-height:80vh;overflow:hidden}
.post-media img,.post-media video{width:100%;height:auto;display:block;object-fit:contain}
.post-actions{padding:10px 12px 4px;display:flex;justify-content:space-between;font-size:24px}
.actions-left{display:flex;gap:16px}
.actions-left i,.actions-right i{cursor:pointer}
.liked{color:#ed4956!important}
.bookmarked{color:#fff!important}
.likes{padding:0 12px;font-weight:600;font-size:14px;margin-top:2px}
.caption{padding:4px 12px;font-size:14px;line-height:18px;word-break:break-word}
.caption b{margin-right:6px}
.comments{padding:2px 12px}
.comment-line{font-size:14px;margin:2px 0}
.comment-line b{font-weight:600}
.view-comments{color:#a8a8a8;font-size:14px;padding:2px 12px;cursor:pointer}
.add-comment{border-top:1px solid #262626;margin-top:8px;padding:10px 12px;display:flex;gap:10px;align-items:center}
.add-comment input{flex:1;background:transparent;border:none;color:#fff;outline:none;font-size:14px}
.add-comment button{background:none;border:none;color:#0095f6;font-weight:600;cursor:pointer}
.add-comment button:disabled{opacity:.4}
.preview{padding:10px;display:none}
.preview img,.preview video{width:100%;border-radius:8px}
.empty{text-align:center;padding:60px 20px;color:#a8a8a8}
.empty i{font-size:48px;margin-bottom:12px;display:block}
</style>
</head>
<body>
<div class="top">
<div class="logo">GelephuGram</div>
<div class="icons"><i class="fa-regular fa-heart"></i><i class="fa-regular fa-paper-plane"></i></div>
</div>

<div class="story-bar">
<div class="story-item"><div class="ring"><div class="ring-inner">K</div></div><div class="story-name">Your story</div></div>
<div class="story-item"><div class="ring"><div class="ring-inner">G</div></div><div class="story-name">gelephu</div></div>
<div class="story-item"><div class="ring"><div class="ring-inner">T</div></div><div class="story-name">tashigatshel</div></div>
<div class="story-item"><div class="ring"><div class="ring-inner">Z</div></div><div class="story-name">zilnoen</div></div>
</div>

<div class="create-box">
<img src="https://i.pravatar.cc/100?img=5">
<input type="file" id="fileInput" accept="image/*,video/*" style="display:none" onchange="handleFile(event)">
<label for="fileInput" style="cursor:pointer"><i class="fa-regular fa-image" style="font-size:22px"></i></label>
<input id="captionInput" class="create-input" placeholder="What's in Gelephu?">
<button id="shareBtn" class="btn-share" onclick="createPost()">Share</button>
</div>

<div id="previewBox" class="preview">
<img id="previewImg" style="display:none"><video id="previewVideo" style="display:none" controls></video>
<div style="margin-top:6px"><button onclick="clearPreview()" style="background:#262626;border:none;color:#fff;padding:4px 10px;border-radius:4px">✕ Remove</button></div>
</div>

<div id="feed"></div>

<script>
let selectedMedia = null;
let selectedType = null;

function handleFile(e){
 let file=e.target.files[0]; if(!file) return;
 let reader=new FileReader();
 reader.onload=function(ev){
  selectedMedia=ev.target.result;
  selectedType=file.type.startsWith('video')?'video':'image';
  document.getElementById('previewBox').style.display='block';
  if(selectedType==='image'){
   document.getElementById('previewImg').src=selectedMedia;
   document.getElementById('previewImg').style.display='block';
   document.getElementById('previewVideo').style.display='none';
  }else{
   document.getElementById('previewVideo').src=selectedMedia;
   document.getElementById('previewVideo').style.display='block';
   document.getElementById('previewImg').style.display='none';
  }
 };
 reader.readAsDataURL(file);
}
function clearPreview(){
 selectedMedia=null; selectedType=null;
 document.getElementById('previewBox').style.display='none';
 document.getElementById('fileInput').value='';
 document.getElementById('previewImg').src='';
 document.getElementById('previewVideo').src='';
}
function escapeHtml(t){
 if(!t) return '';
 return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
async function loadFeed(){
 let res=await fetch('/api/posts');
 let data=await res.json();
 let feed=document.getElementById('feed');
 feed.innerHTML='';
 if(data.length===0){
  feed.innerHTML='<div class="empty"><i class="fa-solid fa-camera"></i>No posts yet<br>Share your first Gelephu moment!</div>';
  return;
 }
 data.slice().reverse().forEach(p=>{
  let mediaHtml='';
  if(p.media){
   if(p.media_type==='video') mediaHtml='<div class="post-media"><video src="'+p.media+'" controls playsinline></video></div>';
   else mediaHtml='<div class="post-media"><img src="'+p.media+'" ondblclick="likePost('+p.id+')"></div>';
  }
  let commentsHtml='';
  p.comments.forEach(c=>{
   commentsHtml+='<div class="comment-line"><b>'+escapeHtml(c.user)+'</b> '+escapeHtml(c.text)+'</div>';
  });
  let div=document.createElement('div');
  div.className='post';
  div.innerHTML=
  '<div class="post-head"><div class="head-left"><div class="avatar">'+p.avatar+'</div><div class="username">'+escapeHtml(p.username)+' • <span style="color:#a8a8a8;font-weight:400">'+p.time+'</span></div></div><i class="fa-solid fa-ellipsis"></i></div>'+
  mediaHtml+
  '<div class="post-actions"><div class="actions-left"><i id="heart-'+p.id+'" class="'+(p.liked?'fa-solid fa-heart liked':'fa-regular fa-heart')+'" onclick="likePost('+p.id+')"></i><i class="fa-regular fa-comment" onclick="document.getElementById(\\'commentInput-'+p.id+'\\').focus()"></i><i class="fa-regular fa-paper-plane"></i></div><div class="actions-right"><i class="fa-regular fa-bookmark"></i></div></div>'+
  '<div class="likes">'+p.likes+' likes</div>'+
  '<div class="caption"><b>'+escapeHtml(p.username)+'</b> '+escapeHtml(p.caption)+'</div>'+
  '<div class="comments">'+commentsHtml+'</div>'+
  '<div class="add-comment"><i class="fa-regular fa-face-smile"></i><input id="commentInput-'+p.id+'" placeholder="Add a comment..."><button onclick="commentPost('+p.id+')">Post</button></div>';
  feed.appendChild(div);
 });
}
async function createPost(){
 let cap=document.getElementById('captionInput').value.trim();
 if(!cap &&!selectedMedia){ alert('Add photo or caption'); return; }
 let btn=document.getElementById('shareBtn'); btn.disabled=true; btn.textContent='Posting...';
 try{
  await fetch('/api/posts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({caption:cap,media:selectedMedia,media_type:selectedType})});
  document.getElementById('captionInput').value=''; clearPreview(); await loadFeed();
 }catch(e){ alert('Failed'); }
 btn.disabled=false; btn.textContent='Share';
}
async function likePost(id){
 try{
  await fetch('/api/posts/'+id+'/like',{method:'POST'});
  await loadFeed();
 }catch(e){}
}
async function commentPost(id){
 let inp=document.getElementById('commentInput-'+id);
 let txt=inp.value.trim(); if(!txt) return;
 try{
  await fetch('/api/posts/'+id+'/comment',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:txt})});
  inp.value=''; await loadFeed();
 }catch(e){}
}
loadFeed();
</script>
</body>
</html>
'''

@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(posts)

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.json
    new_id = len(posts) + 1
    post = {
        "id": new_id,
        "username": "kaydalyrics",
        "avatar": "K",
        "caption": data.get('caption',''),
        "likes": 0,
        "liked": False,
        "media": data.get('media'),
        "media_type": data.get('media_type'),
        "comments": [],
        "time": "now"
    }
    posts.append(post)
    return jsonify(post)

@app.route('/api/posts/<int:pid>/like', methods=['POST'])
def toggle_like(pid):
    for p in posts:
        if p['id'] == pid:
            p['liked'] = not p['liked']
            if p['liked']:
                p['likes'] += 1
            else:
                p['likes'] -= 1
                if p['likes'] < 0:
                    p['likes'] = 0
            return jsonify(p)
    return jsonify({"error":"not found"}),404

@app.route('/api/posts/<int:pid>/comment', methods=['POST'])
def add_comment(pid):
    data = request.json
    for p in posts:
        if p['id'] == pid:
            p['comments'].append({"user":"guest","text":data.get('text','')})
            return jsonify(p)
    return jsonify({"error":"not found"}),404

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT",10000))
    app.run(host='0.0.0.0',port=port)
