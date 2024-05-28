#!/usr/bin/python
# -*- coding: utf-8 -*-

def left_align(obj, offset: int = 0, char: str = "\t") -> str:
    return char * offset + obj
