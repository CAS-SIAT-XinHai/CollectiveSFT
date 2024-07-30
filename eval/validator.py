import json
samples = json.load(open('/path/to/your/result.json'))

assert type(samples) == list
assert len(samples) == 11200
assert all([type(s) == dict for s in samples])

# "id" and "model_answer" are required keys for each sample. Redundant keys have no effect on evaluation.
assert all(['id' in s for s in samples]), "'id' must be a key of every sample"
assert all(['model_answer' in s for s in samples]), "'model_answer' must be a key of every sample"
assert sorted([s['id'] for s in samples]) == list(range(1, 11200+1)), 'ids must start from 1 and end at 11200'

print('good to go!')