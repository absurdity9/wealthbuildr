import simplejson as json
from decimal import Decimal

data = {
    'value': Decimal('12.34')
}

json_data = json.dumps(data, use_decimal=True)
print(json_data)