<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GelephuGram V3</title>
<style>
body{margin:0;background:#fff8e1;font-family:sans-serif}
header{background:linear-gradient(90deg,#ff8f00,#ffd600);padding:14px;text-align:center;font-weight:bold;font-size:22px;color:#000;position:sticky;top:0;z-index:10}
header span{font-size:12px;display:block;font-weight:normal}
main{max-width:500px;margin:auto;padding:10px}
.card{background:white;border-radius:16px;padding:12px;margin:12px 0;box-shadow:0 4px 10px #0001}
.input-row{display:flex;gap:8px;align-items:center}
.input-row input[type=text]{flex:1;padding:12px;border-radius:20px;border:2px solid #ff8f00}
.btn{background:#ff8f00;color:white;border:0;border-radius:20px;padding:10px 16px;font-weight:bold}
.btn-photo{background:#333}
.post{border:1px solid #ffe082;border-radius:16px;overflow:hidden;margin:14px 0;background:white}
.post-top{padding:10px;display:flex;gap:10px;align-items:center}
.avatar{width:40px;height:40px;background:linear-gradient(135deg,#ff8f00,#ffd600);border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold}
.post img{width:100%;max-height:400px;object-fit:cover}
.actions{padding:10px;display:flex;gap:18px;font-size:22px}
.actions b{cursor:pointer}
.info{padding:0 12px 12px}
.small{color:gray;font-size:11px}
</style>
</head>
<body>
<header>📸 GelephuGram V3 🇧🇹 <span>Druk's Instagram • Made in Gelephu</span></header>
<main>
<div class="card">
<div class="input-row">
<input id="txt" type="text" placeholder="What's happening in Gelephu?">
<label class="btn btn-photo">📷<input id="file" type="file" accept="image/*" style="display:none"></label>
<button class="btn" onclick="addPost()">Post</button>
</div>
<p id="preview" style="display:none"><img id="prevImg" style="width:100%;border-radius:12px;margin-top:10px"></p>
</div>
<div id="feed"></div>
</main>
<script>
let posts = JSON.parse(localStorage.getItem("gelephuV3")||"null") || [
 {user:"karma.wangmo",place:"Gelephu Market",text:"Ema Datshi today! 🌶️🧀 Best in Gelephu! #BhutaneseFood",likes:1247,img:"https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600",liked:false},
 {user:"pema.travels",place:"Gelephu Valley",text:"Sunrise hike ⛰️ Happiness is here in Gelephu! #Gelephu #Bhutan",likes:892,img:"https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600",liked:false}
];
let selectedImage = "";

document.getElementById("file").addEventListener("change", e=>{
 let f=e.target.files[0];
 if(!f)return;
 let r=new FileReader();
 r.onload=ev=>{
  selectedImage=ev.target.result;
  document.getElementById("prevImg").src=selectedImage;
  document.getElementById("preview").style.display="block";
 };
 r.readAsDataURL(f);
});

function render(){
 let h="";
 for(let i=posts.length-1;i>=0;i--){
  let p=posts[i];
  h+=`<div class="post">
   <div class="post-top"><div class="avatar">${p.user[0].toUpperCase()}</div><div><b>@${p.user}</b><br><span class="small">📍 ${p.place}</span></div></div>
   ${p.img?`<img src="${p.img}">`:``}
   <div class="actions"><b onclick="like(${i})">${p.liked?'❤️':'🤍'} ${p.likes}</b> <b>💬</b> <b>✈️</b></div>
   <div class="info"><b>@${p.user}</b> ${p.text}<br><span class="small">just now • Gelephu</span></div>
  </div>`;
 }
 document.getElementById("feed").innerHTML=h;
 localStorage.setItem("gelephuV3",JSON.stringify(posts));
}
function addPost(){
 let v=document.getElementById("txt").value;
 if(!v &&!selectedImage)return;
 posts.push({user:"you",place:"Gelephu, Bhutan",text:v||"Photo from Gelephu!",likes:0,img:selectedImage,liked:false});
 document.getElementById("txt").value=""; selectedImage="";
 document.getElementById("preview").style.display="none";
 render();
}
function like(i){
 posts[i].liked=!posts[i].liked;
 posts[i].likes+=posts[i].liked?1:-1;
 render();
}
render();
</script>
</body>
</html>
