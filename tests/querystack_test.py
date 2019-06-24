from unittest import TestCase
from logik import querystack as qs

s = qs.Querystack()


class testQuery(TestCase):
    def test_stack_init(self):
        self.assertEqual(s.size(), 9)

    def test_push1_size(self):
        item = 5
        print(s.push(item))
        self.assertEqual(s.push(item), None)

    def test_push2_size(self):
        s.push(5)
        s.push(6)
        self.assertEqual(s.size(), 9)

    def test_push2_pop1_size(self):
        s.push(5)
        s.push(6)
        s.pop()
        self.assertEqual(s.size(), 6)

    def test_push2_pop1_value(self):
        s.push(8)
        s.push(9)
        self.assertEqual(s.pop(), 9)

    def test_push2_pop2_size(self):
        s.push("Glob")
        s.push("Blob")
        s.pop()
        s.pop()
        self.assertEqual(s.size(), 7)

    def test_push2_pop2_value(self):
        s.push("Glob")
        s.push("Blob")
        s.pop()
        self.assertEqual(s.pop(), "Glob")

    def test_peek_push1(self):
        s.push(88)
        self.assertEqual(s.peek(), 88)

    def test_peek_push3_pop1(self):
        s.push(7)
        s.push(889)
        s.push(3)
        s.pop()
        self.assertEqual(s.peek(), 889)

    def test_pop_empty(self):
        self.assertEqual(s.pop(), None)

    def test_pop_empty(self):
        self.assertNotEqual(s.pop(), [])

    def test_peek_empty(self):
        self.assertNotEqual(s.peek(), None)

    def test_bottom(self):
        self.assertNotEquals(s.bottom(), None)


class TestQueryStackSingleton(TestCase):

    def testQueryStackerstInstanzDannKonstruktor(self):
        from logik import querystack
        import pytest
        with pytest.raises(Exception):
            qIK = querystack.getInstance()
            print(qIK)
            qIK2 = querystack.queryStack()
            self.assertEqual(qIK, qIK2)

    def testQueryStackerstKonstruktorDannKonstruktor(self):
        from logik import querystack
        import pytest
        with pytest.raises(Exception):
            q1K = querystack.queryStack()
            q2K = querystack.queryStack()
            self.assertEqual(q1K, q2K)

    def testQueryStackerstInstanzDannInstanz(self):
        from logik import querystack
        q1 = querystack.Querystack.getInstance()
        print(q1)
        q2 = querystack.Querystack.getInstance()
        print(q2)
        self.assertEqual(q1, q2)
