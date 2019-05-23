

class ProductSummarySlot(object):
    def __init__(self, index, productUrl, imageUrl, isFAssured, rating, reviewCount, title, totalDiscount, mrp, finalPrice):
        self.index = index
        self.productUrl = productUrl
        self.imageUrl = imageUrl
        self.isFAssured = isFAssured
        self.rating = rating
        self.reviewCount = reviewCount
        self.title = title
        self.totalDiscount = totalDiscount
        self.mrp = mrp
        self.finalPrice = finalPrice

    def serialize(self):
        return {
            'index': self.index,
            'productUrl': self.productUrl,
            'imageUrl': self.imageUrl,
            'isFAssured': self.isFAssured,
            'rating': self.rating,
            'reviewCount': self.reviewCount,
            'title': self.title,
            'totalDiscount': self.totalDiscount,
            'mrp': self.mrp,
            'finalPrice': self.finalPrice,
        }


class MapiModel(object):
    def __init__(self, query, productsShown, searchUrl, productCount, productSummarySlots):
        self.query = query
        self.searchUrl = searchUrl
        self.productsShown = productsShown
        self.productCount = productCount
        self.productSummarySlots = productSummarySlots

    def serialize(self):
        return {
            'query': self.query,
            'searchUrl': self.searchUrl,
            'productsShown': self.productsShown,
            'productCount': self.productCount,
            'productSummarySlots': [productSummarySlot.serialize() for productSummarySlot in self.productSummarySlots]
        }
