"""Baják Levente Imre, B5FWY3, 2023.04.20."""


class Task:
    """Taszkokat megvalósító osztály."""

    queue = ""
    runtimes = []

    @staticmethod
    def reset():
        """Statikus változók visszaállítása az alapértelmezett értékre"""
        Task.queue = ""
        Task.runtimes = []

    def __init__(self, input_str: str):
        """
        Taszk konstruktor. Elvárt formátum (vesszővel elválasztva):
        * a taszk betűjele (A, B, C...)
        * a taszk prioritása (0 vagy 1)
        * a taszk indítási ideje (egész szám >= 0), a következő időszeletben már futhat (0: az ütemező
          indításakor már létezik), azonos ütemben beérkező új taszkok esetén az ABC-sorrend dönt
        * a taszk CPU-löketideje (egész szám >= 1)
        :param input_str: A taszk adatait tartalmazó szöveg.
        """
        input_list = input_str.strip().split(',')

        if len(input_list) != 4 or not all(v.isdigit() for v in input_list[1:]):
            raise ValueError('A taszk adatai hibásak!')

        self.name = input_list[0].strip().upper()
        assert len(self.name) == 1 and self.name.isupper(), "A taszk betűjele egy nagybetű kell, hogy legyen!"
        self.priority = int(input_list[1].strip())
        assert self.priority in {0, 1}, 'A taszk prioritása 0 vagy 1 lehet!'
        self.arrival = int(input_list[2].strip())
        assert self.arrival >= 0, 'A taszk indítási ideje legalább 0 kell, hogy legyen!'
        self.remaining = int(input_list[3].strip())
        assert self.remaining >= 1, 'A taszk CPU-löketideje legalább 1 kell, hogy legyen!'
        self.wait = 0

    def __repr__(self):
        """Taszk megjelenítése szövegként."""
        return f'{self.name},{str(self.priority)},{str(self.arrival)},{str(self.remaining)}'

    def tick(self):
        """Taszk futtatása egy időszeletig."""
        if self.remaining > 0:
            if len(Task.queue) == 0 or Task.queue[-1] != self.name:
                Task.queue += self.name
            self.remaining -= 1
            if self.remaining == 0:
                Task.runtimes.append((self.name, str(self.wait)))


class Scheduler:
    """Taszk ütemezők ősosztálya."""
    time = 0

    @staticmethod
    def reset():
        """Statikus változók visszaállítása az alapértelmezett értékre."""
        Scheduler.time = 0

    def __init__(self):
        self.task_queue = []
        self.future_tasks = []
        self.current_task = None

    def add_task(self, task: Task):
        """
        Taszk hozzáadása az ütemezőhőz.
        :param task: az ütemezőhöz hozzáadandó taszk
        """
        self.future_tasks.append(task)

    def tick(self):
        """A soron következő taszk futtatása."""
        ...

    def finished(self):
        """Eldönti, hogy van-e még futó vagy várakozó taszk."""
        return not (self.task_queue or self.current_task or self.future_tasks)

    def run(self):
        """Ütemező indítása."""
        while not self.finished():
            Scheduler.time += 1
            self.tick()


class RoundRobinScheduler(Scheduler):
    """Round Robin (RR) ütemezőket megvalósító osztály."""

    def __init__(self, time_slice: int = 2):
        """
        Round Robin ütemező konstruktor.
        :param time_slice: A Round Robin ütemező időszelete
        """
        super().__init__()
        self.time_slice = time_slice
        self.task_time = 0

    def add_task(self, task: Task):
        super().add_task(task)
        self.future_tasks.sort(key=lambda x: x.name)
        self.future_tasks.sort(key=lambda x: x.arrival)

    def update(self):
        """A soron következő taszkok sorba állítása."""
        for task in self.future_tasks.copy():
            if task.arrival < Scheduler.time:
                self.task_queue.append(task)
                self.future_tasks.remove(task)

    def next_task(self):
        """A soron következő taszk meghatározása."""
        self.task_time = 0
        self.update()
        if not self.task_queue:
            return None

        if not self.current_task:
            self.current_task = self.task_queue.pop(0)
        else:
            self.task_queue.append(self.current_task)
            self.current_task = self.task_queue.pop(0)

        return self.current_task

    def tick(self):
        if not self.current_task or self.task_time == self.time_slice:
            self.next_task()
        if self.current_task:
            self.current_task.tick()
            for task in self.task_queue:
                task.wait += 1
            self.task_time += 1
            if self.current_task.remaining == 0:
                self.current_task = None


class SRTFScheduler(Scheduler):
    """Shortest Remaining Time First (SRTF) ütemezőket megvalósító osztály."""

    def add_task(self, task):
        super().add_task(task)
        self.future_tasks.sort(key=lambda x: x.name)
        self.future_tasks.sort(key=lambda x: x.arrival)

    def update(self):
        """A soron következő taszkok sorba állítása."""
        for task in self.future_tasks.copy():
            if task.arrival < Scheduler.time:
                self.task_queue.append(task)
                self.future_tasks.remove(task)

    def get_shortest(self):
        """
        A legelső legkisebb hátralévő idővel rendelkező taszk megkeresése a taszk sorban.
        Nem távolítja el a taszkot a taszk sorból.
        :return: a legelső legkisebb hátralévő idővel rendelkező taszk
        """
        shortest = self.task_queue[0]
        for task in self.task_queue:
            if task.remaining < shortest.remaining:
                shortest = task
        return shortest

    def next_task(self):
        """A soron következő taszk meghatározása."""
        self.update()
        if not self.task_queue:
            return None

        if not self.current_task:
            self.current_task = self.get_shortest()
            self.task_queue.remove(self.current_task)
        else:
            if self.current_task.remaining > self.get_shortest().remaining:
                self.task_queue.append(self.current_task)
                self.current_task = self.get_shortest()
                self.task_queue.remove(self.current_task)
        return self.current_task

    def tick(self):
        self.next_task()
        if self.current_task:
            self.current_task.tick()
            for task in self.task_queue:
                task.wait += 1
            if self.current_task.remaining == 0:
                self.current_task = None


class MultilevelScheduler:
    """Kétszintű ütemezőket megvalósító osztály."""

    def __init__(self, level1=RoundRobinScheduler(2), level0=SRTFScheduler()):
        """
        Kétszintű ütemező konstruktor.
        :param level1: magas prioritású taszkok ütemezője
        :param level0: alacsony prioritású taszkok ütemezője
        """
        self.level1 = level1
        self.level0 = level0

    def add_task(self, task):
        """
        Taszk hozzáadása az ütemezőhőz.
        :param task: az ütemezőhöz hozzáadandó taszk
        """
        if task.priority == 1:
            self.level1.add_task(task)
        else:
            self.level0.add_task(task)

    def tick(self):
        """A soron következő taszk futtatása."""
        self.level1.update()
        self.level0.update()
        if self.level1.task_queue or self.level1.current_task:
            self.level1.tick()
            if self.level0.current_task:
                self.level0.task_queue.append(self.level0.current_task)
                self.level0.current_task = None
            for task in self.level0.task_queue:
                task.wait += 1
        else:
            self.level0.tick()

    def finished(self):
        """Eldönti, hogy van-e még futó vagy várakozó taszk."""
        return self.level0.finished() and self.level1.finished()

    def run(self):
        """Ütemező indítása."""
        while not self.finished():
            Scheduler.time += 1
            self.tick()


def main():
    scheduler = MultilevelScheduler()
    while True:
        try:
            line = input()
            if line == "":
                break
            try:
                scheduler.add_task(Task(line))
            except Exception as e:
                print(e)
        except EOFError:
            break

    scheduler.run()

    print(Task.queue)
    Task.runtimes.sort(key=lambda x: x[0])
    print(','.join([':'.join(v) for v in Task.runtimes]))


if __name__ == "__main__":
    main()
