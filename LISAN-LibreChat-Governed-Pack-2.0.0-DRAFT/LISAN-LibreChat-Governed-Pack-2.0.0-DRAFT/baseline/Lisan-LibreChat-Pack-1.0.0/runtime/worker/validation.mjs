/** Strict bounded JSON and the closed JSON-Schema subset used by the pinned contracts. */
export class LisanError extends Error { constructor(code, detail='') { super(code); this.code=code; this.detail=detail; } }
export const fail=(code,detail='')=>{throw new LisanError(code,detail);};
export const canonical=x=>JSON.stringify(x && typeof x==='object' ? Array.isArray(x)?x.map(v=>JSON.parse(canonical(v))):Object.fromEntries(Object.keys(x).sort().map(k=>[k,JSON.parse(canonical(x[k]))])):x);
export const sha=async s=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',typeof s==='string'?new TextEncoder().encode(s):s)),x=>x.toString(16).padStart(2,'0')).join('');
export function strictJSON(text,maxBytes=1048576) {
  if(typeof text!=='string'||new TextEncoder().encode(text).length>maxBytes) fail('REQUEST_TOO_LARGE');
  let i=0,nodes=0;
  const ws=()=>{while(i<text.length&&/[\x20\x09\x0a\x0d]/.test(text[i]))i++;};
  function string(){const start=i++;while(i<text.length){const c=text[i++];if(c==='\\'){i++;continue;}if(c==='"'){let s;try{s=JSON.parse(text.slice(start,i));}catch{fail('INVALID_JSON');}for(const x of s){const cp=x.codePointAt(0);if(cp>=0xd800&&cp<=0xdfff)fail('INVALID_UNICODE');}return s;}if(c<' ')fail('INVALID_JSON');}fail('INVALID_JSON');}
  function value(depth=0){ws();if(depth>48||++nodes>250000)fail('JSON_COMPLEXITY_LIMIT');const c=text[i];
    if(c==='"')return string();
    if(c==='{'||c==='['){i++;ws();const object=c==='{',out=object?{}:[],seen=new Set(),end=object?'}':']';if(text[i]===end){i++;return out;}
      while(i<text.length){ws();let k;if(object){if(text[i]!=='"')fail('INVALID_JSON');k=string();if(seen.has(k))fail('DUPLICATE_JSON_KEY');if(['__proto__','constructor','prototype'].includes(k))fail('UNSAFE_JSON_KEY');seen.add(k);ws();if(text[i++]!==':')fail('INVALID_JSON');}
        const v=value(depth+1);if(object)out[k]=v;else out.push(v);ws();if(text[i]===end){i++;return out;}if(text[i++]!==',')fail('INVALID_JSON');}fail('INVALID_JSON');}
    const tail=text.slice(i);for(const [t,v]of [['true',true],['false',false],['null',null]])if(tail.startsWith(t)){i+=t.length;return v;}
    const m=tail.match(/^-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?/);if(!m)fail('INVALID_JSON');i+=m[0].length;const n=Number(m[0]);if(!Number.isFinite(n))fail('NONFINITE_JSON');return n;
  }
  const out=value();ws();if(i!==text.length)fail('INVALID_JSON');return out;
}
export function shape(v,s,path='$'){
  if(!s)return;
  if(s.const!==undefined&&v!==s.const)fail('INVALID_INPUT',path);
  if(s.enum&&!s.enum.includes(v))fail('INVALID_INPUT',path);
  if(s.type==='object'){
    if(v===null||typeof v!=='object'||Array.isArray(v))fail('INVALID_INPUT',path);
    for(const k of s.required||[])if(!Object.hasOwn(v,k))fail('INVALID_INPUT',path);
    for(const [k,x]of Object.entries(v)){if(!Object.hasOwn(s.properties||{},k)&&s.additionalProperties===false)fail('INVALID_INPUT',path);shape(x,(s.properties||{})[k],`${path}.${k}`);}
  }
  if(s.type==='array'){
    if(!Array.isArray(v)||v.length<(s.minItems??0)||v.length>(s.maxItems??1000000))fail('INVALID_INPUT',path);
    if(s.uniqueItems&&new Set(v.map(canonical)).size!==v.length)fail('INVALID_INPUT',path);
    v.forEach((x,i)=>shape(x,s.items,`${path}[${i}]`));
  }
  if(s.type==='string'){
    if(typeof v!=='string'||[...v].length<(s.minLength??0)||[...v].length>(s.maxLength??1000000))fail('INVALID_INPUT',path);
    if(s.pattern&&!new RegExp(s.pattern,'u').test(v))fail('INVALID_INPUT',path);
    for(const x of v){const cp=x.codePointAt(0);if(cp>=0xd800&&cp<=0xdfff)fail('INVALID_UNICODE');}
  }
  if(s.type==='integer'&&(!Number.isSafeInteger(v)||v<(s.minimum??-Infinity)||v>(s.maximum??Infinity)))fail('INVALID_INPUT',path);
  if(s.type==='boolean'&&typeof v!=='boolean')fail('INVALID_INPUT',path);
}
export const obj=(properties,required=Object.keys(properties))=>({type:'object',properties,required,additionalProperties:false});
export const arr=(items,max=6236,min=0,unique=false)=>({type:'array',items,minItems:min,maxItems:max,uniqueItems:unique});
export const str=(max=8192,min=1)=>({type:'string',minLength:min,maxLength:max});
export const integer=(minimum,maximum)=>({type:'integer',minimum,maximum});
export const refSchema={...str(8,3),pattern:'^[1-9][0-9]{0,2}:[1-9][0-9]{0,3}$'};
export const refsSchema=arr(refSchema,6236,0,true);
export const sortRefs=xs=>[...new Set(xs)].sort((a,b)=>{const x=a.split(':').map(Number),y=b.split(':').map(Number);for(let i=0;i<Math.max(x.length,y.length);i++){if((x[i]||0)!==(y[i]||0))return(x[i]||0)-(y[i]||0);}return 0;});
