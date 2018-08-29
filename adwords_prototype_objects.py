





class ResponsiveSearchAdPrototype(object):
    def __init__(self, adGroupId, headlineAssetLinks, descriptionAssetLinks, path1, path2, finalUrls):

        self.validate_fields(adGroupId, headlineAssetLinks, descriptionAssetLinks, path1, path2, finalUrls)
        self.adGroupId = adGroupId
        self.headlineAssetLinks = headlineAssetLinks
        self.descriptionAssetLinks = descriptionAssetLinks
        self.path1 = path1
        self.path2 = path2
        self.finalUrls = finalUrls


    def format_add_operand(self):
        operand = {
            'xsi_type': 'AdGroupAd',
            'adGroupId': self.adGroupId,
            'ad': {
                'xsi_type': 'ResponsiveSearchAd',
                'headlines': [{
                    'asset': {
                        'xsi_type': 'TextAsset',
                        'assetText': self.headlineAssetLinks[i]['assetText']
                        },
                    'pinnedField': self.headlineAssetLinks[i]['pinnedField']
                    } for i in range(len(self.headlineAssetLinks))],

                'descriptions': [{
                    'asset': {
                        'xsi_type': 'TextAsset',
                        'assetText': self.descriptionAssetLinks[i]['assetText']
                        },
                    'pinnedField': self.descriptionAssetLinks[i]['pinnedField']
                    } for i in range(len(self.descriptionAssetLinks))],



                'path1': self.path1,
                'path2': self.path2,
                'finalUrls': [self.finalUrls]
                },
            'status': 'PAUSED'
            }

        return operand

    def validate_fields(self, adGroupId, headlineAssetLinks, descriptionAssetLinks, path1, path2, finalUrls):
        # Check individual fields
        self.validate_adGroupId(adGroupId)
        self.validate_headlineAssetLinks(headlineAssetLinks)
        self.validate_descriptionAssetLinks(descriptionAssetLinks)
        self.validate_path1(path1)
        self.validate_path2(path2)
        self.validate_finalUrls(finalUrls)

    def validate_adGroupId(self, adGroupId):
        if type(adGroupId) != str:
            raise TypeError('adGroupId must be string!', adGroupId)

    def validate_headlineAssetLinks(self, headlineAssetLinks):
        if type(headlineAssetLinks) != list:
            raise TypeError('headlineAssetLink must be list!')

        headlineAssetLinkText_max_length = 30
        for headlineAssetLink in headlineAssetLinks:

            # Check asset text
            headlineAssetLinkText = headlineAssetLink['assetText']
            if len(headlineAssetLinkText) > headlineAssetLinkText_max_length:
                raise AttributeError('headlineAssetLinkText length must be < {headlineAssetLinkText_max_length}!'.format(headlineAssetLinkText_max_length = headlineAssetLinkText_max_Length), headlineAssetLinkText)
            if type(headlineAssetLinkText) != str:
                raise TypeError('headlineAssetLinkText must be str!', headlineAssetLinkText)
            if headlineAssetLinkText == 'nan':
                raise AttributeError('headlineAssetLinkText nan!', headlineAssetLinkText)

            # Check pin
            headlineAssetLinkPinnedField_valid_values = ['NONE', 'HEADLINE_1', 'HEADLINE_2', 'HEADLINE_3']
            headlineAssetLinkPinnedField = headlineAssetLink['pinnedField']
            if headlineAssetLinkPinnedField not in headlineAssetLinkPinnedField_valid_values:
                raise AttributeError('headlineAssetLinkPinnedField must be one of {headlineAssetLinkPinnedField_valid_values}'.format(headlineAssetLinkPinnedField_valid_values = headlineAssetLinkPinnedField_valid_values))

    def validate_descriptionAssetLinks(self, descriptionAssetLinks):
        if type(descriptionAssetLinks) != list:
            raise TypeError('descriptionAssetLinks must be list!')


        for descriptionAssetLink in descriptionAssetLinks:
            if descriptionAssetLink['pinnedField'] == 'HEADLINE_1':
                descriptionAssetLinkText_max_length = 80
            else:
                descriptionAssetLinkText_max_length = 90

            # Check asset text
            descriptionAssetLinkText = descriptionAssetLink['assetText']
            if len(descriptionAssetLinkText) > descriptionAssetLinkText_max_length:
                raise AttributeError('descriptionAssetLinkText length must be < {descriptionAssetLinkText_max_length}!'.format(descriptionAssetLinkText_max_length = descriptionAssetLinkText_max_length), descriptionAssetLinkText)
            if type(descriptionAssetLinkText) != str:
                raise TypeError('descriptionAssetLinkText must be str!', descriptionAssetLinkText)
            if descriptionAssetLinkText == 'nan':
                raise AttributeError('descriptionAssetLinkText nan!', descriptionAssetLinkText)

            # Check pin
            descriptionAssetLinkPinnedField_valid_values = ['NONE', 'DESCRIPTION_1', 'DESCRIPTION_2']
            descriptionAssetLinkPinnedField = descriptionAssetLink['pinnedField']
            if descriptionAssetLinkPinnedField not in descriptionAssetLinkPinnedField_valid_values:
                raise AttributeError('descriptionAssetLinkPinnedField must be one of {descriptionAssetLinkPinnedField_valid_values}'.format(descriptionAssetLinkPinnedField_valid_values = descriptionAssetLinkPinnedField_valid_values), descriptionAssetLinkPinnedField)

    def validate_path1(self, path1):
        # Check nan
        if path1 == 'nan':
            raise AttributeError('path1 nan!', path1)


        # Check max length
        path1_max_length = 15
        if len(path1) > path1_max_length:
            raise AttributeError('path1 length must be < {path1_max_length}!'.format(path1_max_length = path1_max_length))

    def validate_path2(self, path2):
        # Check nan
        if path2 == 'nan':
            raise AttributeError('path2 nan!', path1)

        # Check max length
        path2_max_length = 15
        if len(path2) > path2_max_length:
            raise AttributeError('path2 length must be < {path2_max_length}!'.format(path2_max_length = pax2_max_length))

    def validate_finalUrls(self, finalUrls):
        # Check nan
        for finalUrl in finalUrls:
            if finalUrl == 'nan':
                raise AttributeError('finalUrl {finalUrl} nan!'.format(finalUrl = finalUrl))








class ExpandedTextAdPrototype(object):
    def __init__(self, adGroupId, headlinePart1, headlinePart2, description, path1, path2, finalUrls):


        self.validate_fields(adGroupId, headlinePart1, headlinePart2, description, path1, path2, finalUrls)
        self.adGroupId = adGroupId
        self.headlinePart1 = headlinePart1
        self.headlinePart2 = headlinePart2
        self.description = description
        self.path1 = path1
        self.path2 = path2
        self.finalUrls = finalUrls

    def format_add_operand(self):
        operand = {
            'xsi_type': 'AdGroupAd',
            'adGroupId': self.adGroupId,
            'ad': {
                'xsi_type': 'ExpandedTextAd',
                'headlinePart1': self.headlinePart1,
                'headlinePart2': self.headlinePart2,
                'description': self.description,
                'path1': self.path1,
                'path2': self.path2,
                'finalUrls': [self.finalUrls]
                },
            'status': 'PAUSED'
            }

        return operand

    def validate_fields(self, adGroupId, headlinePart1, headlinePart2, description, path1, path2, finalUrls):

        # Check to make sure all are strings
        for field in [adGroupId, headlinePart1, headlinePart2, description, path1, path2, finalUrls]:
            if type(field) != str:
                raise AttributeError('field is not string!', field)

        # Check individual fields
        self.validate_adGroupId(adGroupId)
        self.validate_headlinePart1(headlinePart1)
        self.validate_headlinePart2(headlinePart2)
        self.validate_description(description)
        self.validate_path1(path1)
        self.validate_path2(path2)
        self.validate_finalUrls(finalUrls)

    def validate_adGroupId(self, adGroupId):
        return True

    def validate_headlinePart1(self, headlinePart1):

        # Check nan
        if headlinePart1 == 'nan':
            raise AttributeError('headlinePart1 contains nan!')

        # Check length
        if len(headlinePart1) > 30:
            raise AttributeError('headlinePart1 length exceeds maximum!')



    def validate_headlinePart2(self, headlinePart2):

        # Check nan
        if headlinePart2 == 'nan':
            raise AttributeError('headlinePart2 contains nan!')

        # Check length
        if len(headlinePart2) > 30:
            raise AttributeError('headlinePart2 length exceeds maximum!')



    def validate_description(self, description):

        # Check nan
        if description == 'nan':
            raise AttributeError('description contains nan!')

        # Check length
        if len(description) > 80:
            raise AttributeError('description length exceeds maximum!')



    def validate_path1(self, path1):

        # Check nan
        if path1 == 'nan':
            raise AttributeError('path 1 contains nan!')

        # Check length
        if len(path1) > 15:
            raise AttributeError('path1 length exceeds maximum!')



    def validate_path2(self, path2):

        # Check nan
        if path2 == 'nan':
            raise AttributeError('path 2 contains nan!')

        # Check length
        if len(path2) > 15:
            raise AttributeError('path 2 length exceeds maximum!')

    def validate_finalUrls(self, finalUrls):

        # Check nan
        if finalUrls == 'nan':
            raise AttributeError('final url contains nan!')
