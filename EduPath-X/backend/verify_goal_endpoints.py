import urllib.request
import json

base_url = 'http://127.0.0.1:8000/api'

# 1. Create or get active goal
create_payload = json.dumps({'concept_id': 3, 'target_mastery': 0.80, 'goal_name': 'Master Arrays & Strings'}).encode()
req = urllib.request.Request(f'{base_url}/goals?learner_id=1', data=create_payload, headers={'Content-Type': 'application/json'})
goal = json.loads(urllib.request.urlopen(req).read().decode())
print('Created/Updated Goal:', json.dumps(goal, indent=2))

goal_id = goal["id"]

# 2. Repeated progress submission (idempotency check)
prog_req1 = urllib.request.Request(f'{base_url}/goals/{goal_id}/progress', data=b'', headers={'Content-Type': 'application/json'})
res1 = json.loads(urllib.request.urlopen(prog_req1).read().decode())

prog_req2 = urllib.request.Request(f'{base_url}/goals/{goal_id}/progress', data=b'', headers={'Content-Type': 'application/json'})
res2 = json.loads(urllib.request.urlopen(prog_req2).read().decode())

print('Progress 1:', res1['progress_percentage'], 'Current Mastery:', res1['current_mastery'])
print('Progress 2:', res2['progress_percentage'], 'Current Mastery:', res2['current_mastery'])
assert res1['progress_percentage'] == res2['progress_percentage'], 'Progress should be idempotent!'
assert res1['current_mastery'] == res2['current_mastery']

# 3. Check Dashboard synchronization
dash = json.loads(urllib.request.urlopen(f'{base_url}/dashboard?learner_id=1').read().decode())
print('Dashboard Goal:', json.dumps(dash['goal'], indent=2))
print('Dashboard Top Recommendation Active Goal:', json.dumps(dash['recommendations'][0].get('active_goal'), indent=2))
print('\nGoal API and Dashboard verification successful!')
