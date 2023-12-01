import datetime

def parse_endereco(data):
    return f"{data.get('logradouro')}, {data.get('numero')}, {data.get('municipio')}-{data.get('uf')}"

def parse_date(date_str, dtformat):
    return datetime.datetime.strptime(date_str, dtformat).date()