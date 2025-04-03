import random
import os
import json
from collections import defaultdict

here = os.path.abspath(os.path.dirname(__file__))


def register_content(dc):

    @dc.content
    def dashboard(**kwargs):
        with open(os.path.join(here, 'sequences.json')) as f:
            data = json.load(f)

        sequences = defaultdict(lambda: [])

        for k, seq in data.items():
            pts = seq['pts']
            sequences[pts].append({'id': k, 'pts': pts, 'seq': list(k), 'sol': seq['sol']})

        random.seed()
        mixed_seqs = []
        for pts, seqs in sequences.items():
            random.shuffle(seqs)
            mixed_seqs.extend(seqs[:pts*10])

        random.shuffle(mixed_seqs)

        data = {
            'sequences': mixed_seqs
        }
        return data

    @dc.content
    def sequences(**kwargs):
        pass


