# basic observer classes
class Observable:
    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(self, *args, **kwargs)


class Observer():
    def __init__(self, observable):
        self.callback = None
        observable.register_observer(self)

    # this function passed to registerCallBack should be the function invoked upon notify
    def registerCallback(self, function):
        self.callback = function

    def notify(self, observable, *args, **kwargs):
        self.callback()






# singleton subject object containing the observers, the subject should always be referenced through this class
class observerObject(object):
    class __observerObject:
        def __init__(self):
            self.subject = Observable()
    instance = None
    def __new__(cls):
        if not observerObject.instance:
            observerObject.instance = observerObject.__observerObject()
        return observerObject.instance

