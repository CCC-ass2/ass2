function (doc) {
  emit([doc.location, doc.district, doc.sentiment_polarity.res],1)
}