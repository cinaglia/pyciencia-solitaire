from distutils.core import setup, Extension

module1 = Extension('estruturas',
                    sources = ['estruturas.c'])

setup (name = 'estruturas',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])