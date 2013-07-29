from five import grok
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from ato.tool import MessageFactory as _


# class ComplianceFamilyVocabulary(object):
#     grok.implements(IVocabularyFactory)
#
#     def __call__(self, context):
#         #catalog = getToolByName(context, 'portal_catalog')
#         #context = aq_inner(self.context)
#         #context = aq_inner(self.context)
#         #putils = getToolByName(context, 'plone_utils')
#
#         # List all ato.tool.compliancefamily in this folder
#         brains = self.listFolderContents(
#             contentFilter={"portal_type": "ato.tool.compliancefamily"})
#         terms = []
#
#         if brains is not None:
#             for ob in brains:
#                 terms.append(SimpleVocabulary.createTerm(ob.id, ob.Title))
#
#         return SimpleVocabulary(terms)


ControlBaselineVocab = SimpleVocabulary(
            [SimpleTerm(value=0, title=_(u'Not Selected')),
             SimpleTerm(value=1, title=_(u'Low')),
             SimpleTerm(value=2, title=_(u'Moderate')),
             SimpleTerm(value=3, title=_(u'High'))
             ])

ControlPriorityVocab = SimpleVocabulary(
            [SimpleTerm(value=0, title=_(u'P0')),
             SimpleTerm(value=1, title=_(u'P1')),
             SimpleTerm(value=2, title=_(u'P2')),
             SimpleTerm(value=3, title=_(u'P3'))
             ])

ControlTypeVocab  = SimpleVocabulary(
            [SimpleTerm(value=u'MC', title=_(u'Management Control')),
             SimpleTerm(value=u'OC', title=_(u'Operational Control')),
             SimpleTerm(value=u'TC', title=_(u'Technical Control')),
             SimpleTerm(value=u'none', title=_(u'- None Selected -')),
             ])

# how about using the Configuration Registry instead?

#grok.global_utility(ControlPriorityVocab,
#                    name=u"ato.tool.ControlPriorityVocab")

# grok.global_utility(ComplianceFamilyVocabulary,
#                     name=u"ato.tool.ComplianceFamilies")
