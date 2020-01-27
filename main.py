from zonaprop import Zonaprop
import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

zonaprop = Zonaprop()
lista_zonaprop = []
input_inmueble = None
input_barrio = None
input_ambientes = None
input_preciohasta = None

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

INMUEBLE, BARRIO, AMBIENTES, PRECIOHASTA = range(4)

def start(bot, context):
    reply_keyboard = [['Casa', 'Departamento'], ['PH', 'Locales Comerciales']]
    bot.message.reply_text('Bienvenido, seleciona el tipo de inmueble que esta buscando', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return INMUEBLE

def inmueble(bot, context):
    print("entre en tipoDeInbueble")
    print(bot.message.text)
    global input_inmueble
    input_inmueble = bot.message.text
    bot.message.reply_text("Ingrese el barrio/localidad o presione /skip para continuar", reply_markup=ReplyKeyboardRemove())
    return BARRIO

def barrio(bot, context):
    print("Entre a barrio")
    global input_barrio
    input_barrio = bot.message.text
    print(input_barrio)
    bot.message.reply_text('Ingrese la cantidad de ambientes o presione /skip para continuar')
    return AMBIENTES

def skip_barrio(bot, context):
    print("Entre a skip_barrio")
    bot.message.reply_text('Ingrese la cantidad de ambientes o presione /skip para continuar')
    return AMBIENTES

def ambientes(bot, context):
    print("Entre en ambientes")
    global input_ambientes
    input_ambientes = bot.message.text
    if not input_ambientes.isdigit():
        bot.message.reply_text('Error: Ingrese un valor numérico o presione /skip para continuar')
        return AMBIENTES
    bot.message.reply_text('Ingrese precio maximo o presione /skip para continuar')
    return PRECIOHASTA

def skip_ambientes(bot, context):
    print("Entre en skip_ambientes")
    bot.message.reply_text('Ingrese precio maximo sin puntos ni comas o presione /skip para continuar')
    return PRECIOHASTA

def precioHasta(bot, context):
    print("Entre en precioHasta")
    global input_preciohasta
    input_preciohasta = bot.message.text
    if not input_preciohasta.isnumeric():
        bot.message.reply_text("Error: Ingrese un valor numérico sin comas ni puntos.")
        return PRECIOHASTA(bot, context)
    bot.message.reply_text('Aguarde un momento mientras recopilamos la información. Esto puede tardar algunos minutos dependiendo de la cantidad de departamentos encontrados.')
    resultado(bot, context)
    return ConversationHandler.END

def skip_precioHasta(bot, context):
    print("ENTRE skip_precioHasta")
    bot.message.reply_text('Aguarde un momento mientras recopilamos la información. Esto puede tardar algunos minutos dependiendo de la cantidad de departamentos encontrados.')
    resultado(bot, context)
    return ConversationHandler.END

def resultado(bot, context):
    print("Entre a resultado")
    print(input_barrio, input_ambientes, input_preciohasta)
    zonaprop.BuscarDeptos(lista_zonaprop,inmueble=input_inmueble, barrio=input_barrio, ambientes=input_ambientes, precioHasta=input_preciohasta)
    tam_ls = len(lista_zonaprop)
    if tam_ls:
        bot.message.reply_text("Se encontraron " + str(tam_ls) + " resultados")
        for dep in lista_zonaprop:
            bot.message.reply_text(dep)
            print(dep)
    else:
        bot.message.reply_text('No se encontraron departamentos con esas caracteristicas')


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():

    bot = Updater("TOKEN", use_context=True)
    dp = bot.dispatcher

    # https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            INMUEBLE: [MessageHandler(Filters.regex('^(Casa|Departamento|PH|Locales Comerciales)$'), inmueble)],

            BARRIO: [MessageHandler(Filters.text, barrio),
                     CommandHandler('skip', skip_barrio)],

            AMBIENTES: [MessageHandler(Filters.text, ambientes),
                    CommandHandler('skip', skip_ambientes)],

            PRECIOHASTA: [MessageHandler(Filters.text, precioHasta),
                       CommandHandler('skip', skip_precioHasta)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    bot.start_polling()
    bot.idle()

if __name__ == '__main__':
    main()