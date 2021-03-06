# Modified from example on the mrjobs github page.
# The original copywrite info below:
#
#
# Copyright 2009-2010 Yelp
# Copyright 2013 David Marin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.from mrjob.job import MRJob
#
from mrjob.protocol import JSONProtocol
from mrjob.step import MRStep
from mrjob.job import MRJob
import mrjob



class MRPageRank(MRJob):

    INPUT_PROTOCOL = JSONProtocol  # read the same format we write

    def configure_options(self):
        super(MRPageRank, self).configure_options()
        self.add_passthrough_option('--iterations', default=10, type='int')
        self.add_passthrough_option('--beta', dest='beta', default=0.85,type='float')


    def send_score(self, node_id, node):
        """Mapper: send score from a single node to other nodes.

        Input: ``node_id, node``

        Output:
        ``node_id, ('node', node)`` OR
        ``node_id, ('score', score)``
        """
        yield node_id, ('node', node)

        for dest_id, weights in node['links']:
            yield dest_id, ('score', [s * w for s,w in zip(node['score'], weights)])



    def receive_score(self, node_id, typed_values):
        """Reducer: Combine scores sent from other nodes, and update this node
        (creating it if necessary).

        Store information about the node's previous score in *prev_score*.
        """
        node = {}
        total_score = 0

        for value_type, value in typed_values:
            if value_type == 'node':
                node = value
            else:
                assert value_type == 'score'
                if total_score == 0:
                    total_score = value
                else:
                    for i in xrange(len(total_score)):
                        total_score[i] += value[i]

        node['prev_score'] = node['score']
        b = self.options.beta # for readability
        if total_score == 0: #noinlinks
            for i in xrange(len(node['score'])):
                node['score'][i] = (1 - b) * node['telep_prob'][i]
        else:
            for i in xrange(len(total_score)):
                node['score'][i] = (1 - b) * node['telep_prob'][i] + b * total_score[i]

        yield node_id, node

    def steps(self):
        return ([MRStep(mapper=self.send_score,
                        reducer=self.receive_score)] *
                self.options.iterations)

if __name__ == '__main__':
    MRPageRank.run()

