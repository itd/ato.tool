from five import grok
from plone.directives import dexterity
from plone.directives import form
from zope import schema
from plone.app.textfield import RichText
from ato.tool import MessageFactory as _
from ato.tool.vocabulary import ControlTypeVocab


class IComplianceFamily(form.Schema):
    """
    A grouping of compliance controls
    """

    # title = schema.TextLine(
    #     title=_(u"Control family name"),
    #     required=True,
    # )
    #
    # description = schema.Text(
    #     title=_(u"Brief description"),
    #     required=False,
    # )

    info = RichText(
        title=_(u"Supporting Info"),
        description=_(u"""List any high-level issues regarding
            this control. Include links and references to other
            documents if appropriate."""),
        required=False,
    )

    controltype = schema.Choice(
        title=_(u"Control Type"),
        description=_(u"""."""),
        vocabulary=ControlTypeVocab,
        default=u"none"
    )


class ComplianceFamily(dexterity.Container):
    grok.implements(IComplianceFamily)

    # Add your class methods and properties here


class View(grok.View):
    grok.context(IComplianceFamily)
    grok.require('zope2.View')
    grok.name('view')

    def controltypetitle(self, fieldname="controltype"):
        """
        Need to display the Title of the vocabulary, not the value.
        I'd really like to make this some method on the view that
        can return a value from any vocab/fieldname.
        """
        #field = IComplianceFamily['controltype']
        field = IComplianceFamily[fieldname]
        vocab = field.vocabulary
        val = field.get(self.context)
        return vocab.by_token[val].title
