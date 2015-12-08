
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

    def registerCallback(self, function):
        self.callback = function


    def notify(self, observable, *args, **kwargs):
        print('Got', args, kwargs, 'From', observable)
        self.callback()






#singleton subject object containing the observers
class observerObject(object):
    class __observerObject:
        def __init__(self):
            self.subject = Observable()
    instance=None
    def __new__(cls):
        if not observerObject.instance:
            observerObject.instance = observerObject.__observerObject()
        return observerObject.instance

