# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""Managers package - API managers for different Jupyter Server endpoints."""

from jupyter_server_api.managers.contents import ContentsManager
from jupyter_server_api.managers.sessions import SessionsManager
from jupyter_server_api.managers.terminals import TerminalsManager
from jupyter_server_api.managers.kernelspecs import KernelSpecsManager
from jupyter_server_api.managers.kernels import KernelsManager
from jupyter_server_api.managers.execs import ExecsManager

__all__ = [
    "ContentsManager",
    "SessionsManager",
    "TerminalsManager", 
    "KernelSpecsManager",
    "KernelsManager",
    "ExecsManager",
]