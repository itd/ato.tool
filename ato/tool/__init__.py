from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
MessageFactory = MessageFactory('ato.tool')

from os import path
import_data = path.join(path.dirname(__file__), 'import_data')
