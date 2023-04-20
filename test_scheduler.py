from unittest import TestCase

from scheduler import Task, Scheduler, MultilevelScheduler


def run_scheduler(tasks: str):
    Task.reset()
    Scheduler.reset()
    scheduler = MultilevelScheduler()
    for task in tasks.split():
        scheduler.add_task(Task(task))
    scheduler.run()
    return Task.queue, Task.get_wait_times()


class SchedulerTest(TestCase):
    def test_1(self):
        queue, wait_times = run_scheduler('A,0,0,6 B,0,1,5 C,1,5,2 D,1,10,1')
        self.assertEqual(queue, 'ACABDB')
        self.assertEqual(wait_times, 'A:2,B:8,C:0,D:0')

    def test_2(self):
        queue, wait_times = run_scheduler('A,1,2,7 B,1,2,3')
        self.assertEqual(queue, 'ABABA')
        self.assertEqual(wait_times, 'A:3,B:4')

    def test_3(self):
        queue, wait_times = run_scheduler('Q,0,5,8 P,1,7,2')
        self.assertEqual(queue, 'QPQ')
        self.assertEqual(wait_times, 'Q:2,P:0')

    def test_4(self):
        queue, wait_times = run_scheduler('A,0,0,5 B,0,0,4 C,0,1,3 D,0,2,1')
        self.assertEqual(queue, 'BDBCA')
        self.assertEqual(wait_times, 'A:8,B:1,C:4,D:0')

    def test_5(self):
        queue, wait_times = run_scheduler('A,0,0,3 B,1,0,2 C,0,3,3 D,1,4,1')
        self.assertEqual(queue, 'BADAC')
        self.assertEqual(wait_times, 'A:3,B:0,C:3,D:0')

    def test_6(self):
        queue, wait_times = run_scheduler('A,0,0,5 B,0,1,3 C,1,1,1 D,0,4,1 E,1,3,2')
        self.assertEqual(queue, 'ACBEDBA')
        self.assertEqual(wait_times, 'A:7,B:4,C:0,E:0,D:1')

    def test_7(self):
        queue, wait_times = run_scheduler('A,1,3,5 D,1,6,1')
        self.assertEqual(queue, 'ADA')
        self.assertEqual(wait_times, 'A:1,D:1')

    def test_8(self):
        queue, wait_times = run_scheduler('A,1,2,7 B,0,4,2 C,1,2,2 D,1,2,1')
        self.assertEqual(queue, 'ACDAB')
        self.assertEqual(wait_times, 'A:3,C:2,D:4,B:8')

    def test_9(self):
        queue, wait_times = run_scheduler('A,0,0,5 B,0,1,1 C,0,3,1 D,0,3,3 E,0,4,1')
        self.assertEqual(queue, 'ABACEDA')
        self.assertEqual(wait_times, 'A:6,B:0,C:0,D:2,E:0')

    def test_10(self):
        queue, wait_times = run_scheduler('A,0,0,3 B,0,0,3 C,1,0,2')
        self.assertEqual(queue, 'CAB')
        self.assertEqual(wait_times, 'A:2,B:5,C:0')

    def test_11(self):
        queue, wait_times = run_scheduler('A,1,3,3 B,0,3,5 C,0,4,5 D,1,6,1 E,0,9,1')
        self.assertEqual(queue, 'ADBEBC')
        self.assertEqual(wait_times, 'A:0,B:5,C:9,D:0,E:0')

    def test_12(self):
        queue, wait_times = run_scheduler('A,1,0,6 B,1,1,5 C,0,5,5 D,0,7,2')
        self.assertEqual(queue, 'ABABABDC')
        self.assertEqual(wait_times, 'A:4,B:5,C:8,D:4')

    def test_13(self):
        queue, wait_times = run_scheduler(
            'A,1,2,2 B,0,5,4 C,1,7,2 D,1,9,2 E,1,12,1 F,1,14,6 G,0,17,1 H,0,17,1 I,1,17,2')
        self.assertEqual(queue, 'ABCDBEBFIFGH')
        self.assertEqual(wait_times, 'A:0,B:5,C:0,D:0,E:0,F:2,G:5,H:6,I:1')

    def test_14(self):
        queue, wait_times = run_scheduler('A,0,2,4 B,0,4,1 C,0,4,2 D,0,4,2 E,0,4,2')
        self.assertEqual(queue, 'ABCDEA')
        self.assertEqual(wait_times, 'A:7,B:0,C:1,D:3,E:5')

    def test_15(self):
        queue, wait_times = run_scheduler('A,1,1,5 B,1,1,1 C,1,2,6 D,0,3,2')
        self.assertEqual(queue, 'ABCACACD')
        self.assertEqual(wait_times, 'A:5,B:2,C:5,D:10')

    def test_16(self):
        queue, wait_times = run_scheduler('A,1,2,4 B,1,5,4 C,1,5,1 D,1,7,1 E,0,10,2 F,1,10,2 G,0,13,3')
        self.assertEqual(queue, 'ABCDBFEG')
        self.assertEqual(wait_times, 'A:0,B:3,C:3,D:2,E:4,F:2,G:3')

    def test_17(self):
        queue, wait_times = run_scheduler('A,1,2,3 B,0,0,2 C,0,2,3 D,1,2,2 E,1,1,3')
        self.assertEqual(queue, 'BEADEABC')
        self.assertEqual(wait_times, 'B:8,E:4,A:4,C:8,D:3')

    def test_18(self):
        queue, wait_times = run_scheduler('A,1,3,1 B,1,6,1 C,0,6,2 D,1,9,22 E,1,12,6 F,1,15,1')
        self.assertEqual(queue, 'ABCDEDFEDED')
        self.assertEqual(wait_times, 'A:0,B:0,C:1,D:7,E:6,F:2')

    def test_19(self):
        queue, wait_times = run_scheduler('A,1,1,5 B,1,2,2 C,1,3,5 D,1,4,1 E,0,4,8 F,0,7,1 G,0,1,10')
        self.assertEqual(queue, 'ABCADCACFEG')
        self.assertEqual(wait_times, 'A:7,G:22,B:1,C:6,D:5,E:11,F:7')

    def test_20(self):
        queue, wait_times = run_scheduler('A,0,1,1 B,1,3,3 C,0,3,5 D,0,3,1 E,1,3,2 F,1,6,1 G,1,8,1')
        self.assertEqual(queue, 'ABEBFGDC')
        self.assertEqual(wait_times, 'A:0,B:2,C:8,D:7,E:2,F:2,G:1')

    def test_21(self):
        queue, wait_times = run_scheduler('A,0,2,2 B,0,4,5 C,1,5,3 D,0,6,4 E,1,7,4')
        self.assertEqual(queue, 'ABCECEBD')
        self.assertEqual(wait_times, 'A:0,B:7,C:2,D:10,E:1')

    def test_22(self):
        queue, wait_times = run_scheduler('A,1,1,3 B,0,0,3 C,1,1,2 D,0,1,2 E,0,1,3')
        self.assertEqual(queue, 'BACADBE')
        self.assertEqual(wait_times, 'B:7,A:2,C:2,D:5,E:9')
