# Copyright (c) 2025 Datalayer, Inc.
#
# BSD 3-Clause License

"""Managers package - API managers for different Jupyter Server endpoints."""

from jupyter_server_client.managers.contents import ContentsManager
from jupyter_server_client.managers.sessions import SessionsManager
from jupyter_server_client.managers.terminals import TerminalsManager
from jupyter_server_client.managers.kernelspecs import KernelSpecsManager
from jupyter_server_client.managers.kernels import KernelsManager

__all__ = [
    "ContentsManager",
    "SessionsManager",
    "TerminalsManager", 
    "KernelSpecsManager",
    "KernelsManager",
]