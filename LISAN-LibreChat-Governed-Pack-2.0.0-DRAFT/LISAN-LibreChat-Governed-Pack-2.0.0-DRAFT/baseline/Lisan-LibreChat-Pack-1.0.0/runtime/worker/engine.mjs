/** New native Worker port of the archived Python 2.0.0 semantics, NOT recovered Site code. */
import data from './data.mjs';
import {QAC_PROJECTION_SHA256} from './derived_pins.mjs';
import {LisanError,fail,shape,sha,canonical,strictJSON,sortRefs} from './validation.mjs';
export const VERSION='1.1.0-candidate.1';
// Immutable trust roots are independent of tool arguments AND generated data.
export const PINS=Object.freeze({corpus:'0ae05c1b6c08196b86ea53d166f10e8558e844a37678043730dc7f60ecc09afa',manifest:'18414a12e558f02bed93e6396d0a78ef7af5e6c8a34275ec773b8509010b6e8c',source:'25c0c77928fe362cbabb7a14b63389b00850e06ff6c8ed33a5e12f9e7a1ad2da',qac:'a1d12923815341face765083805d2148ed2d9f5cc3f7d6665219d887675d8c46'});
const marks=/[\u0610-\u061A\u0640\u064B-\u0652\u0656-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E4\u06E7-\u06E8\u06EA-\u06ED]/gu;
export function normalize(text,profile){if(profile==='EXACT')return text;if(profile==='ARABIC_MARKS_V1')return text.normalize('NFC').replace(marks,'');fail('INVALID_INPUT');}
export class Engine {
  #loaded; #qacLoaded; #raw; #byRef=new Map(); #verses=[]; #manifest; #qac; #searchCache=new Map();
  constructor(raw=data){this.#raw=raw;} // Test/build injection only: no tool exposes this constructor.
  get catalog(){return data.tool_catalog;}
  get schemas(){return data.tool_inputs;}
  async ready(){if(!this.#loaded)this.#loaded=this.#load();return this.#loaded;}
  async #load(){
    for(const [field,pin,code]of [['manifest_raw',PINS.manifest,'MANIFEST_HASH_MISMATCH'],['corpus_raw',PINS.corpus,'CORPUS_HASH_MISMATCH'],['source_raw',PINS.source,'SOURCE_HASH_MISMATCH']]){
      if(typeof this.#raw[field]!=='string')fail('BLOCKED_CORPUS_UNAVAILABLE');if(await sha(this.#raw[field])!==pin)fail(code);
    }
    this.#manifest=strictJSON(this.#raw.manifest_raw,262144);
    const corpus=strictJSON(this.#raw.corpus_raw,16777216);
    if(corpus.corpus_id!=='tanzil-uthmani-v1.1'||this.#manifest.canonical_sha256!==PINS.corpus||this.#manifest.version!=='Tanzil-Uthmani-1.1'||this.#manifest.status!=='APPROVED')fail('APPROVED_PROFILE_MISMATCH');
    const counts=this.#manifest.expected_ayah_counts;
    if(!Array.isArray(counts)||counts.length!==114||corpus.verses?.length!==6236)fail('CORPUS_LAYOUT_MISMATCH');
    let i=0;
    for(let s=1;s<=114;s++){const row=counts[s-1];if(row.surah_id!==s)fail('CORPUS_LAYOUT_MISMATCH');for(let a=1;a<=row.ayah_count;a++){
      const v=corpus.verses[i++];if(!v||v.surah_id!==s||v.ayah_id!==a||typeof v.text!=='string'||!v.text.trim())fail('CORPUS_LAYOUT_MISMATCH');
      const result=Object.freeze({ref:`${s}:${a}`,original_text:v.text,surah:s,ayah:a});this.#verses.push(result);this.#byRef.set(result.ref,result);
    }}if(i!==6236)fail('CORPUS_LAYOUT_MISMATCH');return true;
  }
  provenance(){return {corpus_id:'tanzil-uthmani-v1.1',corpus_version:'Tanzil-Uthmani-1.1',corpus_sha256:PINS.corpus,manifest_sha256:PINS.manifest,source_original_sha256:PINS.source,engine_version:VERSION,original_source_authenticity:'OWNER_ATTESTED_NOT_AUTOMATICALLY_PROVEN'};}
  async verse(ref){await this.ready();if(!/^[1-9][0-9]{0,2}:[1-9][0-9]{0,3}$/.test(ref)||Number(ref.split(':')[0])>114)fail('INVALID_REFERENCE');if(!this.#byRef.has(ref))fail('REFERENCE_NOT_FOUND');return this.#byRef.get(ref);}
  async call(name,args={}){
    if(!Object.hasOwn(this.schemas,name))fail('UNKNOWN_TOOL');shape(args,this.schemas[name]);
    try{await this.ready();}catch(e){if(name==='lisan_status')return {status:e.code||'BLOCKED_CORPUS_UNAVAILABLE',ready:false,message:'Pinned source unavailable or changed.',engine_version:VERSION};throw e;}
    if(name==='lisan_status')return {status:'READY_FOR_CORPUS_OPERATIONS',ready:true,provenance:this.provenance(),record_count:6236,source:this.#manifest.source,semantic_release_accepted:false};
    if(name==='lisan_search')return this.search(args.query,args.offset??0,args.limit??20);
    if(name==='lisan_get_verses')return this.get(args.refs,args.context??0);
    if(name==='lisan_verify_quote')return this.quote(args.ref,args.text,args.kind);
    if(name==='lisan_validate_analysis')return this.validate(args.record);
  }
  async scan(query){
    shape({query},this.schemas.lisan_search);await this.ready();
    const forms=[...new Set(query.forms.map(f=>normalize(f,query.normalization)))].sort();
    if(forms.some(f=>!f.trim()))fail('EMPTY_NORMALIZED_QUERY');
    if(query.match==='TOKEN'&&forms.some(f=>f.trim()!==f||f.split(/\s+/u).length!==1))fail('INVALID_INPUT');
    const effective={...query,forms},key=canonical(effective);
    if(this.#searchCache.has(key))return this.#searchCache.get(key);
    const found=[];let total=0;
    for(const v of this.#verses){const t=normalize(v.original_text,query.normalization);const tokens=query.match==='TOKEN'?t.trim().split(/\s+/u):null,counts={};
      for(const f of forms){let n=0;if(tokens){for(const token of tokens)if(token===f)n++;}else {let at=0;while((at=t.indexOf(f,at))!==-1){n++;at+=f.length;}}if(n)counts[f]=n;}
      const n=Object.values(counts).reduce((a,b)=>a+b,0);if(n){found.push({ref:v.ref,original_text:v.original_text,form_counts:counts,match_events:n});total+=n;}}
    const result={found,total,effective,fingerprint:await sha(canonical({corpus_sha256:PINS.corpus,engine_version:VERSION,query:effective}))};
    // Bounded cache contains corpus-derived literal results only; never drafts or user identity.
    if(this.#searchCache.size>=16)this.#searchCache.delete(this.#searchCache.keys().next().value);this.#searchCache.set(key,result);return result;
  }
  async search(query,offset=0,limit=20){
    shape({query,offset,limit},this.schemas.lisan_search);const {found,total,effective,fingerprint}=await this.scan(query),selected=found.slice(offset,offset+limit);
    return {status:'OK',provenance:this.provenance(),query:structuredClone(query),effective_query:effective,query_fingerprint:fingerprint,
      scan:'COMPLETE_FOR_DECLARED_QUERY',semantic_coverage:'NOT_ESTABLISHED',analysis_coverage:'NOT_MEASURED',scanned_verses:6236,
      matched_verses:found.length,match_events:total,count_definition:'TOKEN: whitespace tokens; SUBSTRING: non-overlapping matches per form; different forms count independently.',
      page:{offset,limit,returned:selected.length,all_matches_returned:offset===0&&selected.length===found.length,next_offset:offset+selected.length<found.length?offset+selected.length:null},occurrences:structuredClone(selected)};
  }
  async get(refs,context=0){
    shape({refs,context},this.schemas.lisan_get_verses);await this.ready();const wanted=new Set();
    for(const ref of refs){const v=await this.verse(ref);for(let a=Math.max(1,v.ayah-context);a<=v.ayah+context;a++)if(this.#byRef.has(`${v.surah}:${a}`))wanted.add(`${v.surah}:${a}`);}
    if(wanted.size>200)fail('RESULT_TOO_LARGE');return {status:'OK',provenance:this.provenance(),verses:sortRefs([...wanted]).map(ref=>({ref,original_text:this.#byRef.get(ref).original_text,requested:refs.includes(ref)})),scope:'REQUESTED_REFERENCES_AND_WITHIN_SURAH_CONTEXT'};
  }
  async quote(ref,text,kind){shape({ref,text,kind},this.schemas.lisan_verify_quote);const v=await this.verse(ref);const matched=kind==='FULL'?v.original_text===text:v.original_text.includes(text);return {status:matched?'QUOTE_EXACT_MATCH':'QUOTE_NOT_VERIFIED',ref,kind,matched,comparison:'EXACT_ORIGINAL_CODEPOINTS',provenance:this.provenance(),semantic_validity:'NOT_ASSESSED'};}
  async validate(record){
    shape({record},this.schemas.lisan_validate_analysis);await this.ready();const errors=[],seen=new Set(),counts=new Map();const bad=(code,claim_id=null)=>errors.push({code,claim_id});
    if(record.corpus_sha256!==PINS.corpus)bad('ANALYSIS_CORPUS_MISMATCH');
    for(const c of record.claims){if(seen.has(c.id))bad('DUPLICATE_CLAIM_ID',c.id);seen.add(c.id);
      for(const e of c.evidence){try{if(!(await this.quote(e.ref,e.text,e.kind)).matched)bad('QUOTE_NOT_VERIFIED',c.id);}catch(e){bad(e.code||'INVALID_INPUT',c.id);}}
      if(c.kind!=='COUNT'&&!c.evidence.length)bad('EVIDENCE_REQUIRED',c.id);
      if(c.kind==='DIRECT_TEXT'){if(c.evidence.length!==1||c.statement!==c.evidence[0].text)bad('DIRECT_TEXT_MUST_EQUAL_QUOTE',c.id);}
      else if(c.kind!=='COUNT'&&!c.warrant.trim())bad('WARRANT_REQUIRED',c.id);
      if(c.kind==='COUNT'){if(!c.count)bad('COUNT_SPEC_REQUIRED',c.id);else try{const k=canonical(c.count.query);if(!counts.has(k)){if(counts.size>=16)fail('COUNT_QUERY_BUDGET_EXCEEDED');counts.set(k,await this.scan(c.count.query));}const r=counts.get(k),n=c.count.unit==='VERSES'?r.found.length:r.total;if(n!==c.count.value)bad('FALSE_COUNT',c.id);}catch(e){bad(e.code||'INVALID_INPUT',c.id);}}
      else if(c.count)bad('COUNT_FIELD_ON_NON_COUNT_CLAIM',c.id);
    }
    return {status:errors.length?'MECHANICAL_FAIL':'MECHANICAL_PASS',provenance:this.provenance(),checked_claims:record.claims.length,errors,semantic_status:'NOT_ASSESSED',external_influence_status:'NOT_DETERMINABLE',publication_status:'NOT_RELEASE_ACCEPTANCE',limitations:['Quote identity does not establish semantic entailment.','Free-text statements and warrants need methodological review.','Counts cover only the declared query, not roots or all relevant meanings.','A successful check is not proof of absence of training-data influence.']};
  }
  async qac(){if(!this.#qacLoaded)this.#qacLoaded=this.#loadQac();return this.#qacLoaded;}
  async #loadQac(){await this.ready();if(!this.#raw.qac_raw)fail('BLOCKED_QAC_UNAVAILABLE');if(this.#raw.qac_sha256!==QAC_PROJECTION_SHA256||await sha(this.#raw.qac_raw)!==QAC_PROJECTION_SHA256)fail('QAC_PROJECTION_HASH_MISMATCH');
    // A generated projection is a derived build artifact, not a second textual authority.
    const q=JSON.parse(this.#raw.qac_raw);if(q.source_sha256!==PINS.qac||q.target_corpus_sha256!==PINS.corpus||q.role!=='STRUCTURAL_CANDIDATE_ONLY')fail('QAC_PROVENANCE_MISMATCH');
    const roots=new Map(),lemmas=new Map(),words=new Map(),seen=new Set();
    for(const row of q.rows){const [ref,surface,pos,root,lemma,form,features]=row;if(!/^\d+:\d+:\d+:\d+$/.test(ref)||seen.has(ref))fail('QAC_DUPLICATE_OR_INVALID_REF');seen.add(ref);
      const parts=ref.split(':'),vr=parts.slice(0,2).join(':'),wr=parts.slice(0,3).join(':');if(!this.#byRef.has(vr))fail('QAC_INVALID_VERSE');
      if(features.some(f=>/^(GLOSS|MEANING|TRANSLATION|SEMANTIC_LABEL|ENGLISH|ENG):/i.test(f)))fail('QAC_EXTERNAL_FIELD');
      const r={segment_ref:ref,word_ref:wr,verse_ref:vr,surface_buckwalter:surface,pos,root_buckwalter:root,lemma_buckwalter:lemma,verb_form:form,features};
      for(const [map,key]of [[roots,root],[lemmas,lemma],[words,wr]])if(key){if(!map.has(key))map.set(key,[]);map.get(key).push(r);}}
    if(q.rows.length!==128219||seen.size!==128219||words.size!==77429||roots.size!==1642||[...roots.values()].reduce((n,x)=>n+x.length,0)!==49968)fail('QAC_COVERAGE_MISMATCH');
    this.#qac={...q,roots,lemmas,words};return this.#qac;
  }
  async structural(spec,offset=0,limit=20){
    const q=await this.qac();let rows;if(spec.kind==='ROOT'){const root=arabicRootToBW(spec.value);rows=q.roots.get(root)||[];}else if(spec.kind==='LEMMA')rows=q.lemmas.get(spec.value)||[];else rows=q.words.get(spec.value)||[];
    if(spec.pos)rows=rows.filter(r=>r.pos===spec.pos);
    const selected=rows.slice(offset,offset+limit),wordrefs=sortRefs(rows.map(x=>x.word_ref)),verserefs=sortRefs(rows.map(x=>x.verse_ref));
    return {status:'OK',query:structuredClone(spec),query_fingerprint:await sha(canonical({spec,source:PINS.qac,projection:this.#raw.qac_sha256})),
      structural_source:{source_sha256:PINS.qac,projection_sha256:this.#raw.qac_sha256,version:'0.4',authority:'STRUCTURAL_CANDIDATE_ONLY',target_corpus_sha256:PINS.corpus},
      counts:{segments:rows.length,words:wordrefs.length,verses:verserefs.length,pos:Object.fromEntries([...new Set(rows.map(x=>x.pos))].map(p=>[p,rows.filter(x=>x.pos===p).length]))},
      matched_refs:verserefs,all_segment_refs:rows.map(r=>r.segment_ref),all_word_refs:wordrefs,
      page:{offset,limit,returned:selected.length,next_offset:offset+selected.length<rows.length?offset+selected.length:null},
      occurrences:selected.map(r=>{const alignment=q.alignment[r.word_ref]||{status:'WORD_ALIGNMENT_UNRESOLVED',target_spans:[]},text=this.#byRef.get(r.verse_ref).original_text;
        return {...r,alignment,canonical_word_excerpts:alignment.target_spans.map(([s,e])=>[...text].slice(s,e).join('')),original_text:text};}),
      index_coverage:'COMPLETE_FOR_PINNED_QAC_QUERY',semantic_coverage:'NOT_ESTABLISHED',syntax_tree_available:false};
  }
}
const BW="'|>&<}AbptvjHxd*rzs$SDTZEgfqklmnhwyY{";
const AR=['ء','آ','أ','ؤ','إ','ئ','ا','ب','ة','ت','ث','ج','ح','خ','د','ذ','ر','ز','س','ش','ص','ض','ط','ظ','ع','غ','ف','ق','ك','ل','م','ن','ه','و','ي','ى','ٱ'];
const reverse=new Map(AR.map((c,i)=>[c,BW[i]]));
export function arabicRootToBW(s){return [...s.replace(/[\sـ]/gu,'')].map(c=>reverse.get(c)||c).join('');}
export default new Engine();
