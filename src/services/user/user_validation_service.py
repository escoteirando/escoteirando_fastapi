from email_validator import validate_email, EmailNotValidError
from src.cross_cutting import Singleton


@Singleton
class UserValidationService:
    # TODO: Mover as funções de validação da classe UserService

    def __init__(self):
        self.pass_policy = dict(length=5,
                                uppercase=1,
                                numbers=1,
                                special=1,
                                nonletters=1)

    def is_valid_username(self, username) -> (bool, str):
        """ Validação do usuário

        8 a 20 caracteres [a-zA-z0-9.-_]
        """
        if not (8 <= len(username) <= 20):
            # Length: 8 to 20
            return False, 'Nome do usuário deve ter de 8 a 20 caracteres'

        for c in username:
            if ('A' <= c <= 'Z' or
                'a' <= c <= 'z' or
                '0' <= c <= '9' or
                    c in ['_', '-', '.']):
                continue
            return False, 'Caracter inválido ['+c+']'

        return True, 'Nome válido'

    def is_valid_email(self, email) -> (bool, str):
        try:
            # Validate.
            valid = validate_email(email)
            return True, valid.email

        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            return False, "Email inválido: {0} {1}".format(email, str(e))

    def is_valid_password(self, password) -> (bool, str):
        if not password or not isinstance(password, str):
            return False, "Não pode ser vazia"

        erros = []
        if len(password) < self.pass_policy['length']:
            erros.append(f'Tamanho mínimo: {self.pass_policy["length"]}')
        uc = nu = sp = nl = 0
        for c in password:
            if c.isdigit():
                nu += 1
            elif c in '!@#$%*()[]{}^~+=-_/*.,\<.>;:?':
                sp += 1
            elif c.isalpha() and c == c.upper():
                uc += 1
            elif c.isalpha():
                nl += 1

        if uc < self.pass_policy['uppercase']:
            erros.append(
                f'Mínimo de maiúsculas: {self.pass_policy["uppercase"]}')
        if nu < self.pass_policy['numbers']:
            erros.append(
                f'Mínimo de números: {self.pass_policy["numbers"]}')

        if sp < self.pass_policy['special']:
            erros.append(
                f'Mínimo de caracteres especiais: {self.pass_policy["special"]}')

        if nl < self.pass_policy['nonletters']:
            erros.append(
                f'Mínimo de não-letras: {self.pass_policy["nonletters"]}')

        if not erros:
            return True, 'Senha válida'
        return False, "Senha: "+", ".join(erros)
