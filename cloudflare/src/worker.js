const json=(body,status=200,headers={})=>new Response(JSON.stringify(body),{status,headers:{"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store",...headers}});
const hex=async value=>Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(value)))).map(x=>x.toString(16).padStart(2,"0")).join("");
const clean=(v,max)=>typeof v==="string"?v.trim().slice(0,max):"";
export default {async fetch(request,env){
 const origin=request.headers.get("Origin")||"";
 const allowed=(env.ALLOWED_ORIGIN||"https://ri0115.github.io").split(",").map(x=>x.trim());
 const cors=allowed.includes(origin)?{"Access-Control-Allow-Origin":origin,"Vary":"Origin","Access-Control-Allow-Methods":"GET,POST,OPTIONS","Access-Control-Allow-Headers":"Content-Type,X-Admin-Key"}:{};
 if(request.method==="OPTIONS")return new Response(null,{status:204,headers:cors});
 const url=new URL(request.url),path=url.pathname;
 if(origin&&!allowed.includes(origin))return json({error:"Origin not allowed"},403,cors);
 if(!env.DB)return json({error:"D1 binding missing"},503,cors);
 try{
 if(path==="/api/visits"&&request.method==="POST"){
   const ip=request.headers.get("CF-Connecting-IP")||"unknown",ua=request.headers.get("User-Agent")||"";
   const day=new Date().toISOString().slice(0,10);
   const hash=await hex((env.HASH_SALT||"")+":"+ip+":"+ua);
   const inserted=await env.DB.prepare("INSERT OR IGNORE INTO visitor_days(token_hash,day) VALUES (?,?)").bind(hash,day).run();
   const counted=(inserted.meta?.changes||0)>0;
   if(counted)await env.DB.prepare("UPDATE counters SET value=value+1 WHERE key='visits'").run();
   const row=await env.DB.prepare("SELECT value FROM counters WHERE key='visits'").first();
   return json({count:row?.value||0,counted,definition:"unique device/network fingerprint per UTC day (approximate)"},200,cors);
 }
 if(path==="/api/visits"&&request.method==="GET"){
   const row=await env.DB.prepare("SELECT value FROM counters WHERE key='visits'").first();
   return json({count:row?.value||0},200,cors);
 }
 if(path==="/api/posts"&&request.method==="GET"){
   const page=Math.min(100,Math.max(1,Number(url.searchParams.get("limit"))||30));
   const rows=await env.DB.prepare("SELECT id,nickname,message,parent_id,created_at FROM posts WHERE hidden=0 ORDER BY id DESC LIMIT ?").bind(page).all();
   return json({posts:rows.results||[]},200,cors);
 }
 if(path==="/api/posts"&&request.method==="POST"){
   if(Number(request.headers.get("Content-Length")||0)>4096)return json({error:"Too large"},413,cors);
   const body=await request.json().catch(()=>null);
   const nickname=clean(body?.nickname,24),message=clean(body?.message,500);
   const parent=body?.parent_id==null?null:Number(body.parent_id);
   if(!nickname||!message||nickname.length>24||message.length>500||/https?:\/\/|www\./i.test(message))return json({error:"名前と本文を入力してください。URL投稿は不可です。"},400,cors);
   if(parent!==null&&(!Number.isSafeInteger(parent)||parent<1))return json({error:"Invalid reply"},400,cors);
   if(parent!==null){const found=await env.DB.prepare("SELECT id FROM posts WHERE id=? AND hidden=0").bind(parent).first();if(!found)return json({error:"Reply target missing"},404,cors);}
   const ip=request.headers.get("CF-Connecting-IP")||"unknown",hash=await hex((env.HASH_SALT||"")+":bbs:"+ip),now=Date.now();
   const prev=await env.DB.prepare("SELECT last_post_ms FROM post_limits WHERE token_hash=?").bind(hash).first();
   if(prev&&now-prev.last_post_ms<120000)return json({error:"投稿は2分間隔でお願いします。"},429,cors);
   // D1 batch runs atomically; the post and throttle record are committed together.
   await env.DB.batch([
     env.DB.prepare("INSERT INTO posts(nickname,message,parent_id) VALUES (?,?,?)").bind(nickname,message,parent),
     env.DB.prepare("INSERT INTO post_limits(token_hash,last_post_ms) VALUES (?,?) ON CONFLICT(token_hash) DO UPDATE SET last_post_ms=excluded.last_post_ms").bind(hash,now)
   ]);
   return json({ok:true},201,cors);
 }
 if(path.startsWith("/api/admin/posts/")&&request.method==="POST"){
   if(!env.ADMIN_KEY||request.headers.get("X-Admin-Key")!==env.ADMIN_KEY)return json({error:"Unauthorized"},401,cors);
   const id=Number(path.split("/").pop());
   if(!Number.isSafeInteger(id)||id<1)return json({error:"Invalid id"},400,cors);
   await env.DB.prepare("UPDATE posts SET hidden=1 WHERE id=?").bind(id).run();
   return json({ok:true},200,cors);
 }
 return json({error:"Not found"},404,cors);
 }catch(e){return json({error:"Request failed"},500,cors);}
}};
