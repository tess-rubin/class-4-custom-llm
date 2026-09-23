"""Build evidence tables from saved artifacts; never train or modify scoring."""
from pathlib import Path
import hashlib,json,math,csv,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from run_evals import load_suite,matching_cases,suite_hash,word_tokens
from test_corpus import load_folder

def read(p):return json.loads(p.read_text())
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def pct(x):return 'n/a' if x is None else f'{100*x:.2f}%'
def textcell(s):return s.replace('|','\\|').replace('\n',' ') or '**[empty response]**'
runs={k:ROOT/read(ROOT/f'evidence/{k}/execution.json')['run_dir'] for k in ['setup','starter','expanded']}
data={k:{n:read(r/f'{n}.json') for n in ['config','training_summary','history','inspection','tokenization','corpus_manifest','split','vocabulary_report','temperature_comparison']} for k,r in runs.items()}
extra,manifest=load_folder(ROOT/'corpus/expanded'); extra=set(extra); suite=load_suite()
plan=read(ROOT/'evidence/provenance/pretraining_plan.json')
source_checks={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha for p,sha in plan['source_sha256'].items()}
assert all(source_checks.values())
audit={'preserved_sources':source_checks,'canonical_suite_sha256':suite_hash(suite),'suite_file_sha256':plan['source_sha256']['evals/language_evals.json'],'extension_unique_passages':len(extra),'runs':{},'notes':['Exact normalized matching is not a semantic leakage detector.','All 240 passages were composed before the suite stories were read; semantic review found no copied stories, answer lists, or close story paraphrases. Generic concepts intentionally overlap.']}
metrics=[];summaries={};results={}
for label in ['starter','expanded']:
 r=runs[label]; d=data[label]; split=d['split'];vocab=set(d['tokenization']['vocabulary'])
 assert d['training_summary']['completed_steps']==3000 and not d['training_summary']['interrupted']
 assert d['config']['seed']==42 and d['config']['device']=='cpu'
 assert not set(split['train'])&set(split['validation'])
 assert all(not matching_cases(p,suite) for p in split['train']+split['validation'])
 panels={p:{'documents':len(split[p]),'extension_documents':len(set(split[p])&extra),'nonpadding_targets':sum(len(word_tokens(t))+1 for t in split[p]),'sha256':hashlib.sha256(json.dumps(split[p]).encode()).hexdigest()} for p in ['evaluation_train','evaluation_validation']}
 assert all(p['documents']<=20 for p in panels.values())
 leakage=[{'source':f['file'],'matches':matching_cases((ROOT/'corpus/expanded'/f['file']).read_text(),suite)} for f in manifest['files']] if label=='expanded' else []
 assert all(not row['matches'] for row in leakage)
 eval_unknown={}
 for part in ['prompt','choices']:
  toks=[t for c in suite['cases'] for t in word_tokens(c['prompt'] if part=='prompt' else ' '.join(c['choices']))]
  eval_unknown[part]={'unknown_tokens':sum(t not in vocab for t in toks),'total_tokens':len(toks),'unknown_rate':sum(t not in vocab for t in toks)/len(toks)}
 for stage in ['untrained','final']:
  key=(label,stage);rows=read(r/f'language_evals/{stage}/eval_results.json'); summary=read(r/f'language_evals/{stage}/eval_summary.json')
  assert len(rows)==48 and {x['id'] for x in rows}=={x['id'] for x in suite['cases']}
  assert summary['suite_sha256']==suite_hash(suite)
  summaries[key]=summary;results[key]=rows
  metrics.append({'experiment':label,'stage':stage,**summary['overall'],'eval_prompt_unknown_rate':eval_unknown['prompt']['unknown_rate'],'eval_choice_unknown_rate':eval_unknown['choices']['unknown_rate']})
 rerun=read(ROOT/f'evidence/{label}/saved-model-eval/eval_results.json')
 assert rerun==results[(label,'final')]
 nb=read(ROOT/f'notebooks/{label}.executed.ipynb')
 codes=[c for c in nb['cells'] if c['cell_type']=='code']
 assert all(c['execution_count'] is not None for c in codes)
 assert not [o for c in codes for o in c['outputs'] if o['output_type']=='error']
 original=read(ROOT/'custom_llm.ipynb');origcodes=[c for c in original['cells'] if c['cell_type']=='code']
 assert all(c['source']==o['source'] for c,o in zip(codes[1:],origcodes[1:]))
 audit['runs'][label]={'run_dir':str(r.relative_to(ROOT)),'two_48_case_sets_complete':True,'saved_eval_rerun_exact_match':True,'source_code_cells_unchanged_except_corpus_folder':True,'no_eval_prefix_in_any_split':True,'split_disjoint':True,'source_file_leakage_checks':leakage,'panels':panels,'eval_token_unknown_rates':eval_unknown,'extension_split_counts':{p:len(set(split[p])&extra) for p in ['train','validation']},'notebook_code_cells_executed':len(codes),'errors':0,'untrained_model_sha256':summaries[(label,'untrained')]['model_sha256'],'final_model_sha256':summaries[(label,'final')]['model_sha256']}
audit['four_complete_48_case_result_sets'] = len(results) == 4
chat_path = ROOT/'evidence/expanded/terminal_chat.json'
if chat_path.exists():
    chat = read(chat_path)
    assert len(chat['turns']) == 3
    assert chat['model_sha256'] == audit['runs']['expanded']['final_model_sha256']
    audit.update({'chat_turns':3, 'chat_model_matches_expanded_final':True,
                  'screenshot':'evidence/expanded/terminal_chat.png'})
import zipfile
for label in ['starter','expanded']:
    run = runs[label]
    with zipfile.ZipFile(str(run)+'.zip') as archive:
        files = {str(p.relative_to(run)):p for p in run.rglob('*') if p.is_file()}
        assert {n for n in archive.namelist() if not n.endswith('/')} == set(files)
        assert all(archive.read(name) == p.read_bytes() for name,p in files.items())
audit['main_zip_byte_checks'] = True
write(ROOT/'evidence/acceptance.json',audit);write(ROOT/'evidence/comparison.json',metrics)
with (ROOT/'evidence/comparison.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(metrics[0]));w.writeheader();w.writerows(metrics)
# Every sample receives a written assessment, including all setup samples.
review=['# Sample review','', 'Every saved BOS sample is reproduced below. Empty strings are labeled explicitly, never omitted. The four samples at each main stage use temperature 0.8, seed 2026, and a 32-token maximum. Evaluations use a separate 24-token continuation limit.','']
for label in ['setup','starter','expanded']:
 for p in sorted((runs[label]/'samples').glob('*.txt')):
  stage=int(p.stem.split('_')[1]);samples=p.read_text().split('\n');assert len(samples)==4
  review += [f'## {label}, step {stage}','']
  for i,s in enumerate(samples):
   if not s: assessment='Empty: EOS was selected before any visible token; this is a real output.'
   elif label=='setup' or stage==0:assessment='Garbled word sequence with no stable sentence structure; an untrained or only briefly trained sample.'
   elif label=='expanded' and stage==1500 and i==1:assessment='Template-shaped but semantically mixed: a teacher is used where the classroom template normally names a place, and peach/harvest belong to the fruit domain.'
   elif label=='expanded' and stage==3000 and i==1:assessment='Grammatical fragments combine incoherently: putting a light room to a small pear has no clear meaning.'
   else:assessment='Coherent within a repeated classroom template; this shows local pattern learning, not broad language competence.'
   review += [f'**Sample {i+1}:** {textcell(s)}','',assessment,'']
(ROOT/'evidence/sample_review.md').write_text('\n'.join(review))
# All 192 case continuations and failures, with explicit unknown and choice details.
lines=['# Complete evaluation review','', 'All 192 original cases remain here and in the original JSON/CSV folders. Choice correctness and free-text quality are different. Empty continuations are retained. This is a public development benchmark.','']
for (label,stage),rows in results.items():
 lines += [f'## {label} / {stage}','', '| Case | Category | Status | Expected | Picked | Score | Missing prompt words | Missing choices | Actual free continuation |','|---|---|---|---|---|---:|---|---|---|']
 for x in rows:
  lines.append('| '+' | '.join([x['id'],x['category'],x['status'],x['expected'],str(x['predicted_choice']),str(x['score']),', '.join(x['unknown_prompt_words']) or 'none',', '.join(x['unknown_choices']) or 'none',textcell(x['generated_text'])])+' |')
 lines += ['', 'Failed case IDs: '+', '.join(x['id'] for x in rows if not x['score'])+'.','']
(ROOT/'evidence/evaluation_review.md').write_text('\n'.join(lines))
# Full coordinate precision and full probability tables, not a truncated vector.
lines=['# Token, embedding, probability, and update evidence','', 'These explanations were written by Codex at the user’s request; they are not represented as independently written student answers.','']
neighbors={}
for label in ['starter','expanded']:
 d=data[label];i=d['inspection'];v=d['tokenization']['vocabulary'];u=i['first_update'];cp=read(runs[label]/'checkpoint.json')
 def near(table):
  q=table[i['token_id']];qn=math.sqrt(sum(x*x for x in q));r=[]
  for n,row in enumerate(table):
   if n==i['token_id']:continue
   sim=sum(a*b for a,b in zip(q,row))/(qn*math.sqrt(sum(x*x for x in row)))
   r.append((v[n],sim))
  return sorted(r,key=lambda x:x[1],reverse=True)[:3]
 neighbors[label]={'before':near(cp['initial_embeddings']),'after':near(cp['weights']['wte'])}
 lines += [f'## {label}: customer, ID {i["token_id"]}','', f'The word tokenizer lowercases words and separates punctuation. The ID is an arbitrary lookup row, not a magnitude or a measure of meaning. `customer` selects row {i["token_id"]} in a {len(v)} × 64 token table. The expanded vocabulary assigns a different row than the starter. Position vectors are separate. The token table is tied to the output projection.','', '| Coordinate (zero-based) | Before training | After 3,000 steps |','|---:|---:|---:|']
 for n,(a,b) in enumerate(zip(i['embedding_before'],i['embedding_after'])):lines.append(f'| {n} | {a!r} | {b!r} |')
 lines += ['', 'Each of the 64 coordinates is learned jointly; no coordinate has an assigned human concept. The model adds position embeddings, mixes earlier context through causal attention, and applies feed-forward layers, GELU, residual connections, and LayerNorm. A 3D PCA plot compresses these 64 dimensions and can distort distance. Neighbors below use the full 64-number vectors.','',f'Nearest cosine neighbors before: {neighbors[label]["before"]}. After: {neighbors[label]["after"]}. Shared designed sentence contexts can explain similar vectors; this is not proof of human-like meaning.','',f'**First real update:** coordinate {u["coordinate"]} began at `{u["before"]!r}`, its recorded loss gradient was `{u["gradient"]!r}`, the effective learning rate was `{u["learning_rate"]!r}`, and AdamW moved it to `{u["after"]!r}` (delta `{u["after"]-u["before"]!r}`).'.replace(']!r}',']}'),'', 'The positive gradient says that locally increasing this coordinate increases this batch’s next-token loss, with other coordinates held fixed. The recorded gradient is before global norm clipping. The observed update is after clipping and AdamW, including momentum, adaptive scaling, and weight decay. It is not simply minus learning rate times the raw gradient. Warmup makes the first learning rate 0.00001, although the chosen base rate is 0.001. Later updates can reverse a coordinate’s direction. This is an actual training gradient, distinct from the notebook’s illustrative a*a+a derivative.','', f'**Probabilities for `{i["prefix"]}`:** softmax converts contextual logits into a distribution over all {len(v)} tokens. Cross-entropy penalizes low probability on the observed next token; backpropagation supplies gradients for the update. Sampling draws from this distribution without changing weights. All probabilities below are raw temperature-1 inspection values, not normalized over four eval choices.','', '| Token | ID | Before | After |','|---|---:|---:|---:|']
 for n,t in enumerate(v):lines.append(f'| {t} | {n} | {i["probabilities_before"][n]!r} | {i["probabilities_after"][n]!r} |')
 lines += ['', 'First-block, first-head attention over BOS, the, customer: `'+json.dumps(i['attention_rows'])+'`. Future positions have zero probability because of the causal mask. These attention weights mix context; they are not the token embedding and are not a complete explanation of a prediction.','']
(ROOT/'evidence/learning_checkpoints.md').write_text('\n'.join(lines));write(ROOT/'evidence/neighbors.json',neighbors)
print(json.dumps(audit,indent=2))
