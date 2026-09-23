import json

from daedalus.registry import ExperimentRegistry
from daedalus.utils import sqlite_connection


def test_registry_can_persist_post_corpus_result_without_losing_config(tmp_path):
    path=tmp_path/'x.sqlite3'; r=ExperimentRegistry(path)
    r.record('e','sha','src','model',{'a':1},{'stage':'final'},False)
    r.update_result('e',{'stage':'final','corpus_qvalue':0.03})
    with sqlite_connection(path) as con:
        config_json,result_json,promoted=con.execute(
            'SELECT config_json,result_json,promoted FROM experiments WHERE experiment_id=?',('e',)
        ).fetchone()
    assert json.loads(config_json)=={'a':1}
    assert json.loads(result_json)['corpus_qvalue']==0.03
    assert promoted==0
