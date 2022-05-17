function (doc) {
  emit(doc._id, [doc.location, doc.sentiment_polarity.res, doc.text])
}