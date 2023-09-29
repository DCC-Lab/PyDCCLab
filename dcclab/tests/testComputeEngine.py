import env
import unittest
from dcclab.analysis import *

def calculateFactorial(inputQueue, outputQueue):
    try:
        value = inputQueue.get_nowait()
        product = 1
        for i in range(value):
            product *= (i+1)
        outputQueue.put( (value,  product) )
    except Empty as err:
        pass # not an error

def slowCalculation(inputQueue, outputQueue):
    try:
        value = inputQueue.get_nowait()
        time.sleep(3)
        outputQueue.put( value )
    except Empty as err:
        pass # not an error

def processSimple(queue):
    while not queue.empty():
        try:
            (n, nfactorial) = queue.get_nowait()
            print('Just finished calculating {0}!'.format(n))
        except Empty as err:
            break # we are done


class MyTestCase(env.DCCLabTestCase):
    def testThreads1(self):
        N = 11
        print("Calculating n! for numbers 0 to {0} (every calculation is independent)".format(N - 1))
        print("======================================================================")

        print("Using threads: fast startup time appropriate for quick calculations")
        engine = ComputeEngine(useThreads=True)
        for i in range(N):
            engine.inputQueue.put(i)
        engine.compute(target=calculateFactorial)

    def testProcesses1(self):
        N = 11
        print("Using processes: long startup time appropriate for longer calculations")
        engine = ComputeEngine(useThreads=False)
        for i in range(N):
            engine.inputQueue.put(i)
        engine.compute(target=calculateFactorial)

    def testThreadsProcessTask(self):
        N = 11
        print("Using threads and replacing the processTaskResult function")
        engine = ComputeEngine(useThreads=True)
        for i in range(N):
            engine.inputQueue.put(i)
        engine.compute(target=calculateFactorial, processTaskResults=processSimple)
    @unittest.skip
    def testProcessesVeryLong(self):
        N = 11
        print("Using processes with very long calculations and timeout")
        engine = ComputeEngine(useThreads=False)
        for i in range(N):
            engine.inputQueue.put(i)
        engine.compute(target=slowCalculation, timeoutInSeconds=2)


if __name__ == '__main__':
    unittest.main()
