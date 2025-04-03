import random
import os
import json
from collections import defaultdict

here = os.path.abspath(os.path.dirname(__file__))


def register_content(dc):

    def get_data():
        with open(os.path.join(here, 'sequences.json')) as f:
            dataJson = json.load(f)

        data = {}

        for k, seq in dataJson.items():
            pts = seq['pts']
            data[k] = {'id': k, 'pts': pts, 'seq': list(k), 'sol': seq['sol']}

        return data

    def get_sessions():
        sessions = dc.app.dm.get_config('sequences')['sessions']
        all_seen = set()
        for s in sessions:
            all_seen.update(d['id'] for d in s['data'])

        return sessions, all_seen

    @dc.content
    def dashboard(**kwargs):
        data = get_data()
        sequences = defaultdict(lambda: [])
        sessions, all_seen = get_sessions()

        for k, seq in data.items():
            pts = seq['pts']
            if seq['id'] not in all_seen:
                sequences[pts].append(seq)

        random.seed()
        mixed_seqs = []
        for pts, seqs in sequences.items():
            random.shuffle(seqs)
            mixed_seqs.extend(seqs[:pts*10])

        random.shuffle(mixed_seqs)

        return {
            'sequences': mixed_seqs,
            'sequencesDict': data
        }

    @dc.content
    def applications(**kwargs):
        data = get_data()
        sessions, all_seen = get_sessions()
        all_good = 0
        all_bad = 0
        for s in sessions:
            n = len(s['data'])
            bad = sum(1 for d in s['data'] if d['expired'])
            good = n - bad
            avg = sum(d['secs'] for d in s['data'] if not d['expired']) / good
            s['info'] = {
                'avg': '%0.2f' % avg,
                'good': good,
                'bad': bad
            }
            all_good += good
            all_bad += bad

        total = len(data)
        seen = len(all_seen)
        seen_percent = seen * 100 / total

        pie_data = [
            {'name': 'Seen', 'y': seen_percent, 'value': seen, 'color': 'green'},
            {'name': 'Unseen', 'y': 100 - seen_percent, 'value': total - seen, 'color': 'lightgrey'}
        ]
        return {
            'firstname': dc.app.user.name.split()[0],
            'sessions': sessions,
            'sequencesDict': data,
            'stats': {
                'seen': seen,
                'total': total,
                'percent': '%0.2f' % seen_percent,
                'good': all_good,
                'bad': all_bad
            },
            'pie_data': pie_data
        }


