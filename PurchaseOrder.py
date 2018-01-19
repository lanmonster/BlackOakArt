class PurchaseOrder:
    def __init__(self, data):
        self.id = data[0]
        self.company = data[1]
        self.item = data[2]
        self.clay_type = data[3]
        self.glaze_color = data[4]
        self.amount = data[5]
        self.buffer = data[6]
        self.adjusted_amount = data[7]
        self.description = data[8]
        self.miscellaneous = data[9]
        self.delivery_date = data[10]
        self.data = data
        self.progress = 0

    def __iter__(self):
        for x in self.data:
            yield x

    @property
    def to_string(self):
        result = ('PO #' + str(self.id) +
                  '\nCompany: ' + self.company +
                  '\nItem: ' + self.item +
                  '\nClay Type: ' + self.clay_type +
                  '\nGlaze Color: ' + self.glaze_color +
                  '\nAmount: ' + str(self.amount) +
                  '\nBuffer: ' + str(self.buffer * 100) + '%' +
                  '\nAdjusted Amount: ' + str(self.adjusted_amount) +
                  '\nDescription: ' + self.description)

        if self.miscellaneous:
            result += '\nMiscellaneous Info: ' + self.miscellaneous

        result += ('\nPercent complete: ' + str(self.progress) + '%' +
                   '\nDelivery Date: ' + self.delivery_date.strftime('%Y/%m/%d'))

        return result

    def to_table_values(self):
        return ["%s\n" % str(self.id),
                "%s\n" % str(self.company),
                "%s\n" % str(self.item),
                "%s\n" % str(self.clay_type),
                "%s\n" % str(self.glaze_color),
                "%s\n" % str(self.amount),
                "%s\n" % str(int(self.buffer * 100)),
                "%s\n" % str(self.adjusted_amount),
                "%s\n" % str(self.description),
                "%s\n" % str(self.miscellaneous),
                "%s\n" % str(self.progress),
                "%s" % str(self.delivery_date.strftime('%Y/%m/%d'))
                ]

    def update_progress(self, progress):
        self.progress = progress

    def to_dict(self):
        return {
            'id': str(self.id),
            'company': self.company,
            'item': self.item,
            'clay type': self.clay_type,
            'glaze color': self.glaze_color,
            'amount': self.amount,
            'buffer': self.buffer,
            'adjusted amount': self.adjusted_amount,
            'description': self.description,
            'miscellaneous': self.miscellaneous,
            'percent complete': str(self.progress),
            'delivery date': self.delivery_date.strftime('%Y/%m/%d')
        }
