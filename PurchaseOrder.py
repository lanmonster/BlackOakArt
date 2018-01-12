class PurchaseOrder:
    def __init__(self, data):
        self.progress = 0
        self.item = data[0]
        self.glaze_color = data[1]
        self.description = data[2]
        self.delivery_date = data[3]
        self.company = data[4]
        self.buffer = data[5]
        self.amount = data[6]
        self.id = data[7]
        self.miscellaneous = data[8]
        self.adjusted_amount = data[9]
        self.clay_type = data[10]
        self.data = data

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
        return (str(self.id) + '\n' +
                self.company + '\n' +
                self.item + '\n' +
                self.clay_type + '\n' +
                self.glaze_color + '\n' +
                str(self.amount) + '\n' +
                str(self.buffer * 100) + '%\n' +
                str(self.adjusted_amount) + '\n' +
                self.description + '\n' +
                self.miscellaneous + '\n' +
                str(self.progress) + '\n' +
                self.delivery_date.strftime('%Y/%m/%d'))

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
