/** Native Fetch handler. Deployment needs a qualified HOST-supplied authenticator.
No model argument, HTTP identity header, UI mode, or unsigned actor is trusted.
The default export FAILS CLOSED until actual host integration and ACL proof exist.
*/
import {Protocol} from './protocol.mjs';
import {strictJSON} from './validation.mjs';
const baseHeaders={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','X-Frame-Options':'DENY'};
function response(code,status){return Response.json({status},{status:code,headers:baseHeaders});}
export function createApplication({authenticate,allowedOrigin,protocol=new Protocol(),bodyTimeoutMs=5000,maxConcurrent=2}={}){
  let inFlight=0;
  return async function fetchHandler(request){
    if(typeof authenticate!=='function'||!allowedOrigin)return response(503,'BLOCKED_HOST_IDENTITY_NOT_QUALIFIED');
    const url=new URL(request.url),origin=request.headers.get('origin');
    if(url.origin!==allowedOrigin||(origin&&origin!==allowedOrigin))return response(403,'ORIGIN_NOT_ALLOWED');
    if(url.pathname!=='/mcp'&&url.pathname!=='/api/research')return response(404,'NOT_FOUND');
    let principal;try{principal=await authenticate(request);}catch{return response(401,'AUTHENTICATION_REQUIRED');}
    if(!principal?.subject||principal?.owner!==true||principal?.scope!=='research:read')return response(403,'ACCESS_DENIED');
    if(request.method!=='POST')return response(405,'METHOD_NOT_ALLOWED');
    if(!(request.headers.get('content-type')||'').startsWith('application/json'))return response(415,'JSON_REQUIRED');
    const size=request.headers.get('content-length');if(size&&(!/^\d+$/.test(size)||Number(size)>1048576))return response(413,'REQUEST_TOO_LARGE');
    if(inFlight>=maxConcurrent)return response(429,'REQUEST_BUDGET_EXCEEDED');inFlight++;
    let timer,reader;
    try{
      const read=async()=>{reader=request.body?.getReader();if(!reader)return '';let count=0,chunks=[];try{while(true){const {done,value}=await reader.read();if(done)break;count+=value.byteLength;if(count>1048576)throw Object.assign(new Error(),{code:'REQUEST_TOO_LARGE'});chunks.push(value);}const all=new Uint8Array(count);let p=0;for(const x of chunks){all.set(x,p);p+=x.byteLength;}return new TextDecoder('utf-8',{fatal:true}).decode(all);}finally{reader.cancel().catch(()=>{});}};
      const body=await Promise.race([read(),new Promise((_,reject)=>{timer=setTimeout(()=>{reject(Object.assign(new Error(),{code:'REQUEST_TIMEOUT'}));reader?.cancel().catch(()=>{});},bodyTimeoutMs);})]);
      const parsed=strictJSON(body);let rpc=parsed;
      if(url.pathname==='/api/research'){
        if(Object.keys(parsed).some(k=>!['tool','arguments'].includes(k))||typeof parsed.tool!=='string')return response(400,'INVALID_INPUT');
        rpc={jsonrpc:'2.0',id:1,method:'tools/call',params:{name:parsed.tool,arguments:parsed.arguments??{},_meta:{protocolVersion:'2026-07-28',clientCapabilities:{}}}};
      }
      const output=await protocol.handle(rpc,principal.subject,{transport:'http',versionHeader:request.headers.get('MCP-Protocol-Version')});
      if(output===null)return new Response(null,{status:202,headers:baseHeaders});
      return Response.json(output,{headers:baseHeaders});
    }catch(error){return response(error.code==='REQUEST_TOO_LARGE'?413:error.code==='REQUEST_TIMEOUT'?408:400,error.code||'INVALID_REQUEST');}
    finally{clearTimeout(timer);reader?.cancel().catch(()=>{});inFlight--;}
  };
}
export default {fetch:async()=>response(503,'BLOCKED_HOST_IDENTITY_AND_OWNER_ONLY_ACL_NOT_QUALIFIED')};
