import urllib.request
import json

def test_api():
    base_url = 'http://127.0.0.1:8000/api'
    
    # 1. Test Recommendations
    req = urllib.request.urlopen(f'{base_url}/recommendations?learner_id=1')
    recs = json.loads(req.read().decode())
    print('1. Live Recommendations for Learner 1:')
    for r in recs:
        cid = r["concept_id"]
        title = r["concept_title"]
        act = r["action_type"]
        print(f'   - Concept ID {cid}: {title} ({act})')
    
    # 2. Test Concepts Question Audit
    concepts_to_test = [
        ('Arrays', 3),
        ('Linked Lists', 4),
        ('Stacks', 5),
        ('Trees', 9),
        ('Graphs', 12),
        ('Algorithmic Thinking', 1),
        ('Queues', 5) # Stacks & Queues is concept 5
    ]
    
    print('\n2. Concept Question Audit:')
    for name, cid in concepts_to_test:
        q_req = urllib.request.urlopen(f'{base_url}/questions?concept_id={cid}')
        q_list = json.loads(q_req.read().decode())
        can_rec = any(r['concept_id'] == cid for r in recs)
        print(f'   - {name} (ID {cid}): {len(q_list)} questions in API. In current recommendations: {can_rec}')
        
    # 3. Test Question Submission on Recommended Concept (Arrays)
    rec_concept = recs[0]
    rec_cid = rec_concept['concept_id']
    q_req = urllib.request.urlopen(f'{base_url}/questions?concept_id={rec_cid}')
    questions = json.loads(q_req.read().decode())
    assert len(questions) > 0, 'No questions found for recommended concept!'
    
    first_q = questions[0]
    print(f'\n3. Testing Question Submission for {rec_concept["concept_title"]}:')
    print(f'   - Question: {first_q["question_text"]}')
    print(f'   - Selected Option: {first_q["options"][0]}')
    
    submit_payload = {
        'question_id': first_q['id'],
        'selected_option': first_q['options'][0],
        'response_time_seconds': 12.5,
        'session_id': 1
    }
    submit_req = urllib.request.Request(
        f'{base_url}/questions/submit?learner_id=1',
        data=json.dumps(submit_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    submit_res = json.loads(urllib.request.urlopen(submit_req).read().decode())
    print('   - Submit Result:')
    print(f'     * is_correct: {submit_res["is_correct"]}')
    print(f'     * bkt_prior: {submit_res["bkt_prior"]}')
    print(f'     * bkt_posterior: {submit_res["bkt_posterior"]}')
    print(f'     * mastery_change: {submit_res["mastery_change"]}')
    next_rec = submit_res.get("next_recommendation")
    next_rec_title = next_rec.get("concept_title") if next_rec else "None"
    print(f'     * next_recommendation: {next_rec_title}')

if __name__ == '__main__':
    test_api()
