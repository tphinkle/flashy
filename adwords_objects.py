


ADWORDS_REPORT_FIELD_NAMES = {
    'AD_PERFORMANCE_REPORT': ADWORDS_AD_PERFORMANCE_REPORT_FIELD_NAMES,
    'ADGROUP_PERFORMANCE_REPORT': ADWORDS_ADGROUP_PERFORMANCE_REPORT_FIELD_NAMES,
    'KEYWORDS_PERFORMANCE_REPORT': ADWORDS_KEYWORDS_PERFORMANCE_REPORT_FIELD_NAMES
    }


CAMPAIGN_GET_FIELDS = ['Id', 'CampaignGroupId', 'Name', 'Status', 'ServingStatus', 'StartDate', 'EndDate', 'AdServingOptimizationStatus',\
 'Settings', 'AdvertisingChannelType', 'Labels',\
 'CampaignTrialType', 'BaseCampaignId', 'TrackingUrlTemplate', 'FinalUrlSuffix', 'UrlCustomParameters', 'SelectiveOptimization']

ADGROUP_GET_FIELDS = ['Id', 'CampaignId', 'CampaignName', 'Name', 'Status', 'Settings', 'Labels',\
'ContentBidCriterionTypeGroup', 'BaseCampaignId', 'BaseAdGroupId', 'TrackingUrlTemplate', 'FinalUrlSuffix', 'UrlCustomParameters', 'AdGroupType']



#AD_GET_FIELDS




ADGROUPCRITERION_GET_FIELDS = ['AdGroupId', 'CriterionUse', 'Text', 'FinalUrls', 'BaseCampaignId']








class TextAd(object):

    get_fields = ['AdGroupId', 'Status', 'PolicySummary', 'Labels', 'Id', 'Url', 'DisplayUrl', 'CreativeFinalUrls', 'CreativeFinalMobileUrls', 'CreativeFinalAppUrls',\
     'DevicePreference', 'Headline', 'Description1', 'Description2']

    def __init__(self):
        pass



class ExpandedTextAd(object):
    get_fields = ['AdGroupId', 'Status', 'PolicySummary', 'Labels', 'Id', 'Url', 'DisplayUrl', 'CreativeFinalUrls', 'CreativeFinalMobileUrls', 'CreativeFinalAppUrls',\
     'DevicePreference', 'Headline', 'Description1', 'Description2']

    def __init__(self, customer_id, adwords_response):

        default_value = 'NONE'

        self._customer_id = customer_id
        self._ad_group_id = adwords_response.get('adGroupId', default_value)
        self._id = adwords_response.get('ad', {}).get('id', default_value)
        self._final_url = adwords_response.get('ad', {}).get('finalUrls', [default_value])[0]
        self._type = adwords_response.get('ad', {}).get('type', default_value)
        self._headline_1 = adwords_response.get('ad', {}).get('headlinePart1', default_value)
        self._headline_2 = adwords_response.get('ad', {}).get('headlinePart2', default_value)
        self._description = adwords_response.get('ad', {}).get('description', default_value)
        self._path_1 = adwords_response.get('ad', {}).get('path1', default_value)
        self._path_2 = adwords_response.get('ad', {}).get('path2', default_value)
        self._status = adwords_response.get('status', default_value)
        self._combined_approval_status = adwords_response.get('policySummary', {}).get('combinedApprovalStatus', default_value)
        self._labels = adwords_response.get('labels', default_value)



    def to_dict(self):
        ad_dict = {}
        ad_dict['customer_id'] = self._customer_id
        ad_dict['ad_group_id'] = self._ad_group_id
        ad_dict['id'] = self._id
        ad_dict['final_url'] = self._final_url
        ad_dict['type'] = self._type
        ad_dict['headline_1'] = self._headline_1
        ad_dict['headline_2'] = self._headline_2
        ad_dict['description'] = self._description
        ad_dict['path_1'] = self._path_1
        ad_dict['path_2'] = self._path_2
        ad_dict['status'] = self._status
        ad_dict['combined_approval_status'] = self._combined_approval_status
        ad_dict['labels'] = self._labels
        return ad_dict



class ResponsiveSearchAd(object):
    get_fields = ['AdGroupId', 'Status', 'PolicySummary', 'Labels',
    'Id', 'Url', 'DisplayUrl', 'CreativeFinalUrls', 'CreativeFinalMobileUrls', 'CreativeFinalAppUrls',
     'DevicePreference', 'HeadlinePart1', 'HeadlinePart2', 'Description',
    'Path1', 'Path2']


    def __init__(self, customer_id, adwords_response):
        pass



class Label(object):
    get_fields = ['LabelId', 'LabelName', 'LabelStatus']

class LabelPrototype(object):

    def __init__(self, name):

        self.name = name

    def format_add_operand(self):
        operand = {
            'xsi_type': 'TextLabel',
            'name': self.name
            }

        return operand




class Keyword(object):

    get_fields = ['Id', 'CriteriaType', 'KeywordMatchType', 'KeywordText', 'FinalUrls']

class KeywordPrototype(object):
    def __init__(self, adGroupId, matchType, text, finalUrls):
        self.adGroupId = AdGroupId
        self.matchType = matchType
        self.text = text
        self.finalUrls = finalUrls
