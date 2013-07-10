from five import grok
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory


class ComplianceFamilyVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        #catalog = getToolByName(context, 'portal_catalog')
        #context = aq_inner(self.context)
        #context = aq_inner(self.context)
        #putils = getToolByName(context, 'plone_utils')

        # List all ato.tool.compliancefamily in this folder
        brains = self.listFolderContents(
                contentFilter={"portal_type": "ato.tool.compliancefamily"}
                )
        terms = []

        if brains is not None:
            for ob in brains:
                terms.append(SimpleVocabulary.createTerm(ob.id, ob.Title))

        return SimpleVocabulary(terms)

grok.global_utility(ComplianceFamilyVocabulary,
                    name=u"ato.tool.ComplianceFamilies")
