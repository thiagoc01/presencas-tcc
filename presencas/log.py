from logging.config import dictConfig
import re, logging

'''
    Configura o log da aplicação para escrever no console e para um arquivo em /var/log/presencas.log.
    Adiciona o nível SUCCESS com número 15 no módulo de log do Python.
    Com a classe FiltroRemovedorDataWerkzeug, retira o carimbo de data e hora dos logs HTTP do Werkzeug.
    Com a classe FormatadorCorSucessoErroCritico, formata a data e hora originais para dia/mês/ano hora:min:segundo offset-UTC,
    além de adicionar cores para SUCCESS, ERROR e CRITICAL.
'''

def configura_log():
    logging.SUCCESS = 15    # Definido para esse projeto para que seja impresa uma string em verde nos logs

    class FiltroRemovedorDataWerkzeug(logging.Filter):
        padrao = re.compile(r' - - \[.+?] "')

        def filter(self, record):

            record.msg = self.padrao.sub(' - "', record.msg)

            return True
        

    class FormatadorCorSucessoErroCritico(logging.Formatter):
        verde = "\033[92m"
        vermelho = "\033[91m"
        normal = "\033[00m"
        formato = "[%(asctime)s] %(levelname)s %(message)s"
        formato_data_hora = "%d/%m/%Y %H:%M:%S %z"

        def format(self, record):
            
            if record.levelno == logging.SUCCESS:

                formatador = logging.Formatter(self.verde + self.formato + self.normal, self.formato_data_hora)

            elif record.levelno == logging.ERROR or record.levelno == logging.CRITICAL:

                formatador = logging.Formatter(self.vermelho + self.formato + self.normal, self.formato_data_hora)

            else:

                formatador = logging.Formatter(self.formato, self.formato_data_hora)

            return formatador.format(record)


    dictConfig(
        {
            "version": 1,

            "formatters": {

                "default": {

                    "()": FormatadorCorSucessoErroCritico
                }
            },

            "handlers": {

                "console": {

                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default"
                },

                "arquivo": {

                    "class" : "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": "/var/log/presencas.log",
                    "maxBytes": 125000000,
                    "backupCount": 5,
                    "encoding": "utf-8"
                }

            },

            "filters" : {

                "removedor_data_werkzeug" : {

                    "()" : FiltroRemovedorDataWerkzeug
                }
            },

            "root": {"level": "DEBUG", "handlers": ["console", "arquivo"]},

            "loggers" : {

                "werkzeug" : {
                    "level": "DEBUG", "handlers": ["console", "arquivo"],
                    "filters": ["removedor_data_werkzeug"], "propagate": False
                }
            }
        }
    )

    logging.addLevelName(logging.SUCCESS, "SUCCESS")