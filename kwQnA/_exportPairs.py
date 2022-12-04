# import json
# import pandas
import os


class exportToJSON:
    """docstring for exportToJSON."""

    def __init__(self):
        super(exportToJSON, self).__init__()

    def dumpdata(self, pairs):
        if os.path.exists(os.path.join(os.getcwd(), 'extra')):
                pass
        else:
                os.makedirs('extra')
        my_data = pairs.to_json('extra/database.json', orient='index')
        # print(my_data)

class exportToCSV:
    """docstring for exportToJSON."""

    def __init__(self):
        super(exportToJSON, self).__init__()

    def dumpdata(self, pairs):
        df = pairs.to_csv(index=False)
        # ff = pairs.to_csv('out.zip', index=False, compression=compression_opts)
        # print(df)

        # df = pd.DataFrame({'name': ['Raphael', 'Donatello'],
        #                    'mask': ['red', 'purple'],
        #                    'weapon': ['sai', 'bo staff']})
        #
        # df.to_csv(index=False)
        # 'name,mask,weapon\nRaphael,red,sai\nDonatello,purple,bo staff\n'
        #
        # Create ‘out.zip’ containing ‘out.csv’

        # compression_opts = dict(method='zip',
        #                         archive_name='out.csv')

        # df.to_csv('out.zip', index=False,
        #           compression=compression_opts)
