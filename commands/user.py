
class User:
    def __init__(self, user_id, bomDia, boaNoite, mensagens, comandos, capturados, xp, level):
        self._user_id = user_id
        self._bomDia = bomDia
        self._boaNoite = boaNoite
        self._mensagens = mensagens
        self._comandos = comandos
        self._capturados = capturados
        self._xp = xp
        self._level = level

#region ## Get e setter's

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def bomDia(self):
        return self._bomDia

    @bomDia.setter
    def bomDia(self, value):
        self._bomDia = value

    @property
    def boaNoite(self):
        return self._boaNoite

    @boaNoite.setter
    def boaNoite(self, value):
        self._boaNoite = value

    @property
    def mensagens(self):
        return self._mensagens

    @mensagens.setter
    def mensagens(self, value):
        self._mensagens = value


    @property
    def comandos(self):
        return self._comandos

    @comandos.setter
    def comandos(self, value):
        self._comandos = value

    @property
    def capturados(self):
        return self._capturados

    @capturados.setter
    def capturados(self, value):
        self._capturados = value

    @property
    def xp(self):
        return self._xp

    @xp.setter
    def xp(self, value):
        self._xp = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value


    # Repita os métodos @property e @atributo.setter para outros atributos

#endregion

