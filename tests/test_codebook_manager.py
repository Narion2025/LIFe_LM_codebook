import tempfile
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import shutil
from pathlib import Path
import yaml
import unittest

from core.marker_model import codebook_manager as cm


class TestCodebookManager(unittest.TestCase):
    def setUp(self):
        self.orig_paths = (cm.MARKER_FILE, cm.INDIKATOREN_FILE, cm.META_FILE)
        self.tmpdir = tempfile.mkdtemp()
        cm.MARKER_FILE = Path(self.tmpdir) / 'marker_library.yaml'
        cm.INDIKATOREN_FILE = Path(self.tmpdir) / 'indikatoren.yaml'
        cm.META_FILE = Path(self.tmpdir) / 'meta_indikatoren.yaml'
        with open(cm.MARKER_FILE, 'w') as f:
            yaml.dump({'marker_library': []}, f)
        with open(cm.INDIKATOREN_FILE, 'w') as f:
            yaml.dump({'indikatoren': []}, f)
        with open(cm.META_FILE, 'w') as f:
            yaml.dump({'meta_indikatoren': []}, f)

    def tearDown(self):
        cm.MARKER_FILE, cm.INDIKATOREN_FILE, cm.META_FILE = self.orig_paths
        shutil.rmtree(self.tmpdir)

    def test_add_marker_and_indikator(self):
        cm.add_marker({
            'id': 'm1',
            'typ': 'test',
            'hinweis': 'h',
            'beispiel_aussage': 'b',
            'linked_indicators': ['i1']
        })
        cm.add_indikator({
            'id': 'i1',
            'name': 'I1',
            'meta_indikatoren': [],
            'marker_ids': ['m1']
        })
        errors = cm.check_consistency()
        self.assertEqual(errors, {'indikatoren': [], 'meta': [], 'marker': []})

