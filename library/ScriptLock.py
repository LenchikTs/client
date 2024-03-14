#!/usr/bin/env python
# -*- coding:utf-8 -*-

#import tempfile
import fcntl
import os


__all__ = ( 'EScriptLock', 'CScriptLock')

class EScriptLock(Exception):
    pass


class CScriptLock:
    def __init__(self, name, block=True):
        self.name = name
        self.fd = None
        self.block = block


    def acquire(self, block=None):
        fullName = self.__getFileName()
        (path,filename) = os.path.split(fullName)
        if not os.path.exists(path):
            os.makedirs(path)
        self.fd = os.open(fullName, os.O_CREAT|os.O_RDWR, 0666)
        try:
            try:
                if block is None:
                    block = self.block
                flags = fcntl.LOCK_EX if block else fcntl.LOCK_EX|fcntl.LOCK_NB
                fcntl.flock(self.fd, flags)
            except IOError, e:
                if e.errno == 11 and not block:
                    return False
                raise
        except:
            os.close(self.fd)
            self.fd = None
            raise

        os.write(self.fd, '%d\n' % os.getpid())
        return True


    def release(self):
        if self.fd:
            os.unlink(self.__getFileName())
            os.close(self.fd)
            self.fd = None


    def __getFileName(self):
#        return '%s/%s.lock' % (tempfile.gettempdir(), self.name)
        return '%s/%s.lock' % ('/tmp', self.name)


    def __enter__(self):
        if not self.acquire():
            raise EScriptLock('Can not acquire %s' % self.__getFileName())
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


if __name__ == '__main__':

    import time

    with CScriptLock('labExchange/mylock', False):
        for t in xrange(10):
            print 'tick'
            time.sleep(1)
