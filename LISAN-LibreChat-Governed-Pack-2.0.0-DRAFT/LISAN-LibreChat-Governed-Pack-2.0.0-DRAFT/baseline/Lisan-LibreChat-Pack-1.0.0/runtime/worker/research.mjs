/** Research routing and additive records. Research judgments remain human/host proposals. */
import engineDefault,{PINS,VERSION} from './engine.mjs';
import data from './data.mjs';
import {shape,fail,obj,arr,str,integer,refSchema,refsSchema,sortRefs,canonical,sha,strictJSON} from './validation.mjs';
export const MODES=['METHOD','LOCAL_CONTEXT','OCCURRENCES','STUDY','COMPARE','HYPOTHESIS','VERIFY'];
const querySchema=data.tool_inputs.lisan_search.properties.query;
const quote=data.tool_inputs.lisan_validate_analysis.properties.record.properties.claims.items.properties.evidence.items;
export const structuralSchema=obj({kind:{enum:['ROOT','LEMMA','WORD']},value:str(128),pos:str(16)},['kind','value']);
const boundedRefs=arr(refSchema,6236,0,true);
const layerSchema=obj({layer_id:integer(1,30),reason:str(2048),status:{enum:['SELECTED','ANALYZED','NOT_APPLICABLE']},observation:str(8192,0),evidence_refs:boundedRefs},['layer_id','reason','status','evidence_refs']);
const hypothesisSchema=obj({id:str(64),statement:str(),warrant:str(8192,0),supporting_refs:boundedRefs,counter_refs:boundedRefs,falsification_condition:str(),state:{enum:['PROPOSED','PREFERRED','REJECTED','UNRESOLVED']}},['id','statement','warrant','supporting_refs','counter_refs','falsification_condition','state']);
const contributionSchema=obj({layer_id:integer(1,30),component:str(2048),evidence:quote,warrant:str()});
const dimensionSchema=obj({claim_id:str(64),claim_scope:{enum:['LOCAL_MEANING','FORM_USAGE','ROOT_CORE','COUNT','TEXTUAL_OBSERVATION','COMPARISON']},layer_contributions:arr(contributionSchema,30),scope_refs:boundedRefs,limitations:arr(str(4096),50)});
const counterSchema=obj({hypothesis_id:str(64),ref:refSchema,observation:str(),warrant:str(),outcome:{enum:['SUPPORTS','COUNTERS','LIMITS','UNRESOLVED']}});
export const STUDY_SCHEMA=obj({schema_version:{const:'quran-lisan-study/1'},study_id:str(128),question:str(),mode:{enum:MODES},corpus:obj({corpus_id:str(128),corpus_version:str(128),corpus_sha256:str(64,64),manifest_sha256:str(64,64),source_original_sha256:str(64,64),engine_version:str(128),original_source_authenticity:str(128)}),
  selectors:arr(obj({query:querySchema,structural_query:structuralSchema,refs:arr(refSchema,50,1,true),context:integer(0,5)},[]),2),
  record:data.tool_inputs.lisan_validate_analysis.properties.record,
  retrieved_refs:boundedRefs,analyzed_refs:boundedRefs,remaining_refs:boundedRefs,receipts:arr(str(200000),256),
  selected_layers:arr(layerSchema,30),hypotheses:arr(hypothesisSchema,30),claim_dimensions:arr(dimensionSchema,100),counter_tests:arr(counterSchema,200),
  dependencies:arr(obj({parent_id:str(128),child_id:str(128),reason:str(2048)}),200),
  reopen_events:arr(obj({reason:str(),affected_ids:arr(str(128),200),previous_digest:str(64,64)}),100),
  research_state:{enum:['UNRESOLVED','PREFERRED','REJECTED']},semantic_review:{const:'NOT_REVIEWED'},release_acceptance:{const:'NOT_GRANTED'},
  provider_kind:{enum:['HUMAN_OR_HOST_UNVERIFIED','TEST_MOCK']},
  historical_context:arr(obj({source_label:str(256),source_sha256:str(64,64),native_states:{type:'object',additionalProperties:true},raw_record:{},reuse_state:{const:'HYPOTHESIS_ONLY_REVALIDATION_REQUIRED'},quarantined:{type:'boolean'},old_evidence:arr(quote,200)}),50)
});
export const PREPARE_SCHEMA=obj({question:str(),mode:{enum:MODES},query:querySchema,refs:arr(refSchema,50,1,true),comparison_queries:arr(querySchema,2,2),structural_query:structuralSchema,
  context:integer(0,5),offset:integer(0,20000),limit:integer(1,50),count_unit:{enum:['VERSES','MATCH_EVENTS']},resume_receipt:str(200000),selected_layers:arr(integer(1,30),30,0,true)},['question']);
export const CHECK_SCHEMA=obj({record:data.tool_inputs.lisan_validate_analysis.properties.record,study:STUDY_SCHEMA,
  retrieved_refs:boundedRefs,analyzed_refs:boundedRefs,counter_evidence_refs:boundedRefs,query:querySchema,receipts:arr(str(200000),256),
  import_history:obj({source_label:str(256),native_states:{type:'object',additionalProperties:true},raw_record:{},refs:arr(refSchema,50,0,true)},['source_label','native_states','raw_record'])},[]);
function b64(b){return btoa(String.fromCharCode(...b)).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');}
function unb64(s){try{return Uint8Array.from(atob(s.replace(/-/g,'+').replace(/_/g,'/')),c=>c.charCodeAt(0));}catch{fail('INVALID_RECEIPT');}}
export class Receipts {
  #key; constructor(keyBytes=crypto.getRandomValues(new Uint8Array(32)),clock=()=>Date.now()){this.#key=crypto.subtle.importKey('raw',keyBytes,{name:'HMAC',hash:'SHA-256'},false,['sign','verify']);this.clock=clock;}
  async issue(subject,payload){if(!subject)fail('AUTHENTICATION_REQUIRED');const body={...payload,corpus_sha256:PINS.corpus,version:VERSION,subject_digest:await sha(subject),issued_at:this.clock(),expires_at:this.clock()+3600000};
    const bytes=new TextEncoder().encode(canonical(body));return b64(bytes)+'.'+b64(new Uint8Array(await crypto.subtle.sign('HMAC',await this.#key,bytes)));}
  async read(subject,token){if(typeof token!=='string'||token.length>200000)fail('INVALID_RECEIPT');const parts=token.split('.');if(parts.length!==2)fail('INVALID_RECEIPT');const bytes=unb64(parts[0]);
    if(!(await crypto.subtle.verify('HMAC',await this.#key,unb64(parts[1]),bytes)))fail('INVALID_RECEIPT');const p=strictJSON(new TextDecoder('utf-8',{fatal:true}).decode(bytes),200000);
    if(p.subject_digest!==await sha(subject))fail('RECEIPT_OWNER_MISMATCH');if(p.corpus_sha256!==PINS.corpus||p.version!==VERSION)fail('RECEIPT_VERSION_MISMATCH');if(p.expires_at<this.clock()||p.issued_at>this.clock())fail('RECEIPT_EXPIRED');return p;}
}
export function route(a){
  if(a.mode)return {mode:a.mode,basis:'EXPLICIT_USER_OR_HOST_MODE',assumptions:[]};
  const q=a.question;
  if(/شرح.*(?:منهج|QURAN_INTERNAL_STRICT)|ما.*المنهج|اشرح.*(?:منهج|سياسة)/iu.test(q))return {mode:'METHOD',basis:'RULE_SUGGESTION',assumptions:[]};
  if(a.comparison_queries||/قارن|الفرق بين/u.test(q))return {mode:'COMPARE',basis:'RULE_SUGGESTION',assumptions:[]};
  if(a.refs||/[1-9]\d{0,2}:[1-9]\d{0,3}/u.test(q))return {mode:'LOCAL_CONTEXT',basis:'RULE_SUGGESTION',assumptions:[]};
  if(/تحقق|دقق|راجع الاقتباس/u.test(q))return {mode:'VERIFY',basis:'RULE_SUGGESTION',assumptions:[]};
  if(/فرضية|اثبت|أثبت|انقض/u.test(q))return {mode:'HYPOTHESIS',basis:'RULE_SUGGESTION',assumptions:[]};
  if(/كم|عدّ|مواضع|مرات/u.test(q))return {mode:'OCCURRENCES',basis:'RULE_SUGGESTION',assumptions:[]};
  return {mode:'STUDY',basis:'RULE_SUGGESTION',assumptions:['استُخدم مسار الدراسة؛ لم يُفترض معنى أو جذر من السؤال.']};
}
export const METHOD_SUMMARY={protocol:'QURAN_INTERNAL_STRICT',primary_semantic_evidence:'PINNED_ARABIC_QURAN_ONLY',
  public_reasoning:'السؤال ← شواهد مسترجعة ← ملاحظات وفرضيات ← اعتراضات واختبار نقض ← نتيجة مقيدة قابلة للمراجعة.',
  excluded:'لا تفسير أو معجم أو رواية أو ترجمة أو دراسة سابقة حجة دلالية صريحة أو خفية.',
  qualifications:'الفحص الآلي لا يثبت صحة المعنى، ولا محو معرفة التدريب، ولا قبول الإصدار.',
  no_forced_assumptions:'لا إلزام عام بالتجميد أو وحدة الجذر أو الترادف أو نفيه أو معنى حرف ثابت.'};
export class Research {
  constructor(engine=engineDefault,receipts=new Receipts()){this.engine=engine;this.receipts=receipts;}
  get catalog(){return [...this.engine.catalog,{name:'lisan_prepare_research',description:'Route a Quran-internal research question, retrieve actual pinned evidence, explicit structural candidates and owner-bound retrieval receipts. Does not generate or accept meanings.',inputSchema:PREPARE_SCHEMA,annotations:{readOnlyHint:true,destructiveHint:false,idempotentHint:false,openWorldHint:false}},
  {name:'lisan_check_study',description:'Check legacy 2.0 claims and additive research records; re-fetch historical references without inheriting acceptance. Mechanical and methodological completeness only, not semantic truth.',inputSchema:CHECK_SCHEMA,annotations:{readOnlyHint:true,destructiveHint:false,idempotentHint:true,openWorldHint:false}}];}
  async call(name,args,subject){if(!subject)fail('AUTHENTICATION_REQUIRED');if(name==='lisan_prepare_research')return this.prepare(args,subject);if(name==='lisan_check_study')return this.check(args,subject);return this.engine.call(name,args);}
  async prepare(args,subject){shape(args,PREPARE_SCHEMA);let a=structuredClone(args),routing=route(a),prior=null;
    if(a.resume_receipt){prior=await this.receipts.read(subject,a.resume_receipt);if(prior.next_offset===null)fail('NO_REMAINING_PAGE');
      if(a.query&&canonical(a.query)!==canonical(prior.selector.query)||a.structural_query&&canonical(a.structural_query)!==canonical(prior.selector.structural_query)||a.refs&&canonical(a.refs)!==canonical(prior.selector.refs)||a.comparison_queries)fail('CONTINUATION_QUERY_CONFLICT');
      if(a.mode&&a.mode!==prior.mode)fail('CONTINUATION_MODE_CONFLICT');a={...a,...prior.selector,offset:prior.next_offset,limit:a.limit??prior.limit,mode:prior.mode};routing={mode:prior.mode,basis:'VERIFIED_CONTINUATION_RECEIPT',assumptions:[]};}
    const mode=routing.mode;
    const supplied=['query','structural_query','refs','comparison_queries'].filter(k=>a[k]!==undefined);
    if(!['METHOD','VERIFY'].includes(mode)&&supplied.length>1)fail('AMBIGUOUS_QUERY_KIND');
    if(!prior&&!['METHOD','VERIFY'].includes(mode)&&((mode==='LOCAL_CONTEXT'&&supplied.some(k=>k!=='refs'))||(mode==='COMPARE'&&supplied.some(k=>k!=='comparison_queries'))||(mode!=='COMPARE'&&a.comparison_queries)||(mode!=='LOCAL_CONTEXT'&&a.refs)))fail('SELECTOR_MODE_CONFLICT');
    if(mode==='METHOD')return {status:'METHOD_ONLY',mode,routing,method:METHOD_SUMMARY,corpus_operations:0,semantic_review:'NOT_REVIEWED'};
    if(mode==='VERIFY')return {status:'NEEDS_VERIFICATION_INPUT',mode,routing,next_action:'استخدم lisan_verify_quote لمرجع ونص، أو lisan_check_study لسجل موجود؛ لا تُنشأ دراسة بديلة عن التدقيق.'};
    const selectors=[];const context=a.context??(mode==='LOCAL_CONTEXT'?1:0),offset=a.offset??0,limit=a.limit??20;
    if(prior)selectors.push(prior.selector);
    else if(mode==='COMPARE'){if(!a.comparison_queries)return {status:'NEEDS_CLARIFICATION',mode,question:'ما الصيغتان أو الاستعلامان المطلوب مقارنتهما؟'};for(const query of a.comparison_queries)selectors.push({query,context});}
    else if(mode==='LOCAL_CONTEXT'){const refs=a.refs||sortRefs((a.question.match(/[1-9]\d{0,2}:[1-9]\d{0,3}/gu)||[]));if(!refs.length)return {status:'NEEDS_CLARIFICATION',mode,question:'ما مرجع الآية المطلوب دراستها؟'};selectors.push({refs,context});}
    else if(a.structural_query){if(a.query)fail('AMBIGUOUS_QUERY_KIND');selectors.push({structural_query:a.structural_query,context});}
    else if(a.query)selectors.push({query:a.query,context});
    else return {status:'NEEDS_CLARIFICATION',mode,question:'هل المطلوب صيغة حرفية محددة أم جذر بنيوي؟ أرسل query أو structural_query؛ لا يُفترض تعريف للكلمة.'};
    const bundles=[],allRetrieved=[],allMatched=[],tokens=[];
    for(const selector of selectors){let result,refs,matched,next=null;
      if(selector.query){result=await this.engine.search(selector.query,offset,limit);refs=result.occurrences.map(x=>x.ref);matched=(await this.engine.scan(selector.query)).found.map(x=>x.ref);next=result.page.next_offset;}
      else if(selector.structural_query){result=await this.engine.structural(selector.structural_query,offset,limit);refs=sortRefs(result.occurrences.map(x=>x.verse_ref));matched=result.matched_refs;next=result.page.next_offset;}
      else {result=null;refs=selector.refs;matched=refs;}
      const evidence=refs.length?(await this.engine.get(refs,context)).verses:[];
      const retrieved=evidence.map(x=>x.ref);const receipt=await this.receipts.issue(subject,{selector,mode,offset,limit,next_offset:next,retrieved_refs:retrieved,matched_refs:matched});
      bundles.push({selector,result,evidence,receipt});tokens.push(receipt);allRetrieved.push(...retrieved);allMatched.push(...matched);
    }
    const retrieved=sortRefs(allRetrieved),matched=sortRefs(allMatched);
    const selected=a.selected_layers??(mode==='LOCAL_CONTEXT'?[1,2,11,17,18,22,23,28,30]:a.structural_query?[1,2,4,5,6,7,9,18,19,27,28,30]:mode==='COMPARE'?[1,2,16,18,19,20,27,28,30]:[1,2,16,18,19,27,28,30]);
    const study={schema_version:'quran-lisan-study/1',study_id:crypto.randomUUID(),question:prior?'متابعة استعلام مثبت؛ اربط هذا الجزء بسجل السؤال الأصلي.':a.question,mode,corpus:this.engine.provenance(),selectors,
      record:{schema_version:'2.0',corpus_sha256:PINS.corpus,claims:[],limitations:[]},retrieved_refs:retrieved,analyzed_refs:[],remaining_refs:matched,receipts:tokens,
      selected_layers:selected.map(layer_id=>({layer_id,reason:'مرشح مرتبط بنوع السؤال؛ يُراجع قبل نسبة تحليل إليه.',status:'SELECTED',evidence_refs:[]})),hypotheses:[],claim_dimensions:[],counter_tests:[],dependencies:[],reopen_events:[],research_state:'UNRESOLVED',semantic_review:'NOT_REVIEWED',release_acceptance:'NOT_GRANTED',provider_kind:'HUMAN_OR_HOST_UNVERIFIED',historical_context:[]};
    return {status:'RESEARCH_PREPARED',mode,routing,provenance:this.engine.provenance(),bundles,study,
      coverage:{scan:'COMPLETE_FOR_DECLARED_SELECTORS',matched_refs:matched,retrieved_refs:retrieved,analyzed_refs:[],remaining_to_retrieve:matched.filter(r=>!retrieved.includes(r)),remaining_to_analyze:matched,analysis_basis:'NO_ANALYSIS_CLAIMED'},
      layers:data.layers.filter(x=>selected.includes(x.id)),method:METHOD_SUMMARY,
      limits:['إعداد الشواهد ليس تحليلها.','التوجيه القاعدي ليس فهمًا لغويًا مضمونًا.','مواءمة QAC بنيوية؛ النص المرجعي يؤخذ من المتن المثبت وحده.','لا قاعدة دراسات مشتركة ولا مراجعة دلالية آلية.']};
  }
  async check(a,subject){shape(a,CHECK_SCHEMA);
    if(a.import_history){if(a.study||a.record)fail('AMBIGUOUS_RECORD');return this.importHistory(a.import_history);}
    if(!!a.study===!!a.record)fail('EXACTLY_ONE_RECORD_REQUIRED');
    const study=a.study,record=study?.record||a.record;
    const mechanical=await this.engine.validate(record),errors=[...mechanical.errors],gaps=[];
    const retrieved=study?.retrieved_refs||a.retrieved_refs||[],analyzed=study?.analyzed_refs||a.analyzed_refs||[],receiptTokens=study?.receipts||a.receipts||[];
    const counters=a.counter_evidence_refs||sortRefs(study?.counter_tests.map(t=>t.ref)||[]),bad=(code)=>errors.push({code,claim_id:null});
    for(const ref of sortRefs([...retrieved,...analyzed,...counters])){try{await this.engine.verse(ref);}catch(e){bad(e.code);}}
    if(analyzed.some(r=>!retrieved.includes(r)))bad('ANALYZED_NOT_RETRIEVED');if(counters.some(r=>!analyzed.includes(r)))bad('COUNTER_NOT_ANALYZED');
    if(record.claims.flatMap(c=>c.evidence.map(e=>e.ref)).some(r=>!retrieved.includes(r)))bad('EVIDENCE_NOT_RETRIEVED');
    let attested=[],matched=[],selectors=[];
    for(const token of receiptTokens){try{const receipt=await this.receipts.read(subject,token);attested.push(...receipt.retrieved_refs);matched.push(...receipt.matched_refs);selectors.push(receipt.selector);}catch(e){bad(e.code||'INVALID_RECEIPT');}}
    attested=sortRefs(attested);matched=sortRefs(matched);
    if(receiptTokens.length&&retrieved.some(r=>!attested.includes(r)))bad('RETRIEVAL_NOT_ATTESTED');
    if(!receiptTokens.length)gaps.push('RETRIEVAL_DECLARATION_NOT_ATTESTED');
    if(study){
      if(canonical(study.corpus)!==canonical(this.engine.provenance()))bad('STUDY_CORPUS_MISMATCH');
      if(study.provider_kind==='TEST_MOCK')gaps.push('TEST_MOCK_NOT_LIVE_RESEARCH');
      if(receiptTokens.length&&study.selectors.some(s=>!selectors.some(r=>canonical(r)===canonical(s))))bad('STUDY_SELECTOR_RECEIPT_MISMATCH');
      const remaining=matched.filter(r=>!analyzed.includes(r));if(receiptTokens.length&&canonical(sortRefs(study.remaining_refs))!==canonical(remaining))bad('REMAINING_REFS_MISMATCH');
      const lids=new Set(),hids=new Set();
      for(const layer of study.selected_layers){if(lids.has(layer.layer_id))bad('DUPLICATE_LAYER');lids.add(layer.layer_id);if(layer.status==='ANALYZED'&&(!layer.observation?.trim()||!layer.evidence_refs.length))bad('LAYER_ANALYSIS_EVIDENCE_REQUIRED');if(layer.evidence_refs.some(r=>!analyzed.includes(r)))bad('LAYER_REF_NOT_ANALYZED');}
      for(const h of study.hypotheses){if(hids.has(h.id))bad('DUPLICATE_HYPOTHESIS');hids.add(h.id);if([...h.supporting_refs,...h.counter_refs].some(r=>!analyzed.includes(r)))bad('HYPOTHESIS_REF_NOT_ANALYZED');}
      for(const c of study.counter_tests){if(!hids.has(c.hypothesis_id))bad('UNKNOWN_HYPOTHESIS');if(!analyzed.includes(c.ref))bad('COUNTER_NOT_ANALYZED');}
      const cids=new Set(record.claims.map(c=>c.id));
      for(const d of study.claim_dimensions){if(!cids.has(d.claim_id))bad('UNKNOWN_CLAIM_DIMENSION');if(d.scope_refs.some(r=>!analyzed.includes(r)))bad('CLAIM_SCOPE_NOT_ANALYZED');
        if(d.claim_scope==='ROOT_CORE'&&!study.selectors.some(s=>s.structural_query?.kind==='ROOT'))gaps.push('ROOT_CORE_WITHOUT_STRUCTURAL_CENSUS');
        for(const contribution of d.layer_contributions){if(!lids.has(contribution.layer_id))bad('CONTRIBUTION_LAYER_NOT_SELECTED');if(!analyzed.includes(contribution.evidence.ref))bad('CONTRIBUTION_NOT_ANALYZED');try{if(!(await this.engine.quote(contribution.evidence.ref,contribution.evidence.text,contribution.evidence.kind)).matched)bad('CONTRIBUTION_QUOTE_NOT_VERIFIED');}catch(e){bad(e.code);}}
      }
      const semanticClaims=record.claims.filter(c=>['SUPPORTED_INFERENCE','TENTATIVE_HYPOTHESIS'].includes(c.kind));
      if(semanticClaims.length){if(!study.hypotheses.length)gaps.push('HYPOTHESES_NOT_RECORDED');if(!study.counter_tests.length)gaps.push('COUNTER_TESTS_NOT_RECORDED');if(semanticClaims.some(c=>!study.claim_dimensions.some(d=>d.claim_id===c.id)))gaps.push('SEMANTIC_COMPONENT_TRACE_MISSING');}
      if(study.historical_context.some(h=>h.quarantined))gaps.push('QUARANTINED_HISTORY_PRESENT_NOT_EVIDENCE');
    }
    if(a.query){const scan=await this.engine.scan(a.query);matched=scan.found.map(x=>x.ref);}
    return {status:errors.length?'MECHANICAL_FAIL':'MECHANICAL_PASS',mechanical:{...mechanical,status:errors.length?'MECHANICAL_FAIL':'MECHANICAL_PASS',errors},
      study_id:study?.study_id||null,coverage:{retrieved_refs:retrieved,attested_refs:attested,analyzed_refs:analyzed,matched_refs:matched,remaining_to_retrieve:matched.filter(r=>!retrieved.includes(r)),remaining_to_analyze:matched.filter(r=>!analyzed.includes(r)),analysis_basis:'RESEARCHER_DECLARATION_NOT_MACHINE_PROOF'},
      methodological_completeness:gaps.length?'RESEARCH_GAPS_REMAIN':'STRUCTURE_READY_FOR_HUMAN_REVIEW',research_gaps:[...new Set(gaps)],
      semantic_review:'NOT_REVIEWED',semantic_validity:'NOT_ASSESSED',release_acceptance:'NOT_GRANTED',publication_status:'NOT_RELEASE_ACCEPTANCE',
      public_summary:'تم فحص النصوص والمجموعات والحقول المحددة فقط. صلاحية وجه الاستدلال وعدالة البدائل تحتاج مراجعة بحثية منفصلة.'};
  }
  async importHistory(h){
    const raw=structuredClone(h.raw_record),rawtext=canonical(raw),hash=await sha(rawtext);
    // Explicit source labels and provider declarations never become canonical authority.
    const quarantined=/batch[\s_-]*0?8|TestModel|"(?:provider_kind|provider|mode)"\s*:\s*"(?:MOCK|TEST_MOCK|SIMULATED)"/iu.test(h.source_label+' '+rawtext);
    let old=[];const candidate=raw.record?.claims||raw.claims||[];
    if(Array.isArray(candidate))for(const c of candidate){if(Array.isArray(c.evidence))for(const e of c.evidence){try{shape(e,quote);old.push(e);}catch{/* Unknown native fields stay verbatim, not in active evidence. */}}}
    const refs=sortRefs(h.refs||old.map(e=>e.ref));if(refs.length>50)fail('IMPORT_REFERENCE_BUDGET');
    const fresh=refs.length?(await this.engine.get(refs,0)).verses:[];
    const checks=[];for(const e of old){try{checks.push({ref:e.ref,kind:e.kind,matched:(await this.engine.quote(e.ref,e.text,e.kind)).matched});}catch(error){checks.push({ref:e.ref,matched:false,status:error.code});}}
    return {status:quarantined?'HISTORY_QUARANTINED':'HISTORY_IMPORTED_FOR_REVALIDATION',historical:{source_label:h.source_label,source_sha256:hash,native_states:structuredClone(h.native_states),raw_record:raw,reuse_state:'HYPOTHESIS_ONLY_REVALIDATION_REQUIRED',quarantined,old_evidence:old},
      re_fetched_evidence:fresh,old_quote_checks:checks,provenance:this.engine.provenance(),analysis_coverage:'NOT_ANALYZED',canonical_state:'NOT_CANONICAL',semantic_review:'NOT_REVIEWED',release_acceptance:'NOT_GRANTED',
      limitations:['الحالة الأصلية محفوظة كتاريخ، وليست سلطة في المرشح.','لا تعني إعادة استرجاع الآيات إعادة تنفيذ التحليل القديم.','لا يتم تعديل LISAN3 أو عزل بياناته الحية.']};
  }
}
export function wrapLegacy(record,meta){shape({record},data.tool_inputs.lisan_validate_analysis);const study=structuredClone(meta);study.record=structuredClone(record);return study;}
export function unwrapLegacy(study){shape({record:study.record},data.tool_inputs.lisan_validate_analysis);return structuredClone(study.record);}
export async function reopen(study,reason,ids){
  const copy=structuredClone(study),affected=new Set(ids);let changed=true;while(changed){changed=false;for(const d of copy.dependencies)if(affected.has(d.parent_id)&&!affected.has(d.child_id)){affected.add(d.child_id);changed=true;}}
  copy.reopen_events.push({reason,affected_ids:[...affected],previous_digest:await sha(canonical(study))});copy.research_state='UNRESOLVED';copy.semantic_review='NOT_REVIEWED';copy.release_acceptance='NOT_GRANTED';return copy;
}
