from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from ato.tool import MessageFactory as _


# Interface class; used to define content-type schema.

class IReviewEvent(form.Schema, IImageScaleTraversable):
    """
    A specific ATO review event
    """

    details = RichText(
        title=_(u"Review Event Details"),
        description=_(u"Info about this specific review event."),
        required=False,
    )




class ReviewEvent(dexterity.Container):
    grok.implements(IReviewEvent)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# reviewevent_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    grok.context(IReviewEvent)
    grok.require('zope2.View')

    grok.name('view')