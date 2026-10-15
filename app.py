from flask import Flask, request, jsonify, render_template_string
import os
app = Flask(__name__)
posts = [
 {"id":1,"user":"karma.wangmo","place":"Gelephu Market","text":"Ema Datshi today! 🌶️","likes":1247,"liked":False,"img":"https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600"},
 {"id":2,"user":"pema.travels","place":"Gelephu Valley","text":"Sunrise hike ⛰️","likes":892,"liked":False,"img":"https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600"}
]
HTML = """<!DOCTYPE html><html><head><meta name=viewport content="width=device-width,initial-scale=1"><title>GelephuGram ONLINE</title>
<style>body{margin:0;background:#fff8e1;font-family:sans-serif}header{background:linear-gradient(90deg,#ff8f00,#ffd600);padding:14px;text-align:center;font-weight:bold;font-size:22px}main{max-width:500px;margin:auto;padding:10px}.card{background:white;border-radius:16px;padding:12px;margin:12px 0;box-shadow:0 4px 10px #0001}.input-row{display:flex;gap:8px}input[type=text]{flex:1;padding:12px;border-radius:20px;border:2px solid #ff8f00}button{background:#ff8f00;color:white;border:0;border-radius:20px;padding:10px 16px;font-weight:bold}.post{border:1px solid #ffe082;border-radius:16px;overflow:hidden;margin:14px 0;background:white}.post-top{padding:10px;display:flex;gap:10px;align-items:center}.avatar{width:40px;height:40px;background:linear-gradient(135deg,#ff8f00,#ffd600);border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold}.post img{width:100%}.actions{padding:10px;display:flex;gap:18px;font-size:20px}.info{padding:0 12px 12px}.small{color:gray;font-size:11px}</style>
</head><body><header>📸 GelephuGram ONLINE 🇧🇹 LIVE</header><main><div class=card><div class=input-row><input id=txt type=text placeholder="Post for all Gelephu!"><input id=file type=file accept=image/* style=display:none><label for=file style=background:#333;color:white;padding:10px 12px;border-radius:20px>📷</label><button onclick=addPost()>Post</button></div><p id=prev style=display:none><img id=prevImg style=width:100%;border-radius:12px;margin-top:10px></p></div><div id=feed>Loading...</div></main>
<script>
let selectedImage="";let allPosts=[];
document.getElementById('file').addEventListener('change',e=>{let f=e.target.files[0];if(!f)return;let r=new FileReader();r.onload=ev=>{selectedImage=ev.target.result;document.getElementById('prevImg').src=selectedImage;document.getElementById('prev').style.display='block'};r.readAsDataURL(f);});
async function load(){let res=await fetch('/api/posts');allPosts=await res.json();render();}
function render(){let h="";for(let i=allPosts.length-1;i>=0;i--){let p=allPosts[i];h+=`<div class=post><div class=post-top><div class=avatar>${p.user[0].toUpperCase()}</div><div><b>@${p.user}</b><br><span class=small>📍 ${p.place}</span></div></div>${p.img?`<img src="${p.img}">`:''}<div class=actions><b onclick="like(${p.id})">${p.liked?'❤️':'🤍'} ${p.likes}</b> 💬 ✈️</div><div class=info><b>@${p.user}</b> ${p.text}</div></div>`}document.getElementById('feed').innerHTML=h;}
async function addPost(){let t=document.getElementById('txt').value;if(!t&&!selectedImage)return;await fetch('/api/posts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t,img:selectedImage,user:'you',place:'Gelephu, Bhutan'})});document.getElementById('txt').value='';selectedImage='';document.getElementById('prev').style.display='none';load();}
async function like(id){await fetch('/api/like/'+id,{method:'POST'});load();}
load();
</script></body></html>"""
@app.route('/')
def home(): return render_template_string(HTML)
@app.route('/api/posts')
def get_posts(): return jsonify(posts)
@app.route('/api/posts', methods=['POST'])
def create_post():
 data=request.json
 new={"id":len(posts)+1,"user":data.get("user","you"),"place":data.get("place","Gelephu"),"text":data.get("text",""),"likes":0,"liked":False,"img":data.get("img","")}
 posts.append(new); return jsonify(new)
@app.route('/api/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
 for p in posts:
  if p["id"]==post_id:
   p["liked"]=not p["liked"]; p["likes"]+=1 if p["liked"] else -1; return jsonify(p)
 return jsonify({"error":"not found"}),404
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.environ.get("PORT",5000)))
