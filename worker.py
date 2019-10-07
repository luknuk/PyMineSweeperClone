import traceback, sys
from PyQt5.QtCore import *
import traceback

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)

class Worker(QRunnable):
    '''
    Workers thread
    ( runs a subroutine on new thread, returns the result )

    Spins up a worker thread.
    :param callback: The function callback to run on this worker thread.
            Supplied args and kwargs will passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    '''
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        '''
        Runs the function, and passes the arguments.
        '''
        try:
            # Try run the function with the arguments
            result = self.fn(*self.args, **self.kwargs)
        except:
            # Return an error
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # Return the result of the process
            self.signals.result.emit(result)
        finally:
            # Send a signal that process is done
            self.signals.finished.emit()