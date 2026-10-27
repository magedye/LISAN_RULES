#!/usr/bin/env node
/** Local stdio transport ONLY. This does not run a local process in ChatGPT Web. */
import {Protocol} from '../worker/protocol.mjs';
import {strictJSON} from '../worker/validation.mjs';
const protocol=new Protocol(),session={state:'NEW'},decoder=new TextDecoder('utf-8',{fatal:true});let buffer='',queue=Promise.resolve(),discard=false;
const send=x=>{if(x!==null)process.stdout.write(JSON.stringify(x)+'\n');};
process.stdin.on('data',bytes=>{
  try{buffer+=decoder.decode(bytes,{stream:true});}catch{send({jsonrpc:'2.0',id:null,error:{code:-32700,message:'INVALID_UTF8'}});buffer='';return;}
  while(buffer.includes('\n')){const at=buffer.indexOf('\n'),line=buffer.slice(0,at);buffer=buffer.slice(at+1);if(discard){discard=false;continue;}if(!line.trim())continue;
    queue=queue.then(async()=>{try{const req=strictJSON(line);send(await protocol.handle(req,'local-process-owner',{transport:'stdio',session}));}catch(error){send({jsonrpc:'2.0',id:null,error:{code:-32700,message:error.code||'INVALID_JSON'}});}});
  }
  if(Buffer.byteLength(buffer)>1048576){buffer='';discard=true;send({jsonrpc:'2.0',id:null,error:{code:-32700,message:'REQUEST_TOO_LARGE'}});}
});
process.stdin.on('end',()=>{if(buffer.trim())send({jsonrpc:'2.0',id:null,error:{code:-32700,message:'NEWLINE_TERMINATOR_REQUIRED'}});});
