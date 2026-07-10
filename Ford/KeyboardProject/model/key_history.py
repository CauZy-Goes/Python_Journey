"""
KeyHistory
----------
Model que representa o histórico de uma tecla pressionada.
"""
 
import socket
from dataclasses import dataclass, field
from datetime import datetime
 
 
def get_local_ip() -> str:
    """Retorna o IP local da máquina que está rodando o script."""
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        return "127.0.0.1"
 
 
#  Gera automaticamente: __init__ (equivalente ao construtor), __repr__ (equivalente ao toString()), __eq__ (equivalente ao equals()).
@dataclass
class KeyHistory:
    key: str
    press_time: datetime = field(default_factory=datetime.now)
    ip_address: str = field(default_factory=get_local_ip)
    id: Optional[int] = field(default=None)  # preenchido pelo banco após o insert
 
    # def __post_init__(self):
    #     # Gera o ID a partir do press_time no formato HHMMDDMMYYYY
    #     self.id = self.press_time.strftime("%H%M%d%m%Y")
 
    def __repr__(self):
        return (
            f"KeyHistory(id={self.id}, key='{self.key}', "
            f"press_time={self.press_time:%d/%m/%Y %H:%M:%S}, "
            f"ip_address='{self.ip_address}')"
        )
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "key": self.key,
            "press_time": self.press_time.isoformat(),
            "ip_address": self.ip_address,
        }