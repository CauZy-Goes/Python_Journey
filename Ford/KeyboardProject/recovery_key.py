from datetime import timedelta, datetime
from Service.log_service import rebuild_text

fim = datetime.now() 
inicio = fim - timedelta(minutes=30)

print(rebuild_text(inicio, fim))