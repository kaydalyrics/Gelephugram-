from flask import Flask, request, jsonify
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

# Posts with comments - GelephuGram V2
posts = [
    {
        "id": 1, 
        "username": "Gelephu_Foodie", 
        "caption": "Best Ema Datshi at Gelephu market! 🇧🇹", 
        "likes": 12,
        "comments": [
            {"user": "ThimphuBoy", "text": "Looks delicious!"}
        ]
    },
    {
        "id": 2, 
        "username": "kaydalyrics", 
        "caption": "Kuzu Zangpo from GelephuGram! Bhutan's own Instagram", 
        "likes": 25,
        "comments": []
    }
]

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GelephuGram V2 - With Comments</title>
<style>
body{font-family:Arial;background:#fafafa;margin:0;padding:0}
.header{background:white;border-bottom:1px solid #ddd;padding:12px;text-align:center;position:sticky;top:0;z-index:10}
.header h1{margin:0;background:linear-gradient(45deg,#ff9933,#ff6600);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:24px}
.post{background:white;border:1px solid #ddd;border-radius:8px;margin:15px auto;max-width:500px;overflow:hidden}
.post-head{padding:12px;font-weight:bold;display:flex;justify-content:space-between}
.post-img{width:100%;max-height:400px;object-fit:cover;background:#f0f0f0;display:none}
.post-actions{padding:10px 12px;display:flex;gap:15px}
.like-btn{cursor:pointer;font-size:20px}
.caption{padding:0 12px 8px}
.comments{padding:0 12px 10px;font-size:14px;color:#333}
.comment{margin:4px 0}
.comment b{margin-right:5px}
.comment-box{display:flex;border-top:1px solid #eee;padding:8px 12px;gap:8px}
.comment-box input{flex:1;border:none;outline:none;background:#f5f5f5;border-radius:20px;padding:8px 12px}
.comment-box button{border:none;background:#ff6600;color:white;border-radius:20px;padding:6px 15px;cursor:pointer}
.create-box{background:white;border:1px solid #ddd;border-radius:8px;margin:15px auto;max-width:500px;padding:15px}
.create-box textarea{width:100%;border:1px solid #ddd;border-radius:8px;padding:10px;resize:none;box-sizing:border-box}
.create-box button{background:#ff6600;color:white;border:none;padding:10px 20px;border-radius:8px;cursor:pointer;margin-top:10px;width:100%;font-weight:bold}
</style>
</head>
<body>
<div class="header"><h1>📸 GelephuGram V2</h1><small>Bhutan's Instagram - Now with Comments!</small></div>

<div class="create-box">
<textarea id="caption" rows="2" placeholder="What's happening in Gelephu?"></textarea>
<button onclick="createPost()">Post to GelephuGram</button>
</div>

<div id="feed"></div>

<script>
let allPosts = [];
async function loadPosts(){
  let res = await fetch('/api/posts');
  allPosts = await res.json();
  let feed = document.getElementById('feed');
  feed.innerHTML = '';
  allPosts.slice().reverse().forEach(p=>{
    let div = document.createElement('div');
    div.className='post';
    let commentsHtml = p.comments.map(c=>`<div class="comment"><b>${c.user}:</b> ${c.text}</div>`).join('');
    div.innerHTML = `
      <div class="post-head"><span>@${p.username}</span><span>📍 Gelephu</span></div>
      <div class="caption"><b>@${p.username}</b> ${p.caption}</div>
      <div class="post-actions"><span class="like-btn" onclick="likePost(${p.id})">❤️ ${p.likes}</span><span>💬 ${p.comments.length}</span></div>
      <div class="comments" id="comments-${p.id}">${commentsHtml}</div>
      <div class="comment-box">
        <input type="text" id="input-${p.id}" placeholder="Add a comment...">
        <button onclick="addComment(${p.id})">Post</button>
      </div>
    `;
    feed.appendChild(div);
  });
}
async function createPost(){
  let cap = document.getElementById('caption').value;
  if(!cap) return alert('Write something!');
  await fetch('/api/posts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:'kaydalyrics',caption:cap})});
  document.getElementById('caption').value='';loadPosts();
}
async function likePost(id){
  await fetch('/api/posts/'+id+'/like',{method:'POST'});loadPosts();
}
async function addComment(id){
  let input = document.getElementById('input-'+id);
  let text = input.value.trim();
  if(!text) return;
  await fetch('/api/posts/'+id+'/comment',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user:'Guest',text:text})});
  input.value='';loadPosts();
}
loadPosts();
</script>
</body>
</html>
    """

@app.route('/api/posts', methods=['GET'])
def get_posts(): return jsonify(posts)

@app.route('/api/posts', methods=['POST'])
def new_post():
    data = request.json
    new = {"id": len(posts)+1, "username": data.get('username','kaydalyrics'), "caption": data['caption'], "likes": 0, "comments": []}
    posts.append(new)
    return jsonify(new)

@app.route('/api/posts/<int:pid>/like', methods=['POST'])
def like(pid):
    for p in posts:
        if p['id']==pid: p['likes']+=1; return jsonify(p)
    return jsonify({"error":"not found"}),404

@app.route('/api/posts/<int:pid>/comment', methods=['POST'])
def comment(pid):
    data = request.json
    for p in posts:
        if p['id']==pid:
            p['comments'].append({"user": data.get('user','Guest'), "text": data['text']})
            return jsonify(p)
    return jsonify({"error":"not found"}),404

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
