from cziName import Name as nm
import unittest


class TestCziName(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_setMouseId_lowerCase(self):
        name = nm('AAV400_AAV995_s238_SC_A-02.czi')
        self.assertEqual(name.setMouseId(), '238')

    def test_setMouseId_upperCase(self):
        name = nm('AAV400_AAV995_S238_SC_A-02.czi')
        self.assertEqual(name.setMouseId(), '238')

    def test_setMouseId_lessNumbers(self):
        name = nm('AAV400_AAV995_S2_SC_A-02.czi')
        self.assertEqual(name.setMouseId(), '2')

    def test_setMouseId_moreNumbers(self):
        name = nm('AAV400_AAV995_S2478_SC_A-02.czi')
        self.assertEqual(name.setMouseId(), '2478')

    def test_setMouseId_noMatch(self):
        name = nm('AAV400_AAV995_SC_A-02.czi')
        self.assertEqual(name.setMouseId(), 0)

    def test_setMouseId_noName(self):
        name = nm('')
        self.assertEqual(name.setMouseId(), 0)

    def test_findAAV_lowerCase(self):
        name = nm('aav400_aav995_s238_SC_A-02.czi')
        self.assertEqual(name.findAAVVectors(), ['aav400', 'aav995'])

    def test_findAAV_upprCase(self):
        name = nm('AAV400_AAV995_s238_SC_A-02.czi')
        self.assertEqual(name.findAAVVectors(), ['AAV400', 'AAV995'])

    def test_findAAV_plusMatch(self):
        name = nm('AAV400+995_s238_SC_A-02.czi')
        self.assertEqual(name.findAAVVectors(), ['AAV400', 'AAV995'])

    def test_findAAV_minusMatch(self):
        name = nm('AAV400-995_s238_SC_A-02.czi')
        self.assertEqual(name.findAAVVectors(), ['AAV400', 'AAV995'])

    def test_findAAV_lowerCase_plusMatch(self):
        name = nm('aav500_AAV400+995_s238_SC_A-02.czi')
        self.assertEqual(name.findAAVVectors(), ['aav500', 'AAV400', 'AAV995'])

    def test_findAAV_noMatch(self):
        name = nm('s238_SC_A-02.czi')
        self.assertEqual(name.findAAVVectors(), [])

    def test_findAAV_noName(self):
        name = nm('')
        self.assertEqual(name.findAAVVectors(), [])

    def test_findRab_lowerCase(self):
        name = nm('rab1.2_s238_SC_A-02.czi')
        self.assertEqual(name.findRabVectors(), ['rab1.2'])

    def test_findRab_vlowerCase(self):
        name = nm('rabv1.2_s238_SC_A-02.czi')
        self.assertEqual(name.findRabVectors(), ['rabv1.2'])

    def test_findRab_upperCase(self):
        name = nm('RAB1.2_s238_SC_A-02.czi')
        self.assertEqual(name.findRabVectors(), ['RAB1.2'])

    def test_findRab_vupperCase(self):
        name = nm('RABV1.2_s238_SC_A-02.czi')
        self.assertEqual(name.findRabVectors(), ['RABV1.2'])

    def test_findRab_noMatch(self):
        name = nm('s238_SC_A-02.czi')
        self.assertEqual(name.findRabVectors(), [])

    def test_findRab_noName(self):
        name = nm('')
        self.assertEqual(name.findRabVectors(), [])

    def test_setVectors_aavAndRab(self):
        name = nm('aav999-888_rab1.2_rabv1.3_s238_SC_A-02.czi')
        self.assertEqual(name.setViralVectors(), ['aav999', 'AAV888', 'rab1.2', 'rabv1.3'])

    def test_setVectors_noMatch(self):
        name = nm('s238_SC_A-02.czi')
        self.assertEqual(name.setViralVectors(), [])

    def test_setVectors_noName(self):
        name = nm('')
        self.assertEqual(name.setViralVectors(), [])

    def test_setInjectionSite_patte(self):
        name = nm('AAV425_patte_DRG-02.czi')
        self.assertEqual(name.setInjectionSite(), 'patte')

    def test_setInjectionSite_IV(self):
        name = nm('AAV533-IV-BB1-02.czi')
        self.assertEqual(name.setInjectionSite(), 'IV')

    def test_setInjectionSite_noMatch(self):
        name = nm('AAV533-BB1-02.czi')
        self.assertEqual(name.setInjectionSite(), '')

    def test_setInjectionSite_noName(self):
        name = nm('')
        self.assertEqual(name.setInjectionSite(), '')

    def test_setTags_moelle(self):
        name = nm('AAV425_patte_moelle.czi')
        self.assertEqual(name.setTags(), 'moelle')

    def test_setTags_antiRabbitSpace(self):
        name = nm('AAV400_anti rabbit-03.czi')
        self.assertEqual(name.setTags(), 'antirabbit')

    def test_setTags_duplicates(self):
        name = nm('AAV400_antimcherry_antimcherry-03.czi')
        self.assertEqual(name.setTags(), 'antimcherry')

    def test_setTags_severalDifferentTags(self):
        name = nm('AAV400_antimcherry_drg21231_anti rabbit_neurones_BB123-03.czi')
        self.assertEqual(name.setTags(), 'antimcherry;drg;antirabbit;neurones;BB')

    def test_setTags_noMatch(self):
        name = nm('AAV400-03.czi')
        self.assertEqual(name.setTags(), '')

    def test_setTags_noName(self):
        name = nm('')
        self.assertEqual(name.setTags(), '')