from unittest import TestCase

from scheduler import Task, Scheduler, MultilevelScheduler


def run_scheduler(tasks: str):
    Task.reset()
    Scheduler.reset()
    scheduler = MultilevelScheduler()
    for line in tasks.splitlines():
        if line.strip() != "":
            scheduler.add_task(Task(line.strip()))
    scheduler.run()
    Task.runtimes.sort(key=lambda x: x[0])
    return Task.queue, ','.join([':'.join(v) for v in Task.runtimes])


class SchedulerTest(TestCase):
    def test_1(self):
        queue, runtimes = run_scheduler("""
                                        A,0,0,6
                                        B,0,1,5
                                        C,1,5,2
                                        D,1,10,1
                                        """)
        self.assertEqual(queue, "ACABDB")
        self.assertEqual(runtimes, ','.join(sorted("A:2,B:8,C:0,D:0".split(","))))

    def test_2(self):
        queue, runtimes = run_scheduler("""
                                        A,1,2,7
                                        B,1,2,3
                                        """)
        self.assertEqual(queue, "ABABA")
        self.assertEqual(runtimes, ','.join(sorted("A:3,B:4".split(","))))

    def test_3(self):
        queue, runtimes = run_scheduler("""
                                        Q,0,5,8
                                        P,1,7,2
                                        """)
        self.assertEqual(queue, "QPQ")
        self.assertEqual(runtimes, ','.join(sorted("Q:2,P:0".split(","))))

    def test_4(self):
        queue, runtimes = run_scheduler("""
                                        A,0,0,5
                                        B,0,0,4
                                        C,0,1,3
                                        D,0,2,1
                                        """)
        self.assertEqual(queue, "BDBCA")
        self.assertEqual(runtimes, ','.join(sorted("A:8,B:1,C:4,D:0".split(","))))

    def test_5(self):
        queue, runtimes = run_scheduler("""
                                        A,0,0,3
                                        B,1,0,2
                                        C,0,3,3
                                        D,1,4,1
                                        """)
        self.assertEqual(queue, "BADAC")
        self.assertEqual(runtimes, ','.join(sorted("A:3,B:0,C:3,D:0".split(","))))

    def test_6(self):
        queue, runtimes = run_scheduler("""
                                        A,0,0,5
                                        B,0,1,3
                                        C,1,1,1
                                        D,0,4,1
                                        E,1,3,2
                                        """)
        self.assertEqual(queue, "ACBEDBA")
        self.assertEqual(runtimes, ','.join(sorted("A:7,B:4,C:0,E:0,D:1".split(","))))

    def test_7(self):
        queue, runtimes = run_scheduler("""
                                        A,1,3,5
                                        D,1,6,1
                                        """)
        self.assertEqual(queue, "ADA")
        self.assertEqual(runtimes, ','.join(sorted("A:1,D:1".split(","))))

    def test_8(self):
        queue, runtimes = run_scheduler("""
                                        A,1,2,7
                                        B,0,4,2
                                        C,1,2,2
                                        D,1,2,1
                                        """)
        self.assertEqual(queue, "ACDAB")
        self.assertEqual(runtimes, ','.join(sorted("A:3,B:8,C:2,D:4".split(","))))

    def test_9(self):
        queue, runtimes = run_scheduler("""
                                        A,1,2,7
                                        B,0,4,2
                                        C,1,2,2
                                        D,1,2,1
                                        """)
        self.assertEqual(queue, "ACDAB")
        self.assertEqual(runtimes, ','.join(sorted("A:3,C:2,D:4,B:8".split(","))))

    def test_10(self):
        queue, runtimes = run_scheduler("""
                                        A,0,0,5
                                        B,0,1,1
                                        C,0,3,1
                                        D,0,3,3
                                        E,0,4,1
                                        """)
        self.assertEqual(queue, "ABACEDA")
        self.assertEqual(runtimes, ','.join(sorted("A:6,B:0,C:0,D:2,E:0".split(","))))

    def test_10(self):
        queue, runtimes = run_scheduler("""
                                        A,0,0,3
                                        B,0,0,3
                                        C,1,0,2
                                        """)
        self.assertEqual(queue, "CAB")
        self.assertEqual(runtimes, ','.join(sorted("A:2,B:5,C:0".split(","))))
