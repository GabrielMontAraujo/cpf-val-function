import re
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    cpf = req.params.get('cpf')
    if not cpf:
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                "Por favor, forneça um CPF na query string ou no corpo da requisição.",
                status_code=400
            )
        else:
            cpf = req_body.get('cpf')

    if not cpf:
        return func.HttpResponse(
            "Por favor, forneça um CPF.",
            status_code=400
        )

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

    return func.HttpResponse(
        body=f'{{"cpf": "{cpf}", "valido": {str(is_valid).lower()}}}',
        status_code=200,
        mimetype="application/json"
    )
