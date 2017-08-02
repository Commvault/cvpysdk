
class SEDSType(object):
    ds_type_dict = {
        0: 'NONE',
        1: 'jdbc',
        2: 'web',
        3: 'exe',
        4: 'csv',
        5: 'file',
        6: 'nas',
        7: 'eloqua',
        8: 'salesforce',
        9: 'ldap',
        10: 'federated',
        11: 'blank',
        12: 'http',
        13: 'camel',
        14: 'facebook',
        15: 'fla',
        16: 'edge',
        17: 'exchange',
        18: 'reviewset',
        19: 'twitter',
        20: 'complianceaudit',
        21: 'fsindex',
        22: 'nfs',
        23: 'cloudoracle',
        24: 'systemdefault',
        25: 'downloadcenteraudit'
    }

    @staticmethod
    def get_name_from_value(value):
        return SEDSType.ds_type_dict.get(value)

