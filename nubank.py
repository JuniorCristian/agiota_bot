import configparser
from pynubank import Nubank
import json
import datetime

config = configparser.ConfigParser()
config.read_file(open('config.ini'))

nu = Nubank()

nu.authenticate_with_refresh_token(config['NUBANK']['token'], config['NUBANK']['cert_path'])

# code = '123' #Código único da tansação é necessário para o get_pix_identifier
#
# data = nu.get_available_pix_keys()
#
# print(data['keys']) # Retorna lista de chaves cadastradas no Pix
#
# print(data['account_id']) # Retorna id da sua conta
#
# # No exemplo abaixo solicitamos uma cobrança de R$ 50,25 utilizando a primeira chave cadastrada
# money_request = nu.create_pix_payment_qrcode(data['account_id'], 1.00, data['keys'][0], code)
#
# # Irá printar o QRCode no terminal
# money_request['qr_code'].print_ascii()
#
# # Também é possível gerar uma imagem para ser enviada através de algum sistema
# # Nesse caso irá salvar um arquivo qr_code.png que pode ser escaneado pelo app do banco para ser pago
# # Salva o nome do arquivo com o código do identifier
# qr = money_request['qr_code']
# img = qr.make_image()
# img.save(code+'.png')
#
# # Além do QRCode também há uma URL para pagamento
# print(money_request)
# print(money_request['payment_url'])

account = nu.get_account_feed_paginated()

print(account)

minDate = datetime.datetime(2023, 2, 1)

totalUltimoMes = list(
    filter(lambda x: x['node']['tags'] is not None and 'money-in' in x['node']['tags'], account['edges']))

lastDateList = totalUltimoMes[len(totalUltimoMes) - 1]['node']['postDate'].split('-')
lastDate = datetime.datetime(int(lastDateList[0]), int(lastDateList[1]), int(lastDateList[2]))
getNextPage = lastDate > minDate and account['pageInfo']['hasNextPage']

while getNextPage:
    cursor = account['edges'][-1]['cursor']
    # Aqui recuperamos a próxima página
    account = nu.get_account_feed_paginated(cursor)
    totalUltimoMes = totalUltimoMes + list(
        filter(lambda x: x['node']['tags'] is not None and 'money-in' in x['node']['tags'], account['edges']))
    lastDateList = totalUltimoMes[len(totalUltimoMes) - 1]['node']['postDate'].split('-')
    lastDate = datetime.datetime(int(lastDateList[0]), int(lastDateList[1]), int(lastDateList[2]))
    getNextPage = lastDate > minDate and account['pageInfo']['hasNextPage']

totalUltimoMes = list(filter(
    lambda x: datetime.datetime(int(x['node']['postDate'].split('-')[0]), int(x['node']['postDate'].split('-')[1]),
                                int(x['node']['postDate'].split('-')[2])) >= minDate and 'money-in' in x['node'][
                  'tags'], totalUltimoMes))

print(list(filter(lambda x: 'Christopher Robert Oliveira de Meira' in x['node']['detail'], totalUltimoMes)))
