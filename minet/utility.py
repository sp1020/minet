
from multiprocessing import Process, Queue


class Manager:
    def __init__(self, f_job, n_worker=1):
        self.n_worker = n_worker
        self.f_job = f_job

        self.q_job = Queue()
        self.q_result = Queue()
        self.create_worker()

    def create_worker(self):
        for i in range(self.n_worker):
            p = Process(target=self.f_job, args=(self.q_job, self.q_result, ))
            p.start()
        print('%s workers were deployed' % self.n_worker)

    def fill_jobs(self, jobs):
        self.n_jobs = len(jobs)
        for j in jobs:
            self.q_job.put({'type': 'JOB', 'value': j})
        for i in range(self.n_worker):
            self.q_job.put({'type': 'CONTROL', 'value': 'END'})

    def analyze_result(self):
        res = []
        for i in range(self.n_jobs):
            res.append(self.q_result.get())
        return res
