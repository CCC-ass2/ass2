function (doc) {
  emit([doc.location, doc.sentiment_polarity.res, doc.time.date],1)
}