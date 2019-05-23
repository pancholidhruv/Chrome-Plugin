

class ProductSummarySlot(object):
    def __init__(self, productUrl, imageUrl, isFAssured, rating, title, totalDiscount, mrp, finalPrice):
        self.productUrl = productUrl
        self.imageUrl = imageUrl
        self.isFAssured = isFAssured
        self.rating = rating
        self.title = title
        self.totalDiscount = totalDiscount
        self.mrp = mrp
        self.finalPrice = finalPrice

    def serialize(self):
        return {
            'productUrl': self.productUrl,
            'imageUrl': self.imageUrl,
            'isFAssured': self.isFAssured,
            'rating': self.rating,
            'title': self.title,
            'totalDiscount': self.totalDiscount,
            'mrp': self.mrp,
            'finalPrice': self.finalPrice,
        }


class MapiModel(object):
    def __init__(self, productCount, productSummarySlots):
        self.productCount = productCount
        self.productSummarySlots = productSummarySlots

    def serialize(self):
        return {
            'productCount': self.productCount,
            'productSummarySlots': [productSummarySlot.serialize() for productSummarySlot in self.productSummarySlots]
        }
