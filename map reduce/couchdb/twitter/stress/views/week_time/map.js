function (doc) {
  emit([doc.location, doc.time.date, doc.time.weekday, doc.district],1)
}
