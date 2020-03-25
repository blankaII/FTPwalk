#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 17:27:21 2020

original @author: Kasramvd

https://xbuba.com/questions/31465199
https://github.com/kasramvd/FTPwalk

modify: blankachang
"""

from os import path as ospath
import stat

class FTPWalk:
    """
    This class is contain corresponding functions for traversing the FTP
    servers using BFS algorithm.
    """
    def __init__(self, connection):
        self.connection = connection

    def listdir(self, _path):
        """
        return files and directory names within a path (directory)
        """

        file_list, dirs, nondirs = [], [], []
        try:
            self.connection.cwd(_path)
        except Exception as exp:
            print ("the current path is : ", self.connection.pwd(), exp.__str__(),_path)
            return [], []
        else:
            self.connection.retrlines('LIST', lambda x: file_list.append(x.split()))
            for info in file_list:
                ls_type, name = info[0], info[-1]
                if ls_type.startswith('d'):
                    dirs.append(name)
                else:
                    nondirs.append(name)
            return dirs, nondirs

    def walk(self, path='/'):
        """
        Walk through FTP server's directory tree, based on a BFS algorithm.
        """
        dirs, nondirs = self.listdir(path)
        yield path, dirs, nondirs
        for name in dirs:
            path = ospath.join(path, name)
            yield from self.walk(path)
            # In python2 use:
            # for path, dirs, nondirs in self.walk(path):
            #     yield path, dirs, nondirs
            self.connection.cwd('..')
            path = ospath.dirname(path)
            
class SFTPWalk:
    """
    base on https://github.com/kasramvd/FTPwalk::FTPWalk
    """
    def __init__(self, connection):
        self.connection = connection

    def listdir(self, _path):
        """
        return files and directory names within a path (directory)
        """

        dirs, nondirs = [], []
        try:
            self.connection.chdir(_path)
        except Exception as exp:
            print ("the current path is : ", self.connection.pwd(), exp.__str__(),_path)
            return [], []
        else:
            for entry in self.connection.listdir_attr():
                if stat.S_ISDIR(entry.st_mode):
                    dirs.append(entry.filename)
                else:
                    nondirs.append(entry.filename)
            return dirs, nondirs

    def walk(self, path='/'):
        """
        Walk through FTP server's directory tree, based on a BFS algorithm.
        """
        dirs, nondirs = self.listdir(path)
        yield path, dirs, nondirs
        for name in dirs:
            path = ospath.join(path, name)
            yield from self.walk(path)
            # In python2 use:
            # for path, dirs, nondirs in self.walk(path):
            #     yield path, dirs, nondirs
            self.connection.chdir('..')
            path = ospath.dirname(path)