import sys
import traceback

from PyQt5.QtCore import (QObject, QRunnable,
                          pyqtSignal, pyqtSlot)


class WorkerSignals(QObject):
    """ Определяет сигналы, доступные из рабочего потока Worker(QRunnable)."""

    finish = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    """ Наследует от QRunnable, настройки рабочего потока обработчика, сигналов и wrap-up. """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        # print(self.fn)

        # print("\nfn=`{}`, \nargs=`{}`, kwargs=`{}`, \nself.signals=`{}`" \
        #       .format(fn, args, kwargs, self.signals))

        # == Добавьте обратный вызов в наши kwargs ====================================###
        kwargs['progress_callback'] = self.signals.progress
        # print("kwargs['progress_callback']->`{}`\n".format(kwargs['progress_callback']))

    @pyqtSlot()
    def run(self):

        try:
            # print(*self.args)
            result = self.fn(*self.args, **self.kwargs)

        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))

        else:  # если ошибок не была, испускаем сигнал .result и передаем результат `result`
            self.signals.result.emit(result)  # Вернуть результат обработки

        finally:
            self.signals.finish.emit()  # Done
