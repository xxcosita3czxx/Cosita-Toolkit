import os  # noqa: D100
from unittest.mock import MagicMock, mock_open, patch

import pytest
import requests

from cosita_toolkit import (
    GithubApi,
    MemMod,
    Networking,
    OSspecific,
    PokeAPI,
    Upload,
)


def test_networking_get_lan_ip():
    """Test for getting local internet ip."""
    with patch('socket.socket') as mock_socket:
        mock_socket.return_value.getsockname.return_value = ('192.168.1.2',)
        result = Networking.get_lan_ip()
        assert result == '192.168.1.2'
