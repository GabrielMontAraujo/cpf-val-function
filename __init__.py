import re

def main(req):
    cpf = req.params.get('cpf')
    if not cpf:
        return {
            'status': 400,
            'body': "Por favor, forneça um CPF."
        }

    def validar_cpf(cpf):
        cpf = re.sub(r'\D', '', cpf)

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = soma % 11
        if resto < 2:
            if int(cpf[9]) != 0:
                return False
        elif int(cpf[9]) != 11 - resto:
            return False

        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = soma % 11
        if resto < 2:
            if int(cpf[10]) != 0:
                return False
        elif int(cpf[10]) != 11 - resto:
            return False

        return True

    is_valid = validar_cpf(cpf)

    return {
        'status': 200,
        'body': {
            'cpf': cpf,
            'valido': is_valid
        }
    }
