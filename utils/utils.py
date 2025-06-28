import numbers


def valida_input_eh_num(entrada):
    entrada_eh_num = False

    while not entrada_eh_num:
        if isinstance(int(entrada), numbers.Number) and len(entrada) == 1:
                    entrada_eh_num = True
                    return entrada_eh_num
        else:
            print("Por favor, insira apenas um número.")